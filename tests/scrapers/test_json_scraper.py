import pytest

import requests

from instascrape.scrapers.json_tools import json_from_html, determine_json_type, json_from_url

@pytest.fixture
def source_html():
    """Return the source HTML from the given page"""
    url = "https://www.instagram.com/chris_greening/"
    source_html = requests.get(url).text
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
