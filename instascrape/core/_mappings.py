"""
Mappings that tell the _JsonEngine the user facing attribute names and the
steps needed to get there in a JSON dictionary
"""

from __future__ import annotations

from abc import ABC
from collections import deque
from copy import deepcopy
from typing import Dict, List, Union

# pylint: disable=used-before-assignment


MappingObject = Union["_PostMapping", "_ProfileMapping", "_HashtagMapping", "_LoginMapping"]


class _GeneralMapping(ABC):
    """
    Maps the user interfacing attribute names with their keys as given in a JSON
    dict that has been flattened using
    instascrape.core._json_flattener.JsonFlattener

    Attributes
    ----------
    mapping : Dict[str, deque]
        Each key: val pair represents one data point and the directive for
        traversing a JSON dict and accessing that value

    Methods
    -------
    return_mapping(keys: List[str]=[]) -> Dict[str, deque]
        Interface for returning only mapping directives that are specified in
        a list of keys

    """

    mapping = {
        # "csrf_token": deque(["csrf_token"]),
        # "viewer_id": deque(["viewerId"]),
        # "country_code": deque(["country_code"]),
        # "language_code": deque(["language_code"]),
        # "locale": deque(["locale"]),
        # "device_id": deque(["device_id"]),
        # "browser_push_pub_key": deque(["browser_push_pub_key"]),
        # "key_id": deque(["key_id"]),
        # "public_key": deque(["public_key"]),
        # "version": deque(["version"]),
        # "is_dev": deque(["is_dev"]),
        # "rollout_hash": deque(["rollout_hash"]),
        # "bundle_variant": deque(["bundle_variant"]),
        # "frontend_dev": deque(["frontend_env"]),
    }

    @classmethod
    def return_mapping(cls, keys: List[str] = None, exclude: List[str] = None) -> Dict[str, deque]:
        """
        Return key-directive pairs specified by key names. If no keys are
        specified, return all

        Parameters
        ----------
        keys : List[str]
            Keys that specify what directives to return

        Returns
        -------
        directive_dict : Dict[str, deque]
            Dictionary of keys and their directives
        """
        if keys is None:
            keys = []
        if exclude is None:
            exclude = []
        if isinstance(keys, str):
            keys = [keys]
        if isinstance(exclude, str):
            exclude = [exclude]

        if not keys:
            keys = list(cls.mapping)
        if exclude:
            keys = [key for key in keys if key not in exclude]
        directive_dict = {key: deepcopy(cls.mapping[key]) for key in keys}
        return directive_dict


