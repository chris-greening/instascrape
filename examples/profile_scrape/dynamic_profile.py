import os
import sys
from sys import platform
import time
from pathlib import Path

import pandas as pd
import numpy as np
from selenium.webdriver import Chrome, ChromeOptions
from bs4 import BeautifulSoup

sys.path.insert(0, os.path.abspath(r"..\.."))
from instascrape import Profile, Post

chrome_options = ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)


class DynamicProfile(Profile):
    """Subclass of Profile to provide some dynamic functionality using Selenium"""

    def dynamic_load(self, browser, max_posts=sys.maxsize):
        """Scroll the users Profile page and load all posts into Post objects"""
        source_data = self._scroll_page(browser)
        post_soup = self._seperate_posts(source_data)
        self._create_post_objects(post_soup, max_posts)
        self._grab_useful_data()
        browser.close()

    def _scroll_page(self, browser):
        """Scroll page and load the source code"""
        browser.get(self.url)

        source_data = []
        js_script = "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;"
        lenOfPage = browser.execute_script(js_script)
        match = False
        while not match:
            time.sleep(abs(np.random.normal(3, 1.5)))
            lastCount = lenOfPage
            lenOfPage = browser.execute_script(js_script)
            source_data.append(browser.page_source)
            if lastCount == lenOfPage:
                match = True
        return source_data, browser

    def _seperate_posts(self, source_data):

        post_soup = []
        for source in source_data[0]:
            soup = BeautifulSoup(source, features="lxml")
            # posts = soup.find("span", {"id":"react-root"})

            anchor_tags = soup.find_all("a")
            found = [tag for tag in anchor_tags if tag.find("div", {"class": "eLAPa"})]

            for tag in found:
                if tag not in post_soup:
                    post_soup.append(tag)
        return post_soup

    def _create_post_objects(self, post_soup, post_size):
        # create post objects for each post on the page
        self.posts = []
        for post in post_soup:
            shortcode = post["href"].replace("/p/", "")[:-1]
            self.posts.append(Post.from_shortcode(shortcode))
            if len(self.posts) >= post_size:
                break

    def _grab_useful_data(self):
        for i, post in enumerate(self.posts):
            if i % 10 == 0:
                print('Read {} posts'.format(i))
            try:
                post.load()
            except Exception as e:
                print(e)


if __name__ == "__main__":
    chris = DynamicProfile.from_username("chris_greening")
    chris.load()
    chris.dynamic_load(Chrome('/tmp/chromedriver'), max_posts=15)

    data_arr = []
    for post in chris.posts:
        try:
            data_arr.append((post.upload_date, post.likes, post.comments))
            print(data_arr)
        except AttributeError as e:
            print(e)
            pass

