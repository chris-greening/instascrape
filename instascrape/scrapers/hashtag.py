"""
Hashtag
-------
    Scrape data from a Hashtag page
"""
from __future__ import annotations

from typing import List
import time

from instascrape.core._mappings import _HashtagMapping, _PostMapping
from instascrape.core._static_scraper import _StaticHtmlScraper
from instascrape.scrapers.post import Post

from bs4 import BeautifulSoup


class Hashtag(_StaticHtmlScraper):
    """Scraper for an Instagram hashtag page"""

    _Mapping = _HashtagMapping

    def get_recent_posts(self, amt: int = 71) -> List[Post]:
        """
        Return a list of recent posts to the hasthag

        Parameters
        ----------
        amt : int
            Amount of recent posts to return

        Returns
        -------
        posts : List[Post]
            List containing the recent 12 posts and their available data
        """
        posts = []
        post_arr = self.json_dict["entry_data"]["TagPage"][0]["graphql"]["hashtag"]["edge_hashtag_to_media"]["edges"]
        amount_of_posts = len(post_arr)
        if amt > amount_of_posts:
            amt = amount_of_posts
        for post in post_arr[:amt]:
            json_dict = post["node"]
            mapping = _PostMapping.post_from_hashtag_mapping()
            post = Post(json_dict)
            post.scrape(mapping=mapping)
            posts.append(post)
        return posts

    def _url_from_suburl(self, suburl: str) -> str:
        return f"https://www.instagram.com/tags/{suburl}/"
    
    def get_posts(self, webdriver, amount=None, login_first=False, login_pause=60, max_failed_scroll=300, scrape=False, scrape_pause=5):
        """
        Return Post objects from profile scraped using a webdriver (not included)

        Parameters
        ----------
        webdriver : selenium.webdriver.chrome.webdriver.WebDriver
            Selenium webdriver for rendering JavaScript and loading dynamic
            content
        amount : int
            Amount of posts to return, default is all of them
        login_first : bool
            Start on login page to allow user to manually login to Instagram
        login_pause : int
            Length of time in seconds to pause before starting scrape
        max_failed_scroll : int
            Maximum amount of scroll attempts before stopping if scroll is stuck
        scrape : bool
            Scrape posts with the webdriver prior to returning
        scrape_pause : int
            Time in seconds between each scrape

        Returns
        -------
        posts : List[Post]
            Post objects gathered from the profile page
        """

        JS_SCROLL_SCRIPT = "window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;"
        JS_PAGE_LENGTH_SCRIPT = "var lenOfPage=document.body.scrollHeight; return lenOfPage;"

        # Determine how many posts are available on the page
#         try:
#             posts_len = self.posts
#             if amount is None:
#                 amount = posts_len
#             if amount > posts_len:
#                 raise ValueError(f"{amount} posts requested but {self.username} only has {posts_len} posts")
#         except AttributeError:
#             raise AttributeError(f"{type(self)} must be scraped first")
        posts_len = 3225

        # Manual login
        if login_first:
            webdriver.get("https://www.instagram.com")
            time.sleep(login_pause)

        # Get profile page
        webdriver.get(self.url)

        # Continuously scroll, collect HTML, and parse Post objects
        posts = []
        shortcodes = []
        scroll_attempts = 0
        last_position = webdriver.execute_script(JS_PAGE_LENGTH_SCRIPT)
        scrolling = True
        while scrolling:
            current_position = webdriver.execute_script(JS_SCROLL_SCRIPT)
            source_data = webdriver.page_source
            found_posts = self._separate_posts(source_data)

            # Append found posts into total posts
            for post in found_posts:
                if post.source not in shortcodes:
                    shortcodes.append(post.source)
                    posts.append(post)

            # If scroll is stuck and exceeds max allowed attempts, exit loop
            if current_position == last_position:
                scroll_attempts += 1
                if scroll_attempts > max_failed_scroll:
                    scrolling = False
            else:
                scroll_attempts = 0
                last_position = current_position

            current_post_len = len(posts)

            if (current_post_len >= posts_len) or (current_post_len >= amount):
                break

        # Remove excess posts from right of list
        posts = posts[:amount]

        # If scrape arg is True, scrape all posts using webdriver
        scraped_posts = []
        if scrape:
            for post in posts:
                scraped_posts.append(post.scrape(inplace=False, webdriver=webdriver))
                time.sleep(scrape_pause)
            posts = scraped_posts

        return posts
    
    def _separate_posts(self, source_data):
        """Separate the HTML and parse out BeautifulSoup for every post"""
        post_soup = []

        soup = BeautifulSoup(source_data, features="lxml")
        anchor_tags = soup.find_all("a")
        post_tags = [tag for tag in anchor_tags if tag.find(
            "div", {"class": "eLAPa"})]

        #Filter new posts that have not been stored yet
        new_posts = [tag for tag in post_tags if tag not in post_soup]
        post_soup += new_posts

        return self._create_post_objects(post_soup)

    def _create_post_objects(self, post_soup):
        """Create a Post object from the given shortcode"""
        posts = []
        for post in post_soup:
            shortcode = post["href"].replace("/p/", "")[:-1]
            posts.append(Post(shortcode))
        return posts