class _PostMapping(_GeneralMapping):
    """Mapping specific to Instagram post pages"""

    mapping = _GeneralMapping.return_mapping().copy()
    mapping.update(
        {
            "id": deque(["id"]),
            "shortcode": deque(["shortcode"]),
            "height": deque(["height"]),
            "width": deque(["width"]),
            "gating_info": deque(["gating_info"]),
            "fact_check_overall_rating": deque(["fact_check_overall_rating"]),
            "fact_check_information": deque(["fact_check_information"]),
            "sensitivity_friction_info": deque(["sensitivity_friction_info"]),
            "media_overlay_info": deque(["media_overlay_info"]),
            "media_preview": deque(["media_preview"]),
            "display_url": deque(["display_url"]),
            "accessibility_caption": deque(["accessibility_caption"]),
            "is_video": deque(["is_video"]),
            "tracking_token": deque(["tracking_token"]),
            "tagged_users": deque(["edge_media_to_tagged_user"]),
            "caption": deque(["text"]),
            "caption_is_edited": deque(["caption_is_edited"]),
            "has_ranked_comments": deque(["has_ranked_comments"]),
            "comments": deque(["count"]),
            "comments_disabled": deque(["comments_disabled"]),
            "commenting_disabled_for_viewer": deque(["commenting_disabled_for_viewer"]),
            "timestamp": deque(["taken_at_timestamp"]),
            "likes": deque(["edge_media_preview_like_count"]),
            "location": deque(["name"]),
            "viewer_has_liked": deque(["viewer_has_liked"]),
            "viewer_has_saved": deque(["viewer_has_saved"]),
            "viewer_has_saved_to_collection": deque(["viewer_has_saved_to_collection"]),
            "viewer_in_photo_of_you": deque(["viewer_in_photo_of_you"]),
            "viewer_can_reshare": deque(["viewer_can_reshare"]),
            "video_url": deque(["video_url"]),
            "has_audio": deque(["has_audio"]),
            "video_view_count": deque(["video_view_count"]),
            "username": deque(["shortcode_media_owner_username"]),
            "full_name": deque(['owner_full_name']),
        }
    )

    @classmethod
    def post_from_profile_mapping(cls):
        """
        Return the mapping needed for parsing a post's JSON data from the JSON
        served back after requesting a Profile page.
        """
        return {
            "id": deque(["id"]),
            "shortcode": deque(["shortcode"]),
            "dimensions": deque(["dimensions"]),
            "display_url": deque(["display_url"]),
            "tagged_users": deque(["edge_media_to_tagged_user", "edges"]),
            "fact_check_overall_rating": deque(["fact_check_overall_rating"]),
            "fact_check_information": deque(["fact_check_information"]),
            "is_video": deque(["is_video"]),
            "accessibility_caption": deque(["accessibility_caption"]),
            "caption": deque(["edge_media_to_caption", "edges", 0, "node", "text"]),
            "comments": deque(["count"]),
            "comments_disabled": deque(["comments_disabled"]),
            "timestamp": deque(["taken_at_timestamp"]),
            "likes": deque(["edge_media_preview_like_count"]),
            "location": deque(["location"]),
        }

    @classmethod
    def post_from_hashtag_mapping(cls):
        """
        Return the mapping needed for parsing a post's JSON data from the JSON
        served back after requesting a Hashtag page.
        """
        return {
            "comments_disabled": deque(["comments_disabled"]),
            "id": deque(["id"]),
            "caption": deque(["edge_media_to_caption", "edges", 0, "node", "text"]),
            "shortcode": deque(["shortcode"]),
            "comments": deque(["edge_media_to_comment", "count"]),
            "upload_date": deque(["taken_at_timestamp"]),
            "dimensions": deque(["dimensions"]),
            "display_url": deque(["display_url"]),
            "likes": deque(["edge_media_preview_like", "count"]),
            "owner": deque(["owner", "id"]),
            "is_video": deque(["is_video"]),
            "accessibility_caption": deque(["accessibility_caption"]),
        }


class _ReelMapping(_PostMapping):
    mapping = _PostMapping.return_mapping().copy()
    mapping.update(
        {
            "video_play_count": deque(["video_play_count"]),
        }
    )


class _IGTVMapping(_PostMapping):
    mapping = _PostMapping.return_mapping().copy()


