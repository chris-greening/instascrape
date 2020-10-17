import pytest
import json
import csv

from instascrape import Profile
from instascrape import Post

class TestProfile:
    @pytest.fixture
    def page_instance(self):
        profile_url = "https://www.instagram.com/chris_greening/"
        profile_obj = Profile(profile_url)
        profile_obj.load()
        return profile_obj

    def test_to_dict(self, page_instance):
        assert type(page_instance.to_dict()) == dict

    def test_to_json(self, page_instance, tmpdir):
        file = tmpdir.join("data.json")
        page_instance.to_json(fp=str(file))
        with open(str(file), "r") as injson:
            json_dict = json.load(injson)
        assert page_instance.to_dict() == json_dict

    def test_to_csv(self, page_instance, tmpdir):

        # write to CSV
        file = tmpdir.join("data.csv")
        page_instance.to_csv(fp=str(file))

        # reread the csv
        with open(str(file), mode="r") as infile:
            reader = csv.reader(infile)
            csv_dict = {row[0]: row[1] for row in reader}

        # have to convert everything to str otherwise AssertionError will trip
        # up comparing stuff like True == 'True'
        str_dict = {}
        for key, val in page_instance.to_dict().items():
            if val is None:
                val = ""
            str_dict[key] = str(val)

        assert str_dict == csv_dict

    def test_from_username(self, page_instance):
        expected_profile_username = "chris_greening"
        result_profile: Profile = Profile.from_username(
            username=expected_profile_username
        )

        assert result_profile.url == page_instance.url

    def test_get_recent_posts(self, page_instance):
        posts = page_instance.get_recent_posts(amt=6)
        assert len(posts) == 6
        assert all([type(post) is Post for post in posts])