import csv
import json

from bs4 import BeautifulSoup
import pytest

from instascrape import Hashtag


class TestHashtag:
    @pytest.fixture
    def page_instance(self):
        kotlin_hashtag_name = "kotlin"
        kotlin_hashtag_url = f"https://www.instagram.com/tags/{kotlin_hashtag_name}/"

        kotlin_hashtag = Hashtag(kotlin_hashtag_url)
        kotlin_hashtag.load()

        return kotlin_hashtag

    def test_from_html(self, page_instance):
        hashtag_html = page_instance.html
        hashtag_obj = Hashtag(hashtag_html)
        hashtag_obj.scrape()
        assert hasattr(hashtag_obj, 'amount_of_posts')

    def test_from_soup(self, page_instance):
        hashtag_html = page_instance.html
        hashtag_soup = BeautifulSoup(hashtag_html, features='lxml')
        hashtag_obj = Hashtag(hashtag_soup)
        hashtag_obj.scrape()
        assert hasattr(hashtag_obj, 'amount_of_posts')

    def test_to_dict(self, page_instance):
        assert type(page_instance.to_dict()) == dict

    # @pytest.mark.file_io
    # def test_to_json(self, page_instance, tmpdir):
    #     file = tmpdir.join("data.json")
    #     page_instance.to_json(fp=str(file))
    #     with open(str(file), "r") as injson:
    #         json_dict = json.load(injson)
    #     assert page_instance.to_dict() == json_dict

    # @pytest.mark.file_io
    # def test_to_csv(self, page_instance, tmpdir):

    #     # write to CSV
    #     file = tmpdir.join("data.csv")
    #     page_instance.to_csv(fp=str(file))

    #     # reread the csv
    #     with open(str(file), mode="r") as infile:
    #         reader = csv.reader(infile)
    #         csv_dict = {row[0]: row[1] for row in reader}

    #     # have to convert everything to str otherwise AssertionError will trip
    #     # up comparing stuff like True == 'True'
    #     str_dict = {}
    #     for key, val in page_instance.to_dict().items():
    #         if val is None:
    #             val = ""
    #         str_dict[key] = str(val)

    #     assert str_dict == csv_dict
