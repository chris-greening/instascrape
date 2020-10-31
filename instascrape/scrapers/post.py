"""
Post
----
    Scrape data from a Post page
"""
from __future__ import annotations

import datetime
from typing import List
import re
import shutil
import pathlib
import warnings

import requests

from instascrape.core._mappings import _PostMapping
from instascrape.core._static_scraper import _StaticHtmlScraper
from instascrape.scrapers.json_tools import parse_json_from_mapping
from instascrape.scrapers.comment import Comment

warnings.simplefilter("always", DeprecationWarning)


class Post(_StaticHtmlScraper):
    """
    Scraper for an Instagram post page

    Methods
    -------
    from_shortcode(shortcode: str) -> Post
        Factory method that returns a Post object from a shortcode
    """

    _Mapping = _PostMapping
    SUPPORTED_DOWNLOAD_EXTENSIONS = [".mp3", ".mp4", ".png", ".jpg"]

    def load(self, mapping=None, keys: List[str] = None, exclude: List[str] = None):
        msg = "f{type(self).__name__}.load will be permanently renamed to {type(self).__name__}.scrape, use that method instead for future compatibility"
        warnings.warn(msg, DeprecationWarning)
        self.scrape(mapping, keys, exclude)

    def scrape(self, mapping=None, keys: List[str] = None, exclude: List[str] = None):
        super().scrape(mapping=mapping, keys=keys, exclude=exclude)

        if mapping is None:
            self.upload_date = datetime.datetime.fromtimestamp(self.timestamp)
            self.tagged_users = self._parse_tagged_users(self.json_dict)
            self.hashtags = self._parse_hashtags(self.caption)

    def download(self, fp: str) -> None:
        """
        Download an image or video from a post to your local machine at the given fpath

        Parameters
        ----------
        fp : str
            Filepath to download the image to
        """
        ext = pathlib.Path(fp).suffix
        if ext not in self.SUPPORTED_DOWNLOAD_EXTENSIONS:
            raise NameError(
                f"{ext} is not a supported file extension. Please use {', '.join(self.SUPPORTED_DOWNLOAD_EXTENSIONS)}"
            )
        url = self.video_url if self.is_video else self.display_url

        data = requests.get(url, stream=True)
        if not self.is_video:
            self._download_photo(fp, data)
        else:
            self._download_media(fp, data)

    def get_recent_comments(self):
        list_of_dicts = self.json_dict["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"][
            "edge_media_to_parent_comment"
        ]["edges"]
        comments_arr = [Comment(comment_dict) for comment_dict in list_of_dicts]
        return comments_arr

    @staticmethod
    def _url_from_suburl(suburl):
        return f"https://www.instagram.com/p/{suburl}/"

    def _download_photo(self, fp: str, data):
        with open(fp, 'wb') as outfile:
            data.raw.decode_content = True
            shutil.copyfileobj(data.raw, outfile)

    def _download_media(self, fp: str, data):
        """Write the media to file at given fp from the response"""
        with open(fp, "wb") as outfile:
            for chunk in data.iter_content(chunk_size=1024):
                if chunk:
                    outfile.write(chunk)
                    outfile.flush()

    def _parse_tagged_users(self, json_dict) -> List[str]:
        """Parse the tagged users from JSON dict containing the tagged users"""
        tagged_arr = json_dict["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["edge_media_to_tagged_user"][
            "edges"
        ]
        return [node["node"]["user"]["username"] for node in tagged_arr]

    def _parse_hashtags(self, caption) -> List[str]:
        """Parse the hastags from the post's caption using regex"""
        pattern = r"#(\w+)"
        return re.findall(pattern, caption)

    @classmethod
    def from_shortcode(self, shortcode):
        warnings.warn(
            "This will be deprecated in the near future. You no longer need to use from_shortcode, simply pass shortcode as argument to Post",
            DeprecationWarning,
        )
        return Post(shortcode)
