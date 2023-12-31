
from time import sleep
from pprint import pprint
from modules.scrape.scrapers import Scraper, YHFinanceScraper
import yaml

scrapers: dict[str, Scraper] = {}
with open('config/selenium.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    scrapers['yhfinance'] = YHFinanceScraper(config)
    
for scraper in scrapers.values():
    scraper.get_tickers_per_sector('technology')
    scraper.get_tickers_per_sector('financial services')
    scraper.get_tickers_per_sector('basic materials')
    scraper.get_tickers_per_sector('energy')
    scraper.get_tickers_per_sector('real estate')