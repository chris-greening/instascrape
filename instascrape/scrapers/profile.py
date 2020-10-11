from __future__ import annotations

from typing import Any

from instascrape.scrapers import static_scraper
from instascrape.scrapers import json_scraper
from instascrape.scrapers import PostJSON

class Profile(static_scraper.StaticHTMLScraper):
    """
    Scraper for a profile page.

    Attribues
    ---------
    url : str
        Full URL to an existing Instagram profile

    Methods
    -------
    static_load(session=requests.Session())
        Makes request to URL, instantiates BeautifulSoup, finds JSON data,
        then parses JSON data.
    get_recent_posts()
        Scrape the most recent 12 posts from the profile into PostJSON objects
    """

    def _scrape_json(self, json_dict: dict):
        """Scrape the JSON"""
        super()._scrape_json(json_dict)

    def get_recent_posts(self):
        """Get data from the 12 most recent posts"""
        self.posts = []
        for post_json in self.data.json_dict['entry_data']['ProfilePage'][0][
            'graphql']['user']['edge_owner_to_timeline_media']['edges']:
            post = PostJSON()
            post.parse_from_profile(post_json['node'], exception=False)
            self.posts.append(post)

    @classmethod
    def from_username(cls, username: str):
        """
        Factory method for convenience to create Profile instance given
        just a username instead of a full URL.

        Parameters
        ----------
        username : str
            Username of the Profile for scraping

        Returns
        -------
        Profile(url)
            Instance of Profile with URL at the given username

        Example
        -------
        >>>Profile.from_username('gvanrossum')
        <https://www.instagram.com/gvanrossum/: Profile>
        """

        url = f"https://www.instagram.com/{username}/"
        return cls(url, name=username)


class ProfileJSON(json_scraper.JSONScraper):
    """
    Tool for parsing data from Instagram profile JSON data

    json_dict : dict
        Python dictionary containing the Instagram JSON data
    name : str, optional
        Custom name that will represent this JSON data

    Methods
    -------
    parse_json() -> None
        Parses the JSON data regarding a single Instagram profile
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

    def parse_full(self, window_dict: dict, missing: Any="ERROR", exception: bool=True) -> None:
        """Parse .json data from window"""
        self.json_dict = window_dict
        self.parse_base(window_dict, missing, exception)
        prof_info = window_dict["entry_data"]["ProfilePage"][0]["graphql"]["user"]
        self.parse_partial(prof_info, missing, exception)

    def parse_partial(self, prof_dict, missing: Any="ERROR", exception: bool=True) -> None:
        # Convenience definition for prof info
        self.biography = prof_dict["biography"]
        self.blocked_by_viewer = prof_dict["blocked_by_viewer"]
        self.business_email = prof_dict["business_email"]
        self.restricted_by_viewer = prof_dict["restricted_by_viewer"]
        self.country_block = prof_dict["country_block"]
        self.external_url = prof_dict["external_url"]
        self.followers = prof_dict["edge_followed_by"]["count"]
        self.followed_by_viewer = prof_dict["followed_by_viewer"]
        self.following = prof_dict["edge_follow"]["count"]
        self.follows_viewer = prof_dict["follows_viewer"]
        self.name = prof_dict["full_name"]
        self.has_ar_effects = prof_dict["has_ar_effects"]
        self.has_clips = prof_dict["has_clips"]
        self.has_guides = prof_dict["has_guides"]
        self.has_channel = prof_dict["has_channel"]
        self.has_blocked_viewer = prof_dict["has_blocked_viewer"]
        self.highlight_reel_count = prof_dict["highlight_reel_count"]
        self.has_requested_viewer = prof_dict["has_requested_viewer"]
        self.id = prof_dict["id"]
        self.is_business_account = prof_dict["is_business_account"]
        self.is_joined_recently = prof_dict["is_joined_recently"]
        self.business_category = prof_dict["business_category_name"]
        self.overall_category = prof_dict["overall_category_name"]
        self.category_enum = prof_dict["category_enum"]
        self.is_private = prof_dict["is_private"]
        self.is_verified = prof_dict["is_verified"]
        self.mutual_followed_by = prof_dict["edge_mutual_followed_by"]["count"]
        self.profile_pic_url = prof_dict["profile_pic_url"]
        self.requested_by_viewer = prof_dict["requested_by_viewer"]
        self.username = prof_dict["username"]
        self.connected_fb_page = prof_dict["connected_fb_page"]
        self.amount_of_posts = prof_dict["edge_owner_to_timeline_media"]["count"]


Profile.set_associated_json(ProfileJSON)

if __name__ == "__main__":
    url = r"https://www.instagram.com/chris_greening/"
    profile = Profile(url)
    profile.static_load()
