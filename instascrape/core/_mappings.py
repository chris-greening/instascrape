from __future__ import annotations

# pylint: disable=used-before-assignment

from collections import deque
from copy import deepcopy
from typing import Dict, List, Union
from abc import ABC

MappingObject = Union[
    "_PostMapping", "_ProfileMapping", "_HashtagMapping", "_LoginMapping"
]


class _GeneralMapping(ABC):
    """
    Maps the user interfacing attribute names with a directive for parsing that
    data point from JSON data

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

    """ """General mappings to the JSON data that are present in all JSON data"""

    mapping = {
        "config": deque(["config", "csrf_token"]),
        "viewer": deque(["config", "viewer"]),
        "country_code": deque(["country_code"]),
        "language_code": deque(["language_code"]),
        "locale": deque(["locale"]),
        "device_id": deque(["device_id"]),
        "browser_push_pub_key": deque(["browser_push_pub_key"]),
        "key_id": deque(["encryption", "key_id"]),
        "public_key": deque(["encryption", "public_key"]),
        "version": deque(["encryption", "version"]),
        "is_dev": deque(["is_dev"]),
        "rollout_hash": deque(["rollout_hash"]),
        "bundle_variant": deque(["bundle_variant"]),
        "frontend_dev": deque(["frontend_env"]),
    }

    @classmethod
    def return_mapping(
        cls, keys: List[str] = [], exclude: List[str] = []
    ) -> Dict[str, deque]:
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
        if not keys:
            keys = list(cls.mapping)
        if exclude:
            keys = [key for key in keys if key not in exclude]
        directive_dict = {key: deepcopy(cls.mapping[key]) for key in keys}
        return directive_dict


class _PostMapping(_GeneralMapping):
    """Mapping specific to Instagram post pages"""

    mapping = _GeneralMapping.return_mapping().copy()
    post_page = ["entry_data", "PostPage", 0]
    post = post_page + ["graphql", "shortcode_media"]
    mapping.update(
        {
            "id": deque(post + ["id"]),
            "shortcode": deque(post + ["shortcode"]),
            "dimensions": deque(post + ["dimensions"]),
            "gating_info": deque(post + ["gating_info"]),
            "fact_check_overall_rating": deque(post + ["fact_check_overall_rating"]),
            "fact_check_information": deque(post + ["fact_check_information"]),
            "sensitivity_friction_info": deque(post + ["sensitivity_friction_info"]),
            "media_overlay_info": deque(post + ["media_overlay_info"]),
            "media_preview": deque(post + ["media_preview"]),
            "display_url": deque(post + ["display_url"]),
            "accessibility_caption": deque(post + ["accessibility_caption"]),
            "is_video": deque(post + ["is_video"]),
            "tracking_token": deque(post + ["tracking_token"]),
            "tagged_users": deque(post + ["edge_media_to_tagged_user"]),
            "caption": deque(
                post + ["edge_media_to_caption", "edges", 0, "node", "text"]
            ),
            "caption_is_edited": deque(post + ["caption_is_edited"]),
            "has_ranked_comments": deque(post + ["has_ranked_comments"]),
            "comments": deque(post + ["edge_media_to_parent_comment", "count"]),
            "comments_disabled": deque(post + ["comments_disabled"]),
            "commenting_disabled_for_viewer": deque(
                post + ["commenting_disabled_for_viewer"]
            ),
            "upload_date": deque(post + ["taken_at_timestamp"]),
            "likes": deque(post + ["edge_media_preview_like", "count"]),
            "location": deque(post + ["location"]),
            "viewer_has_liked": deque(post + ["viewer_has_liked"]),
            "viewer_has_saved": deque(post + ["viewer_has_saved"]),
            "viewer_has_saved_to_collection": deque(
                post + ["viewer_has_saved_to_collection"]
            ),
            "viewer_in_photo_of_you": deque(post + ["viewer_in_photo_of_you"]),
            "viewer_can_reshare": deque(post + ["viewer_can_reshare"]),
        }
    )

    @classmethod
    def post_from_profile_mapping(self):
        return {
            "id": deque(['id']),
            "shortcode": deque(['shortcode']),
            "dimensions": deque(['dimensions']),
            "display_url": deque(['display_url']),
            "tagged_users": deque(['edge_media_to_tagged_user']),
            "fact_check_overall_rating": deque(['fact_check_overall_rating']),
            "fact_check_information": deque(['fact_check_information']),
            "is_video": deque(['is_video']),
            "accessibility_caption": deque(['accessibility_caption']),
            "caption": deque(['edge_media_to_caption', 'edges', 0, 'node', 'text']),
            "comments": deque(['edge_media_to_comment', 'count']),
            "comments_disabled": deque(['comments_disabled']),
            "upload_date": deque(['taken_at_timestamp']),
            "likes": deque(['edge_media_preview_like', 'count']),
            "location": deque(['location'])
        }

