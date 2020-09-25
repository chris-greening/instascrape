from __future__ import annotations

import datetime
from typing import List

from .insta_scraper import StaticInstaScraper


class Post(StaticInstaScraper):
    def __init__(self, url: str) -> None:
        super().__init__(url)

    def _scrape_soup(self) -> None:
        """Scrape data from the soup"""
        super()._scrape_soup()
        self.hashtags = self._get_hashtags()

    def _get_hashtags(self) -> List[str]:
        hashtags_meta = self.soup.find_all("meta", {"property": "instapp:hashtags"})
        return [tag["content"] for tag in hashtags_meta]

    def _scrape_json(self, post_json: dict) -> None:
        """Scrape data from the posts json"""
        # TODO: might be a good idea to store these vars in a dataclass
        self.country_code = post_json["country_code"]
        self.language_code = post_json["language_code"]
        self.locale = post_json["locale"]

        # Convenience definition for post info
        post_info = post_json["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]
        self.upload_date = datetime.datetime.fromtimestamp(
            post_info["taken_at_timestamp"]
        )
        self.accessibility_caption = post_info["accessibility_caption"]
        self.likes = post_info["edge_media_preview_like"]["count"]
        self.amount_of_comments = post_info["edge_media_preview_comment"]["count"]
        self.caption_is_edited = post_info["caption_is_edited"]
        self.has_ranked_comments = post_info["has_ranked_comments"]
        self.location = post_info["location"]
        self.is_ad = post_info["is_ad"]
        self.viewer_can_reshare = post_info["viewer_can_reshare"]
        self.shortcode = post_info["shortcode"]
        self.dimensions = post_info["dimensions"]
        self.is_video = post_info["is_video"]
        self.fact_check_overall_rating = post_info["fact_check_overall_rating"]
        self.fact_check_information = post_info["fact_check_information"]

        # Get caption and tagged users
        self.caption = post_info["edge_media_to_caption"]["edges"][0]["node"]["text"]
        self.tagged_users = self._get_tagged_users(post_info)

        # Owner json data
        owner = post_info["owner"]
        self.is_verified = owner["is_verified"]
        self.profile_pic_url = owner["profile_pic_url"]
        self.username = owner["username"]
        self.blocked_by_viewer = owner["blocked_by_viewer"]
        self.followed_by_viewer = owner["followed_by_viewer"]
        self.full_name = owner["full_name"]
        self.has_blocked_viewer = owner["has_blocked_viewer"]
        self.is_private = owner["is_private"]

    def _get_tagged_users(self, post_info: dict) -> List[str]:
        """Scrape the usernames of the tagged users"""
        tagged_users_json = post_info["edge_media_to_tagged_user"]["edges"]
        return [user["node"]["user"]["username"] for user in tagged_users_json]

    @classmethod
    def from_shortcode(cls, shortcode: str) -> Post:
        """Return a Post given a shortcode"""
        url = f"https://www.instagram.com/p/{shortcode}/"
        return cls(url)


if __name__ == "__main__":
    url = r"https://www.instagram.com/p/CFQNno8hSDX/"
    post = Post(url)
    post.static_load()
