import csv
import datetime
import json
import re

import pytest
from bs4 import BeautifulSoup
import requests

from instascrape import Post


class TestPost:
    @pytest.fixture
    def url(self):
        return "https://www.instagram.com/p/CGX0G64hu4Q/"

    @pytest.fixture
    def get_request(self, url):
        return requests.get(url)

    @pytest.fixture
    def page_instance(self, url):
        random_google_post = Post(url)
        random_google_post.load()
        return random_google_post

    def test_from_html(self, get_request, page_instance):
        post_html = get_request.text
        post_obj = Post(post_html)
        post_obj.scrape()
        assert post_obj.likes == page_instance.likes

    def test_from_soup(self, get_request, page_instance):
        post_html = get_request.text
        post_soup = BeautifulSoup(post_html, features='lxml')
        post_obj = Post(post_soup)
        post_obj.scrape()
        assert post_obj.likes == page_instance.likes

    def test_to_dict(self, page_instance):
        assert isinstance(page_instance.to_dict(), dict)

    @pytest.mark.file_io
    def test_to_json(self, page_instance, tmpdir):
        file = tmpdir.join("data.json")
        page_instance.to_json(fp=str(file))
        with open(str(file), "r") as injson:
            json_dict = json.load(injson)
        assert page_instance['shortcode'] == json_dict['shortcode']

    @pytest.mark.file_io
    def test_to_csv(self, page_instance, tmpdir):

        # write to CSV
        file = tmpdir.join("data.csv")
        page_instance.to_csv(fp=str(file))

        # reread the csv
        with open(str(file), mode="r") as infile:
            reader = csv.reader(infile)
            csv_dict = {row[0]: row[1] for row in reader}

        assert page_instance['shortcode'] == csv_dict['shortcode']
