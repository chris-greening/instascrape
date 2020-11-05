from __future__ import annotations

from instascrape.scrapers import Profile, Post, Hashtag


class InstaScrape:
    """
    Quick and clean interface for tying in much of instascrape's functionality
    in easy and clean syntax
    """

    def scrape_profile(self, username: str) -> Profile:
        """
        Load, scrape, and return a Profile object that contains all of the
        availably scraped data from a given profile

        Parameters
        ----------
        username : str
            Username of the profile to be scraped

        Returns
        -------
        profile : Profile
            Profile object with the scraped data
        """
        profile = Profile(username)
        profile.scrape()
        return profile

    def scrape_post(self, url: str) -> Post:
        """
        Load, scrape, and return a Post object that contains all of the
        availably scraped data from a given post

        Parameters
        ----------
        url : str
            Full URL of the post to be scraped

        Returns
        -------
        post : Post
            Post object with the scraped data
        """
        post = Post(url)
        post.scrape()
        return post

    def scrape_hashtag(self, hashtag: str) -> Hashtag:
        """
        Load, scrape, and return a Hashtag object that contains all of the
        availably scraped data from a given hashtag

        Parameters
        ----------
        hashtag : str
            Name of the hashtag to be scraped

        Returns
        -------
        hashtag : Hashtag
            Hashtag object with the scraped data
        """
        hashtag = Hashtag(hashtag)
        hashtag.scrape()
        return hashtag

    def download_post(self, url: str, fp: str) -> None:
        """Download post at the given url to local machine at given fp"""
        post = Post(url)
        post.scrape()
        post.download(fp)