class _ProfileMapping(_GeneralMapping):
    """Mapping specific to Instagram profile pages"""

    mapping = _GeneralMapping.return_mapping().copy()
    profile_page = ["entry_data", "ProfilePage", 0]
    user = profile_page + ["graphql", "user"]
    mapping.update(
        {
            "logging_page_id": deque(profile_page + ["logging_page_id"]),
            "show_suggested_profiles": deque(
                profile_page + ["show_suggested_profiles"]
            ),
            "show_follow_dialog": deque(profile_page + ["show_follow_dialog"]),
            "biography": deque(user + ["biography"]),
            "blocked_by_viewer": deque(user + ["blocked_by_viewer"]),
            "business_email": deque(user + ["business_email"]),
            "restricted_by_viewer": deque(user + ["restricted_by_viewer"]),
            "country_block": deque(user + ["country_block"]),
            "external_url": deque(user + ["external_url"]),
            "external_url_linkshimmed": deque(user + ["external_url_linkshimmed"]),
            "followers": deque(user + ["edge_followed_by", "count"]),
            "followed_by_viewer": deque(user + ["followed_by_viewer"]),
            "following": deque(user + ["edge_follow", "count"]),
            "follows_viewer": deque(user + ["follows_viewer"]),
            "full_name": deque(user + ["full_name"]),
            "has_ar_effects": deque(user + ["has_ar_effects"]),
            "has_clips": deque(user + ["has_clips"]),
            "has_guides": deque(user + ["has_guides"]),
            "has_channel": deque(user + ["has_channel"]),
            "has_blocked_viewer": deque(user + ["has_blocked_viewer"]),
            "highlight_reel_count": deque(user + ["highlight_reel_count"]),
            "has_requested_viewer": deque(user + ["has_requested_viewer"]),
            "id": deque(user + ["id"]),
            "is_business_account": deque(user + ["is_business_account"]),
            "is_joined_recently": deque(user + ["is_joined_recently"]),
            "business_category_name": deque(user + ["business_category_name"]),
            "overall_category_name": deque(user + ["overall_category_name"]),
            "category_enum": deque(user + ["category_enum"]),
            "is_private": deque(user + ["is_private"]),
            "is_verified": deque(user + ["is_verified"]),
            "mutual_followers": deque(user + ["edge_mutual_followed_by", "count"]),
            "profile_pic_url": deque(user + ["profile_pic_url"]),
            "profile_pic_url_hd": deque(user + ["profile_pic_url_hd"]),
            "requested_by_viewer": deque(user + ["requested_by_viewer"]),
            "username": deque(user + ["username"]),
            "connected_fb_page": deque(user + ["connected_fb_page"]),
            "posts": deque(user + ["edge_owner_to_timeline_media", "count"]),
        }
    )


class _HashtagMapping(_GeneralMapping):
    """Mapping specific to Instagram hashtag pages"""

    mapping = _GeneralMapping.return_mapping().copy()
    hashtag_page = ["entry_data", "TagPage", 0]
    tag = hashtag_page + ["graphql", "hashtag"]
    mapping.update(
        {
            "id": deque(tag + ["id"]),
            "name": deque(tag + ["name"]),
            "allow_following": deque(tag + ["allow_following"]),
            "is_following": deque(tag + ["is_following"]),
            "is_top_media_only": deque(tag + ["is_top_media_only"]),
            "profile_pic_url": deque(tag + ["profile_pic_url"]),
            "amount_of_posts": deque(tag + ["edge_hashtag_to_media", "count"]),
        }
    )


class _LoginMapping(_GeneralMapping):
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
    }

    @classmethod
    def get_mapper(cls, page_type: str) -> MappingObject:
        return cls.str_to_mapper_obj[page_type]
