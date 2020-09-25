from __future__ import annotations

from .insta_scraper import StaticInstaScraper


class Profile(StaticInstaScraper):
    def __init__(self, url):
        super().__init__(url)

    def _scrape_soup(self):
        """Scrape data from the profile page"""
        super()._scrape_soup()

    def _scrape_json(self, prof_json: dict):
        self.country_code = prof_json["country_code"]
        self.language_code = prof_json["language_code"]
        self.locale = prof_json["locale"]

        # Convenience definition for prof info
        self.prof_info = prof_json["entry_data"]["ProfilePage"][0]["graphql"]["user"]
        self.biography = self.prof_info["biography"]
        self.blocked_by_viewer = self.prof_info["blocked_by_viewer"]
        self.business_email = self.prof_info["business_email"]
        self.restricted_by_viewer = self.prof_info["restricted_by_viewer"]
        self.country_block = self.prof_info["country_block"]
        self.external_url = self.prof_info["external_url"]
        self.followers = self.prof_info["edge_followed_by"]["count"]
        self.followed_by_viewer = self.prof_info["followed_by_viewer"]
        self.following = self.prof_info["edge_follow"]["count"]
        self.follows_viewer = self.prof_info["follows_viewer"]
        self.name = self.prof_info["full_name"]
        self.has_ar_effects = self.prof_info["has_ar_effects"]
        self.has_clips = self.prof_info["has_clips"]
        self.has_guides = self.prof_info["has_guides"]
        self.has_channel = self.prof_info["has_channel"]
        self.has_blocked_viewer = self.prof_info["has_blocked_viewer"]
        self.highlight_reel_count = self.prof_info["highlight_reel_count"]
        self.has_requested_viewer = self.prof_info["has_requested_viewer"]
        self.id = self.prof_info["id"]
        self.is_business_account = self.prof_info["is_business_account"]
        self.is_joined_recently = self.prof_info["is_joined_recently"]
        self.business_category = self.prof_info["business_category_name"]
        self.overall_category = self.prof_info["overall_category_name"]
        self.category_enum = self.prof_info["category_enum"]
        self.is_private = self.prof_info["is_private"]
        self.is_verified = self.prof_info["is_verified"]
        self.mutual_followed_by = self.prof_info["edge_mutual_followed_by"]["count"]
        self.profile_pic_url = self.prof_info["profile_pic_url"]
        self.requested_by_viewer = self.prof_info["requested_by_viewer"]
        self.username = self.prof_info["username"]
        self.connected_fb_page = self.prof_info["connected_fb_page"]
        self.posts = self.prof_info["edge_owner_to_timeline_media"]["count"]

    @classmethod
    def from_username(cls, username: str):
        url = f"https://www.instagram.com/{username}/"
        return cls(url)


if __name__ == "__main__":
    url = r"https://www.instagram.com/chris_greening/"
    profile = Profile(url)
    profile.static_load()
