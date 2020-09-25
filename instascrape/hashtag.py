from __future__ import annotations

from .insta_scraper import StaticInstaScraper


class Hashtag(StaticInstaScraper):
    def __init__(self, url):
        super().__init__(url)

    def _scrape_json(self, json_data: dict):
        """Scrape the JSON"""
        self.country_code = json_data["country_code"]
        self.language_code = json_data["language_code"]
        self.locale = json_data["locale"]

        tag_data = json_data["entry_data"]["TagPage"][0]["graphql"]["hashtag"]
        self.id = tag_data["id"]
        self.name = tag_data["name"]
        self.allow_following = tag_data["allow_following"]
        self.is_following = tag_data["is_following"]
        self.is_top_media_only = tag_data["is_top_media_only"]
        self.profile_pic_url = tag_data["profile_pic_url"]
        self.amount_of_posts = tag_data["edge_hashtag_to_media"]["count"]

    @classmethod
    def from_hashtag(cls, hashtag: str):
        url = f"https://www.instagram.com/tags/{hashtag}/"
        return cls(url)


if __name__ == "__main__":
    url = "https://www.instagram.com/explore/tags/worldviewmag/"
    worldviewmag = Hashtag(url)
    worldviewmag.static_load()
