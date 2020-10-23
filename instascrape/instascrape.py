from __future__ import annotations

from instascrape.scrapers import *


class InstaScrape:
    def load_profile(self, username: str) -> Profile:
        profile = Profile.from_username(username)
        profile.load()
        return profile

    def load_post(self, url: str) -> Post:
        post = Post(url)
        post.load()
        return post

    def load_hashtag(self, hashtag: str) -> Hashtag:
        hashtag = Hashtag.from_hashtag(hashtag)
        hashtag.load()
        return hashtag
