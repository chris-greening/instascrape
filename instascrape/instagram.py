from __future__ import annotations
# pylint: disable=unused-wildcard-import

from typing import Dict

from instascrape.scrapers import * 

class Instagram:
    def scrape_profile(self, profile: str) -> Dict[str, str]:
        profile_obj = Profile.from_username(profile)
        return profile_obj.recent_data.to_dict()