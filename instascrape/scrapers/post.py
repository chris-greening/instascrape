from __future__ import annotations

import datetime
from typing import List, Any

import requests

from . import static_scraper
from . import json_scraper
from .hashtag import Hashtag

class Post(static_scraper.StaticHTMLScraper):
    """
    Scraper for a single post.

    Attribues
    ---------
    url : str
        Full URL to an existing Instagram profile

    Methods
    -------
    static_load(session=requests.Session())
        Makes request to URL, instantiates BeautifulSoup, finds JSON data,
        then parses JSON data.
    scrape_hashtags
    """

    def _scrape_soup(self, soup) -> None:
        """Scrape data from the soup"""
        self.hashtags = self._get_hashtags(soup)
        super()._scrape_soup(soup)

    def _get_hashtags(self, soup) -> List[str]:
        hashtags_meta = soup.find_all("meta", {"property": "instapp:hashtags"})
        return [tag["content"] for tag in hashtags_meta]

    def _scrape_json(self, json_data: dict) -> None:
        """Scrape data from the posts json"""
        self.data = PostJSON()
        self.data.parse_full(json_data)
        self._load_json_into_namespace(self.data)

    def scrape_hashtags(self, session=requests.Session(), status_output=False):
        """Load hashtags used in post as Hashtag objects"""
        self.hashtag_objects = []
        for tag in self.hashtags:
            if status_output:
                print(f"Loading {tag}")
            tag_obj = Hashtag.from_hashtag(tag)
            tag_obj.static_load(session=session)

    @classmethod
    def from_shortcode(cls, shortcode: str) -> Post:
        """
        Factory method for convenience to create Post instance given
        just a shortcode instead of a full URL.

        Parameters
        ----------
        shortcode : str
            Shortcode of the Post for scraping

        Returns
        -------
        Post(url)
            Instance of Post with URL at the given shortcode

        Example
        -------
        >>>Post.from_shortcode('CFcSLyBgseW')
        <https://www.instagram.com/p/CFcSLyBgseW/: Post>
        """
        url = f"https://www.instagram.com/p/{shortcode}/"
        return cls(url, name=shortcode)


