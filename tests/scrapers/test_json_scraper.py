import pytest 

import requests

from instascrape import JsonScraper

class TestJsonScraper:
    @pytest.fixture
    def json_scraper(self):
        return JsonScraper()

    @pytest.fixture
    def source_html(self):
        url = 'https://www.instagram.com/chris_greening/'
        source_html = requests.get(url).text
        return source_html

    def test_json_from_html(self, json_scraper, source_html):
        json_dict = json_scraper.json_from_html(source_html)
        assert type(json_dict) == dict
        assert 'entry_data' in json_dict

    def test_determine_json_type(self, json_scraper, source_html):
        json_dict = json_scraper.json_from_html(source_html)
        json_type = json_scraper.determine_json_type(json_dict)
        assert json_type == 'ProfilePage'

    def test_json_from_url(self, json_scraper):
        url = 'https://www.instagram.com/chris_greening/'
        json_dict = json_scraper.json_from_url(url)
        assert type(json_dict) == dict
        assert 'entry_data' in json_dict
