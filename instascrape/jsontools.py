import json
from abc import ABC, abstractmethod
import datetime

from typing import List, Any

class JSONScraper(ABC):
    """
    Abstract base class containing methods for handling and parsing Instagram 
    JSON data 

    Attributes 
    ----------
    json_dict : dict
        Python dictionary containing the Instagram JSON data
    name : str, optional 
        Custom name that will represent this JSON data

    Methods 
    -------
    parse_json() -> None
        Parses JSON data that every Instagram type has
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

    _METADATA_KEYS = ['json_dict', 'name']

    def __init__(self, json_dict: dict, name: str = None) -> None:
        """Container for storing all scraped data from Instagram JSON"""
        self.json_dict = json_dict
        if name is not None:
            self.name = name

    def parse_json(self) -> None:
        """Parse JSON object"""
        config = self.json_dict['config']
        self.csrf_token = self.load_value(config, 'csrf_token')

        self.country_code = self.load_value(self.json_dict, "country_code")
        self.language_code = self.load_value(self.json_dict, "language_code")
        self.locale = self.load_value(self.json_dict, "locale")

        self.hostname = self.load_value(self.json_dict, 'hostname')
        self.is_whitelisted_crawl_bot = self.load_value(
            self.json_dict, 'is_whitelisted_crawl_bot')
        self.connection_quality_rating = self.load_value(
            self.json_dict, 'connection_quality_rating')
        self.platform = self.load_value(self.json_dict, 'platform')

        self.device_id = self.load_value(self.json_dict, 'device_id')
        self.encryption = self.load_value(self.json_dict, 'encryption')

        self.rollout_hash = self.load_value(self.json_dict, 'rollout_hash')

    @property
    def scraped_attr(self) -> List[str]:
        """Return list of names of attributes that have been scraped from the JSON"""
        return [attr for attr in self.__dict__ if attr not in JSONScraper._METADATA_KEYS]

    def to_dict(self) -> dict:
        """Return a dictionary containing all of the data that has been scraped"""
        return {key: val for key, val in self.__dict__.items() if key not in JSONScraper._METADATA_KEYS}

    def __repr__(self) -> str:
        class_name = type(self).__name__
        output_str = "<{}: " + f"{class_name}>"
        if hasattr(self, "name"):
            return output_str.format(self.name)
        return output_str.format("unnamed")

    def load_value(self, data_dict: dict, key: str, fail_default: Any = None) -> Any:
        """
        Returns the value of a dictionary at a given key, returning a specified 
        value if the key does not exsit.

        Parameters
        ----------
        data_dict : dict 
            Dictionary of key: val pairs that you want to look for 
        key : str 
            Key in dictionary to search for 
        fail_return : Any, optional 

        Returns 
        -------
        return_val : Any 
            Value or default return of the dictionary lookup
        """
        try: 
            return_val = data_dict[key]
        except KeyError: 
            return_val = fail_default
        return return_val

    @classmethod
    def from_json_string(cls, json_string: str, name: str = None):
        """
        Factory method for returning a JSONData object given a string 
        representation of JSON data. 

        Parameters
        ----------
        json_string : str 
            String representation of the JSON data for loading into dict 
        name : str, optional  
            Optional name of the JSON data 
        
        Returns 
        -------
        JSONData : JSONData
            JSONData  object containing the JSON data loaded from string as a dictionary 

        """
        return cls(json.loads(json_string), name)

    @classmethod
    def from_json_file(cls, json_fpath: str, name: str = None):
        """
        Factory method for returning a JSONData object given a filepath 
        to a .json file that contains valid JSON data. 

        Parameters
        ----------
        json_fpath : str 
            Filepath to the .json file
        name : str, optional  
            Optional name of the JSON data 
        
        Returns 
        -------
        JSONData : JSONData
            JSONData object containing the JSON data loaded from file as a dictionary 

        """
        with open(json_fpath, 'r') as infile:
            json_data = json.load(infile)
        return cls(json_data, name)

class ProfileJSON(JSONScraper):
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
    def parse_json(self) -> None:
        """Parse profile JSON data"""
        super().parse_json()

        # Convenience definition for prof info
        prof_info = self.json_dict["entry_data"]["ProfilePage"][0]["graphql"][
            "user"
        ]
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
        self.posts = prof_info["edge_owner_to_timeline_media"]["count"]

class HashtagJSON(JSONScraper):
    """
    Tool for parsing data fron Instagram hashtag JSON data

    Attributes 
    ----------
    json_dict : dict
        Python dictionary containing the Instagram JSON data
    name : str, optional 
        Custom name that will represent this JSON data

    Methods 
    -------
    parse_json() -> None
        Parses the JSON data regarding a single Instagram hashtag 
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
    def parse_json(self) -> None:
        super().parse_json()

        tag_data = self.json_dict["entry_data"]["TagPage"][0]["graphql"]["hashtag"]
        self.id = tag_data["id"]
        self.name = tag_data["name"]
        self.allow_following = tag_data["allow_following"]
        self.is_following = tag_data["is_following"]
        self.is_top_media_only = tag_data["is_top_media_only"]
        self.profile_pic_url = tag_data["profile_pic_url"]
        self.amount_of_posts = tag_data["edge_hashtag_to_media"]["count"]

class PostJSON(JSONScraper):
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
    def parse_json(self) -> None:
        super().parse_json()

        # Convenience definition for post info
        post_info = self.json_dict["entry_data"]["PostPage"][0]["graphql"][
            "shortcode_media"
        ]
        self.upload_date = datetime.datetime.fromtimestamp(
            self.load_value(post_info,"taken_at_timestamp")
        )
        self.accessibility_caption = self.load_value(post_info,"accessibility_caption")
        self.likes = self.load_value(post_info["edge_media_preview_like"], "count")
        self.amount_of_comments = self.load_value(post_info["edge_media_preview_comment"], "count")
        self.caption_is_edited = self.load_value(post_info,"caption_is_edited")
        self.has_ranked_comments = self.load_value(post_info,"has_ranked_comments")
        self.location = self.load_value(post_info,"location")
        self.is_ad = self.load_value(post_info,"is_ad")
        self.viewer_can_reshare = self.load_value(post_info,"viewer_can_reshare")
        self.shortcode = self.load_value(post_info,"shortcode")
        self.dimensions = self.load_value(post_info,"dimensions")
        self.is_video = self.load_value(post_info,"is_video")
        self.fact_check_overall_rating = self.load_value(post_info,"fact_check_overall_rating")
        self.fact_check_information = self.load_value(post_info,"fact_check_information")

        # Get caption and tagged users
        try:
            self.caption = self.load_value(post_info["edge_media_to_caption"]["edges"][0]["node"], "text")
        except IndexError:
            self.caption = ""
        self.tagged_users = self.get_tagged_users()

        # Owner json data
        owner = self.load_value(post_info,"owner")
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

class LandingPageJSON(JSONScraper):
    def parse_json(self):
        super().parse_json()

class HttpErrorPageJSON(JSONScraper):
    def parse_json(self):
        super().parse_json()

class LoginAndSignupJSON(JSONScraper):
    def parse_json(self):
        super().parse_json()
