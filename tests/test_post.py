import re

import pytest

from instascrape import Post

@pytest.fixture(scope='module')
def google_post() -> Post:
    google_post_url = f"https://www.instagram.com/p/CFkIz2UlIng/"
    random_google_post = Post(url=google_post_url)
    random_google_post.load()
    return random_google_post

def test_from_shortcode(google_post):
    result_post: Post = Post.from_shortcode(shortcode=google_post.shortcode)

    assert result_post.url == google_post.url

