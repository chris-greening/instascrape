from abc import ABC
from typing import Dict, Union, Any, List
from collections import deque

JSONDict = Dict[str, Any]

class GeneralMapping:
    """General mappings to the JSON data that are present in all JSON data"""
    mapping = {
        'config': deque(['config', 'csrf_token']),
        'viewer': deque(['config', 'viewer']),
        'country_code': deque(['country_code']),
        'language_code': deque(['language_code']),
        'locale': deque(['locale']),
        'device_id': deque(['device_id']),
        'browser_push_pub_key': deque(['browser_push_pub_key']),
        'key_id': deque(['encryption', 'key_id']),
        'public_key': deque(['encryption', 'public_key']),
        'version': deque(['encryption', 'version']),
        'is_dev': deque(['is_dev']),
        'rollout_hash': deque(['rollout_hash']),
        'bundle_variant': deque(['bundle_variant']),
        'frontend_dev': deque(['frontend_env'])
    }

    @classmethod
    def return_mapping(cls, keys=[]):
        if not keys:
            keys = list(cls.mapping)
        return {key: cls.mapping[key] for key in keys}

class ProfileMapping(GeneralMapping):
    mapping = GeneralMapping.return_mapping().copy()
    profile_page = ['entry_data', 'ProfilePage', 0]
    user = profile_page + ['graphql', 'user']
    mapping.update({
        'logging_page_id': deque(profile_page + ['logging_page_id']),
        'show_suggested_profiles': deque(profile_page + ['show_suggested_profiles']),
        'show_follow_dialog': deque(profile_page + ['show_follow_dialog']),
        'biography': deque(user + ['biography']),
        'blocked_by_viewer': deque(user + ['blocked_by_viewer']),
        'business_email': deque(user + ['business_email']),
        'restricted_by_viewer': deque(user + ['restricted_by_viewer']),
        'country_block': deque(user + ['country_block']),
        'external_url': deque(user + ['external_url']),
        'external_url_linkshimmed': deque(user + ['external_url_linkshimmed']),
        'followers': deque(user + ['edge_followed_by', 'count']),
        'followed_by_viewer': deque(user + ['followed_by_viewer']),
        'following': deque(user + ['edge_follow', 'count']),
        'follows_viewer': deque(user + ['follows_viewer']),
        'full_name': deque(user + ['full_name']),
        'has_ar_effects': deque(user + ['has_ar_effects']),
        'has_clips': deque(user + ['has_clips']),
        'has_guides': deque(user + ['has_guides']),
        'has_channel': deque(user + ['has_channel']),
        'has_blocked_viewer': deque(user + ['has_blocked_viewer']),
        'highlight_reel_count': deque(user + ['highlight_reel_count']),
        'has_requested_viewer': deque(user + ['has_requested_viewer']),
        'id': deque(user + ['id']),
        'is_business_account': deque(user + ['is_business_account']),
        'is_joined_recently': deque(user + ['is_joined_recently']),
        'business_category_name': deque(user + ['business_category_name']),
        'overall_category_name': deque(user + ['overall_category_name']),
        'category_enum': deque(user + ['category_enum']),
        'is_private': deque(user + ['is_private']),
        'is_verified': deque(user + ['is_verified']),
        'mutual_followers': deque(user + ['edge_mutual_followed_by', 'count']),
        'profile_pic_url': deque(user + ['profile_pic_url']),
        'profile_pic_url_hd': deque(user + ['profile_pic_url_hd']),
        'requested_by_viewer': deque(user + ['requested_by_viewer']),
        'username': deque(user + ['username']),
        'connected_fb_page': deque(user + ['connected_fb_page']),
        'posts': deque(user + ['edge_owner_to_timeline_media', 'count']),
    })

class JsonEngine:
    """
    Generalized version of the JSONScraper classes that will act more as a backend engine that
    the user doesn't have to ever worry about or think of
    """

    DEFAULT_VAL = float('nan')

    def __init__(self, json_data: JSONDict, map_dict: Dict[str, deque]) -> None:
        self.json_data = json_data
        self.map_dict = map_dict

        self._fill_default_values()

    def _fill_default_values(self):
        """Loop through each key in map_dict and set value given a list of directives"""
        for key in self.map_dict:
            self._set_value(key, self.json_data, self.map_dict[key])

    def _set_value(self, orig_key: str, container: dict, directive_queue: deque):
        """Recursively set each value from the mapping"""
        current_key = directive_queue.popleft()
        value = container[current_key]
        if len(directive_queue) == 0:
            setattr(self, orig_key, value)
        else:
            self._set_value(orig_key, value, directive_queue)

if __name__ == '__main__':
    from instascrape import json_from_url

    json_dict = json_from_url('https://www.instagram.com/chris_greening')
    data = JsonEngine(json_dict, ProfileMapping.return_mapping())
