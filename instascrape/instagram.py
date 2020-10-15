from __future__ import annotations
# pylint: disable=unused-wildcard-import

from typing import Dict

from instascrape.scrapers import * 

class Instagram:
    def scrape_profile(self, profile: str) -> Dict[str, str]:
        profile_obj = Profile.from_username(profile)
        profile_obj.static_load()
        return profile_obj.recent_data.to_dict()

    def scrape_post(self, url: str) -> Dict[str, str]:
        post_obj = Post(url)
        post_obj.static_load()
        return post_obj.recent_data.to_dict()

    def scrape_hashtag(self, hashtag: str) -> Dict[str, str]:
        hashtag_obj = Hashtag.from_hashtag(hashtag)
        hashtag_obj.static_load()
        return hashtag_obj.recent_data.to_dict()
