from __future__ import annotations

from . import static_scraper
from . import json_scraper
from .post_scraper import PostJSON

class ProfileScraper(static_scraper.StaticHTMLScraper):
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
    """

    def _scrape_json(self, json_data: dict):
        """Scrape JSON data and load into instances namespace"""
        self.data = ProfileJSON(json_data)
        self._load_json_into_namespace(self.data)

    def get_recent_posts(self):
    #     self.posts = []
    #     for post_json in self.data.json_dict['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']:
    #         post = PostJSON(json_dict=post_json)
    #         post.parse_json(exception=False)
    #         self.posts.append(post)
        pass

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

    def parse_json(self, *args, **kwargs) -> None:
        # super().parse_json(*args, **kwargs)

        # Convenience definition for prof info
        prof_info = self.json_dict["entry_data"]["ProfilePage"][0]["graphql"]["user"]
        self.biography = prof_info["biography"]
        self.blocked_by_viewer = prof_info["blocked_by_viewer"]
        self.business_email = prof_info["business_email"]
        self.restricted_by_viewer = prof_info["restricted_by_viewer"]
        self.country_block = prof_info["country_block"]
        self.external_url = prof_info["external_url"]
        self.followers = prof_info["edge_followed_by"]["count"]
        self.followed_by_viewer = prof_info["followed_by_viewer"]
        self.following = prof_info["edge_follow"]["count"]
        self.follows_viewer = prof_info["follows_viewer"]
        self.name = prof_info["full_name"]
        self.has_ar_effects = prof_info["has_ar_effects"]
        self.has_clips = prof_info["has_clips"]
        self.has_guides = prof_info["has_guides"]
        self.has_channel = prof_info["has_channel"]
        self.has_blocked_viewer = prof_info["has_blocked_viewer"]
        self.highlight_reel_count = prof_info["highlight_reel_count"]
        self.has_requested_viewer = prof_info["has_requested_viewer"]
        self.id = prof_info["id"]
        self.is_business_account = prof_info["is_business_account"]
        self.is_joined_recently = prof_info["is_joined_recently"]
        self.business_category = prof_info["business_category_name"]
        self.overall_category = prof_info["overall_category_name"]
        self.category_enum = prof_info["category_enum"]
        self.is_private = prof_info["is_private"]
        self.is_verified = prof_info["is_verified"]
        self.mutual_followed_by = prof_info["edge_mutual_followed_by"]["count"]
        self.profile_pic_url = prof_info["profile_pic_url"]
        self.requested_by_viewer = prof_info["requested_by_viewer"]
        self.username = prof_info["username"]
        self.connected_fb_page = prof_info["connected_fb_page"]
        self.amount_of_posts = prof_info["edge_owner_to_timeline_media"]["count"]

if __name__ == "__main__":
    url = r"https://www.instagram.com/chris_greening/"
    profile = ProfileScraper(url)
    profile.static_load()
