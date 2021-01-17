import csv
import json
import os

from bs4 import BeautifulSoup
import pytest
import requests

from instascrape import Location

class TestHashtag:

    @pytest.fixture
    def url(self):
        return "https://www.instagram.com/explore/locations/212918601/grand-central-terminal/"

    @pytest.fixture(scope="session")
    def headers(self):
        return {"User-Agent": "user-agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.57",
                "cookie": f"sessionid={os.environ.get('sessionid')};"}

    @pytest.fixture
    def get_request(self, url, headers):
        return requests.get(url, headers=headers)

    @pytest.fixture
    def page_instance(self, url, headers):
        random_location = Location(url)
        random_location.scrape(headers=headers)
        return random_location

    def test_from_html(self, get_request, page_instance):
        location_html = get_request.text
        location_obj = Location(location_html)
        location_obj.scrape()
        assert location_obj.amount_of_posts == page_instance.amount_of_posts

    def test_from_soup(self, get_request, page_instance):
        location_html = get_request.text
        location_soup = BeautifulSoup(location_html, features='lxml')
        location_obj = Location(location_soup)
        location_obj.scrape()
        assert location_obj.amount_of_posts == page_instance.amount_of_posts

    def test_to_dict(self, page_instance):
        assert isinstance(page_instance.to_dict(), dict)

    @pytest.mark.file_io
    def test_to_json(self, page_instance, tmpdir):
        file = tmpdir.join("data.json")
        page_instance.to_json(fp=str(file))
        with open(str(file), "r") as injson:
            json_dict = json.load(injson)
        assert page_instance['name'] == json_dict['name']

    @pytest.mark.file_io
    def test_to_csv(self, page_instance, tmpdir):

        # write to CSV
        file = tmpdir.join("data.csv")
        page_instance.to_csv(fp=str(file))

        # reread the csv
        with open(str(file), mode="r") as infile:
            reader = csv.reader(infile)
            csv_dict = {row[0]: row[1] for row in reader}

        assert page_instance['name'] == csv_dict['name']
