from instascrape.scrapers.json_scraper import JsonScraper
from instascrape.core._json_flattener import JsonTree

from instascrape.scrapers.json_scraper import JsonScraper

url = 'https://www.instagram.com/chris_greening/'
json_scraper = JsonScraper()
json_dict = json_scraper.json_from_url(url)

tree = JsonTree(json_dict)
