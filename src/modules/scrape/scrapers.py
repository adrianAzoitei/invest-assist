from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver import ChromeOptions
from typing import override

class Scraper:
    def __init__(self, url: str, wait: int) -> None:
        options = ChromeOptions()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options)
        self.wait = WebDriverWait(self.driver, wait)
        self.url = url
        self.driver.get(url)
        self.levels = 0
        
    def click(self, element: WebElement) -> None:
        self.levels += 1
        element.click()
    
    def back(self, diff: int = 0):
        if diff != None:
            for _ in range(0, diff):
                self.driver.back()
        else:
            for _ in range(0, self.levels):
                self.driver.back()
        
    def clickable(self, tuple: tuple[str, str]) -> WebElement:
        return self.wait.until(EC.element_to_be_clickable(tuple))
    
    def visible(self, tuple: tuple[str, str]) -> WebElement:
        return self.wait.until(EC.presence_of_element_located(tuple))
    
    def get_tickers_per_sector(self, sector: str) -> list: # define Ticker and return list[Ticker]
         raise NotImplementedError("Generic Scraper does not know how to execute: get_tickers_per_sector")
        
class YHFinanceScraper(Scraper):
    def __init__(self, config: dict) -> None:
        super().__init__(config['scrapers']['yhfinance']['url'], int(config['wait']))
        self.xpaths = config['scrapers']['yhfinance']['xpaths']
        
        # accept cookies
        self.clickable((By.XPATH, self.xpaths['cookie_button'])).click()
        
    @override
    def get_tickers_per_sector(self, sector: str) -> list: # define Ticker and return list[Ticker]
        self.driver.get(f"{self.url}/sectors")
        sectors: list[WebElement] = self.visible((By.XPATH, self.xpaths['sectors_table'])).find_elements(By.TAG_NAME, 'tr')
        for sector_element in sectors:
            sector_name = sector_element.find_elements(By.TAG_NAME, 'td')[0].text
            if sector_name.lower() == sector:
                self.click(sector_element)
                self.click(self.clickable((By.XPATH, f"{self.xpaths['go_to_sector']}[contains(@href, '/sectors/{sector_name.lower().replace(' ', '-')}')]")))
                break
        