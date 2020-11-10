import csv
import json

from bs4 import BeautifulSoup
import pytest
import requests

from instascrape import Hashtag


class TestHashtag:

    @pytest.fixture
    def url(self):
        return "https://www.instagram.com/tags/kotlin/"

    @pytest.fixture
    def get_request(self, url):
        return requests.get(url)

    @pytest.fixture
    def page_instance(self, url):
        random_hashtag = Hashtag(url)
        random_hashtag.load()
        return random_hashtag

    def test_from_html(self, get_request, page_instance):
        hashtag_html = get_request.text
        hashtag_obj = Hashtag(hashtag_html)
        hashtag_obj.scrape()
        assert hashtag_obj.amount_of_posts == page_instance.amount_of_posts

    def test_from_soup(self, get_request, page_instance):
        hashtag_html = get_request.text
        hashtag_soup = BeautifulSoup(hashtag_html, features='lxml')
        hashtag_obj = Hashtag(hashtag_soup)
        hashtag_obj.scrape()
        assert hashtag_obj.amount_of_posts == page_instance.amount_of_posts

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
