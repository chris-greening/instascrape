from __future__ import annotations
# pylint: disable=unused-wildcard-import

from typing import Dict

from instascrape.scrapers import *

class InstaScrape:
    def scrape_profile(self, username: str) -> Dict[str, str]:
        profile = Profile.from_username(username)
        profile.load()
        return profile.to_dict()

    def scrape_post(self, url: str) -> Dict[str, str]:
        post = Post(url)
        post.load()
        return post.recent_data.to_dict()

    def scrape_hashtag(self, hashtag: str) -> Dict[str, str]:
        hashtag = Hashtag.from_hashtag(hashtag)
        hashtag.load()
        return hashtag.recent_data.to_dict()
