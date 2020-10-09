from __future__ import annotations

import datetime
from typing import List

import requests

from . import static_scraper
from . import json_scraper
from .hashtag_scraper import HashtagScraper

class PostScraper(static_scraper.StaticHTMLScraper):
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
        self.data = PostJSON(json_data)
        self._load_json_into_namespace(self.data)

    def scrape_hashtags(self, session=requests.Session(), status_output=False):
        """Load hashtags used in post as Hashtag objects"""
        self.hashtag_objects = []
        for tag in self.hashtags:
            if status_output:
                print(f"Loading {tag}")
            tag_obj = HashtagScraper.from_hashtag(tag)
            tag_obj.static_load(session=session)

    @classmethod
    def from_shortcode(cls, shortcode: str) -> PostScraper:
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

    def parse_json(self, *args, **kwargs) -> None:
        # super().parse_json(*args, **kwargs)

        # Convenience definition for post info
        try:
            post_info = self.json_dict["entry_data"]["PostPage"][0]["graphql"][
                "shortcode_media"
            ]
        except KeyError:
            post_info = self.json_dict
        self.upload_date = datetime.datetime.fromtimestamp(
            self.load_value(post_info, "taken_at_timestamp")
        )
        self.accessibility_caption = self.load_value(
            post_info, "accessibility_caption")
        self.likes = self.load_value(
            post_info["edge_media_preview_like"], "count")
        self.amount_of_comments = self.load_value(
            post_info["edge_media_preview_comment"], "count"
        )
        self.caption_is_edited = self.load_value(
            post_info, "caption_is_edited")
        self.has_ranked_comments = self.load_value(
            post_info, "has_ranked_comments")
        self.location = self.load_value(post_info, "location")
        self.is_ad = self.load_value(post_info, "is_ad")
        self.viewer_can_reshare = self.load_value(
            post_info, "viewer_can_reshare")
        self.shortcode = self.load_value(post_info, "shortcode")
        self.dimensions = self.load_value(post_info, "dimensions")
        self.is_video = self.load_value(post_info, "is_video")
        self.fact_check_overall_rating = self.load_value(
            post_info, "fact_check_overall_rating"
        )
        self.fact_check_information = self.load_value(
            post_info, "fact_check_information"
        )

        # Get caption and tagged users
        try:
            self.caption = self.load_value(
                post_info["edge_media_to_caption"]["edges"][0]["node"], "text"
            )
        except IndexError:
            self.caption = ""
        self.tagged_users = self.get_tagged_users()

        # Owner json data
        owner = self.load_value(post_info, "owner")
        self.is_verified = owner["is_verified"]
        self.profile_pic_url = owner["profile_pic_url"]
        self.username = owner["username"]
        self.blocked_by_viewer = owner["blocked_by_viewer"]
        self.followed_by_viewer = owner["followed_by_viewer"]
        self.full_name = owner["full_name"]
        self.has_blocked_viewer = owner["has_blocked_viewer"]
        self.is_private = owner["is_private"]

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
    post = PostScraper(url)
    post.static_load()