class PostJSON(json_scraper.JSONScraper):
    """
    Tool for parsing data from an Instagram post JSON data

    Attributes
    ----------
    json_dict : dict
        Python dictionary containing the Instagram JSON data
    name : str, optional
        Custom name that will represent this JSON data

    Methods
    -------
    parse_json() -> None
        Parses the JSON data regarding a single Instagram post
    load_value(data_dict: dict, key: str, fail_return: Any=None)
        Returns value in dictionary at the specified key. If value doesn't
        exist, returns a default value
    from_json_string(json_str: str, name: str = None)
        Loads a json string as a dictionary and returns a JSONData object with
        that dictionary.
    from_json_file(json_fpath: str, name: str = None)
        Loads a json file at a given JSON filepath into a dictionary and
        returns a JSONData object with that dictionary
    """

    def parse_full(self, window_dict: dict, missing: Any = "ERROR", exception: bool = True) -> None:
        """Parse .json data from window"""
        self.json_dict = window_dict
        self.parse_base(window_dict, missing, exception)
        post_dict = window_dict["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]
        self.parse_partial(post_dict, missing, exception)

        self.scrape_timestamp = datetime.datetime.now()

    def parse_partial(self, post_dict: dict, missing: Any = "ERROR", exception: bool = True) -> None:
        self.upload_date = datetime.datetime.fromtimestamp(
            self.load_value(post_dict, "taken_at_timestamp", missing, exception)
        )
        self.accessibility_caption = self.load_value(
            post_dict, "accessibility_caption")
        self.likes = self.load_value(
            post_dict["edge_media_preview_like"], "count")
        self.amount_of_comments = self.load_value(
            post_dict["edge_media_preview_comment"], "count"
        )
        self.caption_is_edited = self.load_value(
            post_dict, "caption_is_edited")
        self.has_ranked_comments = self.load_value(
            post_dict, "has_ranked_comments")
        self.location = self.load_value(post_dict, "location")
        self.is_ad = self.load_value(post_dict, "is_ad")
        self.viewer_can_reshare = self.load_value(
            post_dict, "viewer_can_reshare")
        self.shortcode = self.load_value(post_dict, "shortcode")
        self.dimensions = self.load_value(post_dict, "dimensions")
        self.is_video = self.load_value(post_dict, "is_video")
        self.fact_check_overall_rating = self.load_value(
            post_dict, "fact_check_overall_rating"
        )
        self.fact_check_information = self.load_value(
            post_dict, "fact_check_information"
        )

        # Get caption and tagged users
        try:
            self.caption = self.load_value(
                post_dict["edge_media_to_caption"]["edges"][0]["node"], "text"
            )
        except IndexError:
            self.caption = ""
        self.tagged_users = self.get_tagged_users()

        # Owner json data
        owner = self.load_value(post_dict, "owner")
        self.is_verified = owner["is_verified"]
        self.profile_pic_url = owner["profile_pic_url"]
        self.username = owner["username"]
        self.blocked_by_viewer = owner["blocked_by_viewer"]
        self.followed_by_viewer = owner["followed_by_viewer"]
        self.full_name = owner["full_name"]
        self.has_blocked_viewer = owner["has_blocked_viewer"]
        self.is_private = owner["is_private"]

        self.scrape_timestamp = datetime.datetime.now()

    def parse_from_profile(self, post_dict, missing: Any = "ERROR", exception: bool = True):
        """Parse the JSON data for a post from a user's profile page"""
        self.id = self.load_value(post_dict, 'id', missing, exception)
        self.shortcode = self.load_value(post_dict, 'shortcode', missing, exception)
        self.dimensions = self.load_value(post_dict, 'dimensions', missing, exception)
        self.display_url = self.load_value(post_dict, 'display_url', missing, exception)
        self.tagged_users = self.load_value(post_dict, 'edge_media_to_tagged_user', missing, exception)
        self.fact_check_overall_rating = self.load_value(post_dict, 'fact_check_overall_rating', missing, exception)
        self.fact_check_information = self.load_value(post_dict, 'fact_check_information', missing, exception)
        self.gating_info = self.load_value(post_dict, 'gating_info', missing, exception)
        self.media_overlay_info = self.load_value(post_dict, 'media_overlay_info', missing, exception)
        self.media_preview = self.load_value(post_dict, 'media_preview', missing, exception)
        self.owner = self.load_value(post_dict, 'owner', missing, exception)
        self.is_video = self.load_value(post_dict, 'is_video', missing, exception)
        self.accessibility_caption = self.load_value(post_dict, 'accessibility_caption', missing, exception)
        self.caption = self.load_value(
            post_dict['edge_media_to_caption']['edges'][0]['node'], 'text', missing, exception)
        self.amount_of_comments = self.load_value(post_dict['edge_media_to_comment'], 'count', missing, exception)
        self.comments_disabled = self.load_value(post_dict, 'comments_disabled', missing, exception)
        self.upload_date = datetime.datetime.fromtimestamp(
            self.load_value(post_dict, "taken_at_timestamp",
                            missing, exception)
        )
        self.edge_liked_by = self.load_value(post_dict, 'edge_liked_by', missing, exception)
        self.likes = self.load_value(post_dict['edge_media_preview_like'], 'count', missing, exception)
        self.location = self.load_value(post_dict, 'location', missing, exception)
        self.thumbnail_src = self.load_value(post_dict, 'thumbnail_src', missing, exception)
        self.thumbnail_resources = self.load_value(post_dict, 'thumbnail_resources', missing, exception)

        self.scrape_timestamp = datetime.datetime.now()

    def get_tagged_users(self) -> List[str]:
        """
        Scrape the usernames of users that have been tagged in the post

        Returns
        -------
        List[str]
            List of strings containing the usernames of tagged users
        """
        tagged_users_json = self.json_dict["entry_data"]["PostPage"][0]["graphql"][
            "shortcode_media"
        ]["edge_media_to_tagged_user"]["edges"]
        return [user["node"]["user"]["username"] for user in tagged_users_json]

if __name__ == "__main__":
    url = r"https://www.instagram.com/p/CFQNno8hSDX/"
    post = Post(url)
    post.static_load()
