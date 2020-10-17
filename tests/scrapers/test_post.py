import re
import json
import csv
import datetime

import pytest

from instascrape import Post


class TestHashtag:
    @pytest.fixture
    def page_instance(self):
        google_post_url = f"https://www.instagram.com/p/CGX0G64hu4Q/"
        random_google_post = Post(url=google_post_url)
        random_google_post.load()
        return random_google_post

    def test_to_dict(self, page_instance):
        assert type(page_instance.to_dict()) == dict

    @pytest.mark.file_io
    def test_to_json(self, page_instance, tmpdir):
        file = tmpdir.join("data.json")
        page_instance.to_json(fp=str(file))
        with open(str(file), "r") as injson:
            json_dict = json.load(injson)
        json_dict["upload_date"] = datetime.datetime.fromtimestamp(
            int(json_dict["upload_date"])
        )
        assert page_instance.to_dict() == json_dict

    @pytest.mark.file_io
    def test_to_csv(self, page_instance, tmpdir):

        # write to CSV
        file = tmpdir.join("data.csv")
        page_instance.to_csv(fp=str(file))

        # reread the csv
        with open(str(file), mode="r") as infile:
            reader = csv.reader(infile)
            csv_dict = {row[0]: row[1] for row in reader}
        csv_dict["upload_date"] = str(
            datetime.datetime.fromtimestamp(float(csv_dict["upload_date"]))
        )

        # have to convert everything to str otherwise AssertionError will trip
        # up comparing stuff like True == 'True'
        str_dict = {}
        for key, val in page_instance.to_dict().items():
            if val is None:
                val = ""
            str_dict[key] = str(val)

        assert str_dict == csv_dict

    def test_from_shortcode(self, page_instance):
        expected_post = "CGX0G64hu4Q"
        result_profile: Post = Post.from_shortcode(shortcode=expected_post)

        assert result_profile.url == page_instance.url
