from instascrape.scrapers.json_scraper import JsonScraper
from instascrape.core._json_flattener import JsonFlattener

from instascrape.scrapers.json_scraper import JsonScraper

url = 'https://www.instagram.com/chris_greening/'
json_scraper = JsonScraper()
json_dict = json_scraper.json_from_url(url)

flat = JsonFlattener(json_dict)
