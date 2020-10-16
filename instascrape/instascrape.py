from __future__ import annotations
# pylint: disable=unused-wildcard-import

from typing import Dict

from instascrape.scrapers import *

class InstaScrape:
    def scrape_profile(self, username: str) -> Dict[str, str]:
        profile_obj = Profile.from_username(username)
        profile_obj.load()
        return profile_obj.recent_data.to_dict()

    def scrape_post(self, url: str) -> Dict[str, str]:
        post_obj = Post(url)
        post_obj.load()
        return post_obj.recent_data.to_dict()

    def scrape_hashtag(self, hashtag: str) -> Dict[str, str]:
        hashtag_obj = Hashtag.from_hashtag(hashtag)
        hashtag_obj.load()
        return hashtag_obj.recent_data.to_dict()
