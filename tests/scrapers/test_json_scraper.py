import pytest
import requests

from instascrape.scrapers.json_tools import determine_json_type, json_from_html, json_from_url


@pytest.fixture
def source_html():
    """Return the source HTML from the given page"""
    url = "https://www.instagram.com/chris_greening/"
    source_html = requests.get(url, headers={
                               "User-Agent": "user-agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.57"}).text
    return source_html


def test_json_from_html(source_html):
    json_dict = json_from_html(source_html)
    assert type(json_dict) == dict
    assert "entry_data" in json_dict


def test_determine_json_type(source_html):
    json_dict = json_from_html(source_html)
    json_type = determine_json_type(json_dict)
    assert json_type == "ProfilePage"


def test_json_from_url():
    url = "https://www.instagram.com/chris_greening/"
    json_dict = json_from_url(url)
    assert type(json_dict) == dict
    assert "entry_data" in json_dict
