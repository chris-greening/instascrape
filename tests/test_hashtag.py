import pytest

from instascrape import Hashtag


@pytest.fixture
def kotlin_hashtag():
    kotlin_hashtag_name = "kotlin"
    kotlin_hashtag_url = f"https://www.instagram.com/tags/{kotlin_hashtag_name}/"

    kotlin_hashtag = Hashtag(url=kotlin_hashtag_url, name=kotlin_hashtag_name)
    kotlin_hashtag.static_load()

    return kotlin_hashtag


def test_from_hashtag(kotlin_hashtag):
    result_hashtag: Hashtag = Hashtag.from_hashtag(hashtag=kotlin_hashtag.name)
    result_hashtag.static_load()

    assert result_hashtag.url == kotlin_hashtag.url
    assert result_hashtag.name == kotlin_hashtag.name
