import csv
import json

import pytest
from bs4 import BeautifulSoup
import requests

from instascrape import Post, Profile


class TestProfile:

    @pytest.fixture
    def url(self):
        return "https://www.instagram.com/chris_greening/"

    @pytest.fixture
    def get_request(self, url):
        return requests.get(url, headers={"User-Agent": "user-agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.57"})

    @pytest.fixture
    def page_instance(self, url):
        random_profile = Profile(url)
        random_profile.load()
        return random_profile

    def test_from_html(self, get_request, page_instance):
        profile_html = get_request.text
        profile_obj = Profile(profile_html)
        profile_obj.scrape()
        assert profile_obj.followers == page_instance.followers

    def test_from_soup(self, get_request, page_instance):
        profile_html = get_request.text
        profile_soup = BeautifulSoup(profile_html, features='lxml')
        profile_obj = Profile(profile_soup)
        profile_obj.scrape()
        assert profile_obj.followers == page_instance.followers

    def test_to_dict(self, page_instance):
        assert isinstance(page_instance.to_dict(), dict)

    def test_get_recent_posts(self, page_instance):
        posts = page_instance.get_recent_posts(amt=6)
        assert len(posts) == 6
        assert all([type(post) is Post for post in posts])
        assert all([hasattr(post, "id") for post in posts])

    @pytest.mark.file_io
    def test_to_json(self, page_instance, tmpdir):
        file = tmpdir.join("data.json")
        page_instance.to_json(fp=str(file))
        with open(str(file), "r") as injson:
            json_dict = json.load(injson)
        assert page_instance['username'] == json_dict['username']

    @pytest.mark.file_io
    def test_to_csv(self, page_instance, tmpdir):

        # write to CSV
        file = tmpdir.join("data.csv")
        page_instance.to_csv(fp=str(file))

        # reread the csv
        with open(str(file), mode="r") as infile:
            reader = csv.reader(infile)
            csv_dict = {row[0]: row[1] for row in reader}

        assert page_instance['username'] == csv_dict['username']
