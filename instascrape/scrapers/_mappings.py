from collections import deque
from copy import deepcopy

class _GeneralMapping:
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
        return {key: deepcopy(cls.mapping[key]) for key in keys}

class _PostMapping(_GeneralMapping):
    mapping = _GeneralMapping.return_mapping().copy()
    post_page = ['entry_data', 'PostPage', 0]
    post = post_page + ['graphql', 'shortcode_media']
    mapping.update({
        'id': deque(post + ['id']),
        'shortcode': deque(post + ['shortcode']),
        'dimensions': deque(post + ['dimensions']),
        'gating_info': deque(post + ['gating_info']),
        'fact_check_overall_rating': deque(post + ['fact_check_overall_rating']),
        'fact_check_information': deque(post + ['fact_check_information']),
        'sensitivity_friction_info': deque(post + ['sensitivity_friction_info']),
        'media_overlay_info': deque(post + ['media_overlay_info']),
        'media_preview': deque(post + ['media_preview']),
        'display_url': deque(post + ['display_url']),
        'accessibility_caption': deque(post + ['accessibility_caption']),
        'is_video': deque(post + ['is_video']),
        'tracking_token': deque(post + ['tracking_token']),
        'tagged_users': deque(post + ['edge_media_to_tagged_user']),
        'caption': deque(post + ['edge_media_to_caption', 'edges', 0, 'node', 'text']),
        'caption_is_edited': deque(post + ['caption_is_edited']),
        'has_ranked_comments': deque(post + ['has_ranked_comments']),
        'comments': deque(post + ['edge_media_to_parent_comment', 'count']),
        'comments_disabled': deque(post + ['comments_disabled']),
        'commenting_disabled_for_viewer': deque(post + ['commenting_disabled_for_viewer']),
        'taken_at_timestamp': deque(post + ['taken_at_timestamp']),
        'likes': deque(post + ['edge_media_preview_like', 'count']),
        'location': deque(post + ['location']),
        'viewer_has_liked': deque(post + ['viewer_has_liked']),
        'viewer_has_saved': deque(post + ['viewer_has_saved']),
        'viewer_has_saved_to_collection': deque(post + ['viewer_has_saved_to_collection']),
        'viewer_in_photo_of_you': deque(post + ['viewer_in_photo_of_you']),
        'viewer_can_reshare': deque(post + ['viewer_can_reshare']),
    })

class _ProfileMapping(_GeneralMapping):
    mapping = _GeneralMapping.return_mapping().copy()
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

class _HashtagMapping(_GeneralMapping):
    mapping = _GeneralMapping.return_mapping().copy()
    hashtag_page = ['entry_data', 'TagPage', 0]
    tag = hashtag_page + ['graphql', 'hashtag']
    mapping.update({
        'id': deque(tag + ['id']),
        'name': deque(tag + ['name']),
        'allow_following': deque(tag + ['allow_following']),
        'is_following': deque(tag + ['is_following']),
        'is_top_media_only': deque(tag + ['is_top_media_only']),
        'profile_pic_url': deque(tag + ['profile_pic_url']),
        'amount_of_posts': deque(tag + ['edge_hashtag_to_media', 'count']),
    })

class _MetaMapping:
    """Map the page type to the necessary mapping class"""
    mapping = {
        "ProfilePage": _ProfileMapping,
        "TagPage": _HashtagMapping,
        "PostPage": _PostMapping
    }

    @classmethod
    def get_mapper(cls, page_type: str):
        return cls.mapping[page_type]