class _ProfileMapping(_GeneralMapping):
    """Mapping specific to Instagram profile pages"""

    mapping = _GeneralMapping.return_mapping().copy()
    mapping.update(
        {
            "logging_page_id": deque(["logging_page_id"]),
            "show_suggested_profiles": deque(["show_suggested_profiles"]),
            "show_follow_dialog": deque(["show_follow_dialog"]),
            "biography": deque(["biography"]),
            "blocked_by_viewer": deque(["blocked_by_viewer"]),
            "restricted_by_viewer": deque(["restricted_by_viewer"]),
            "country_block": deque(["country_block"]),
            "external_url": deque(["external_url"]),
            "external_url_linkshimmed": deque(["external_url_linkshimmed"]),
            "followers": deque(["count"]),
            "followed_by_viewer": deque(["followed_by_viewer"]),
            "following": deque(["edge_follow_count"]),
            "follows_viewer": deque(["follows_viewer"]),
            "full_name": deque(["user_full_name"]),
            "has_ar_effects": deque(["has_ar_effects"]),
            "has_clips": deque(["has_clips"]),
            "has_guides": deque(["has_guides"]),
            "has_channel": deque(["has_channel"]),
            "has_blocked_viewer": deque(["has_blocked_viewer"]),
            "highlight_reel_count": deque(["highlight_reel_count"]),
            "has_requested_viewer": deque(["has_requested_viewer"]),
            "id": deque(["id"]),
            "is_business_account": deque(["is_business_account"]),
            "is_joined_recently": deque(["is_joined_recently"]),
            "business_category_name": deque(["business_category_name"]),
            "overall_category_name": deque(["overall_category_name"]),
            "category_enum": deque(["category_enum"]),
            "is_private": deque(["is_private"]),
            "is_verified": deque(["is_verified"]),
            "mutual_followers": deque(["edge_mutual_followed_by_count"]),
            "profile_pic_url": deque(["profile_pic_url"]),
            "profile_pic_url_hd": deque(["profile_pic_url_hd"]),
            "requested_by_viewer": deque(["requested_by_viewer"]),
            "username": deque(["user_username"]),
            "connected_fb_page": deque(["connected_fb_page"]),
            "posts": deque(["edge_owner_to_timeline_media_count"]),
        }
    )


class _HashtagMapping(_GeneralMapping):
    """Mapping specific to Instagram hashtag pages"""

    mapping = _GeneralMapping.return_mapping().copy()
    mapping.update(
        {
            "id": deque(["id"]),
            "name": deque(["name"]),
            "allow_following": deque(["allow_following"]),
            "is_following": deque(["is_following"]),
            "is_top_media_only": deque(["is_top_media_only"]),
            "profile_pic_url": deque(["profile_pic_url"]),
            "amount_of_posts": deque(["count"]),
        }
    )


class _LocationMapping(_GeneralMapping):
    """Mapping specific to Instagram profile pages"""

    mapping = _GeneralMapping.return_mapping().copy()
    mapping.update(
        {
            "id": deque(["id"]),
            "name": deque(["name"]),
            "has_public_page": deque(["has_public_page"]),
            "latitude": deque(["lat"]),
            "longitude": deque(["lng"]),
            "slug": deque(["slug"]),
            "blurb": deque(["blurb"]),
            "website": deque(["website"]),
            "phone": deque(["phone"]),
            "primary_alias_on_fb": deque(["primary_alias_on_fb"]),
            "stress_address": deque(["street_address"]),
            "zip_code": deque(["zip_code"]),
            "city_name": deque(["city_name"]),
            "region_name": deque(["region_name"]),
            "country_code": deque(["country_code"]),
            "amount_of_posts": deque(["count"]),
        }
    )


class _LoginMapping(_GeneralMapping):
    """Mapping specific to Instagram login page"""

    mapping = _GeneralMapping.return_mapping().copy()


class _HttpErrorMapping(_GeneralMapping):
    """Mapping specific to Instagram login page"""

    mapping = _GeneralMapping.return_mapping().copy()


class _MetaMapping:
    """
    Map the string in the Instagram JSON that indicates the type of page the
    JSON was scraped from

    Attributes
    ----------
    str_to_mapper_obj : Dict[str, Any]
        Dictionary that maps the string name of the JSON type to the specific
        mapping object

    Methods
    -------
    get_mapper(page_type: str)
        Return the mapping object that correlates to the string
    """

    str_to_mapper_obj = {
        "ProfilePage": _ProfileMapping,
        "TagPage": _HashtagMapping,
        "PostPage": _PostMapping,
        "LoginAndSignupPage": _LoginMapping,
        "LocationsPage": _LocationMapping
    }

    @classmethod
    def get_mapper(cls, page_type: str) -> MappingObject:
        """
        Return the appropriate mapper that corresponds to the page_type as
        given in the requested Instagram JSON data
        """
        return cls.str_to_mapper_obj[page_type]
