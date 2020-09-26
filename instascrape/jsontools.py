from abc import ABC, abstractmethod
import datetime

from typing import List

class JSONScraper(ABC):
    def __init__(self, json_data: dict, name: str=None):
        """Container for storing all scraped data from Instagram JSON"""
        self.json_data = json_data
        if name is not None:
            self.name = name

    @abstractmethod
    def parse_json(self):
        """Parse JSON object"""

    @property
    def scraped_attr(self):
        """Return list of names of scraped data points"""
        pass

    def __repr__(self):
        class_name = type(self).__name__
        output_str = "<{}: " + f"{class_name}>"
        if hasattr(self, 'name'):
            return output_str.format(self.name)
        return output_str.format("unnamed")

class ProfileJSON(JSONScraper):
    def parse_json(self):
        self.country_code = self.json_data["country_code"]
        self.language_code = self.json_data["language_code"]
        self.locale = self.json_data["locale"]

        # Convenience definition for prof info
        self.prof_info =self.json_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]
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

class HashtagJSON(JSONScraper):
    def parse_json(self):
        self.country_code = self.json_data["country_code"]
        self.language_code = self.json_data["language_code"]
        self.locale = self.json_data["locale"]

        tag_data = self.json_data["entry_data"]["TagPage"][0]["graphql"]["hashtag"]
        self.id = tag_data["id"]
        self.name = tag_data["name"]
        self.allow_following = tag_data["allow_following"]
        self.is_following = tag_data["is_following"]
        self.is_top_media_only = tag_data["is_top_media_only"]
        self.profile_pic_url = tag_data["profile_pic_url"]
        self.amount_of_posts = tag_data["edge_hashtag_to_media"]["count"]

class PostJSON(JSONScraper):
    def parse_json(self):
        self.country_code = self.json_data["country_code"]
        self.language_code = self.json_data["language_code"]
        self.locale = self.json_data["locale"]

        # Convenience definition for post info
        post_info = self.json_data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]
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
        self.tagged_users = self.get_tagged_users()

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

    def get_tagged_users(self) -> List[str]:
        """Scrape the usernames of the tagged users"""
        tagged_users_json = self.json_data["entry_data"]["PostPage"][0][
            "graphql"]["shortcode_media"]["edge_media_to_tagged_user"]["edges"]
        return [user["node"]["user"]["username"] for user in tagged_users_json]
