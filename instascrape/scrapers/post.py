from __future__ import annotations

import datetime
from typing import List
import re
import shutil

import requests

from instascrape.core._mappings import _PostMapping
from instascrape.core._static_scraper import _StaticHtmlScraper
from instascrape.scrapers.json_tools import parse_json_from_mapping
from instascrape.scrapers.comment import Comment

class Post(_StaticHtmlScraper):
    """
    Scraper for an Instagram post page

    Methods
    -------
    from_shortcode(shortcode: str) -> Post
        Factory method that returns a Post object from a shortcode
    """

    _Mapping = _PostMapping

    def download(self, fp: str) -> None:
        """Download an image from a post to your local machine at the given fpath"""
        img_data = requests.get(self.display_url, stream=True)
        with open(fp, 'wb') as img_file:
            shutil.copyfileobj(img_data.raw, img_file)

    def load(self, keys: List[str] = [], exclude: List[str] = []):
        super().load(keys=keys)
        self.upload_date = datetime.datetime.fromtimestamp(self.upload_date)
        self.tagged_users = self._parse_tagged_users(self.json_dict)
        self.hashtags = self._parse_hashtags(self.caption)

    def to_json(self, fp: str):
        # have to convert to serializable format
        self.upload_date = datetime.datetime.timestamp(self.upload_date)
        super().to_json(fp=fp)
        self.upload_date = datetime.datetime.fromtimestamp(self.upload_date)

    def to_csv(self, fp: str):
        # have to convert to serializable format
        self.upload_date = datetime.datetime.timestamp(self.upload_date)
        super().to_csv(fp=fp)
        self.upload_date = datetime.datetime.fromtimestamp(self.upload_date)

    @classmethod
    def load_from_mapping(self, json_dict, map_dict):
        data_dict = parse_json_from_mapping(json_dict, map_dict)
        post = Post.from_shortcode(data_dict["shortcode"])
        for key, val in data_dict.items():
            setattr(post, key, val)
        # TODO: Bad encapsulation, figure a better way of handling timestamp
        post.upload_date = datetime.datetime.fromtimestamp(post.upload_date)
        return post

    def get_recent_comments(self):
        list_of_dicts = self.json_dict['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_media_to_parent_comment']['edges']
        comments_arr = [Comment(comment_dict) for comment_dict in list_of_dicts]
        return comments_arr

    def _parse_tagged_users(self, json_dict) -> List[str]:
        """Parse the tagged users from JSON dict containing the tagged users"""
        tagged_arr = json_dict['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_media_to_tagged_user']['edges']
        return [node['node']['user']['username'] for node in tagged_arr]

    def _parse_hashtags(self, caption) -> List[str]:
        """Parse the hastags from the post's caption using regex"""
        pattern = r"#(\w+)"
        return re.findall(pattern, caption)

    @classmethod
    def from_shortcode(cls, shortcode: str) -> Post:
        url = f"https://www.instagram.com/p/{shortcode}/"
        return cls(url, name=shortcode)