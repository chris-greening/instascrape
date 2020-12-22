import sys
import time
import os

from selenium import webdriver
import numpy as np
from bs4 import BeautifulSoup

from instascrape.scrapers import Profile, Post

#TODO: this script is admittedly pretty hacky, will legitimize and clean this
# up at a later date

class DynamicProfile(Profile):
    """Subclass of Profile to provide some dynamic functionality using Selenium"""
    CHROMEDRIVER = r"C:\Users\Chris\chromedriver.exe"
    JS_SCROLL_SCRIPT = "window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;"

    def get_all_posts(self):
        """Scroll the users Profile page and load all posts into Post objects"""
        browser = webdriver.Chrome(DynamicProfile.CHROMEDRIVER)
        source_data = self._scroll_page(browser)
        post_soup = self._seperate_post_soup(source_data)
        posts = self._create_post_objects(post_soup)
        return posts

    def _scroll_page(self, browser):
        """Scroll page and store HTML source everytime AJAX loads new data"""
        browser.get(self.source)

        source_data = []
        page_len = browser.execute_script(DynamicProfile.JS_SCROLL_SCRIPT)
        match = False
        #Pause program to login manually and navigate back to profile page
        time.sleep(60)

        while not match:
            time.sleep(10)  #wait for page to load
            last_count = page_len
            page_len = browser.execute_script(DynamicProfile.JS_SCROLL_SCRIPT)
            source_data.append(browser.page_source)
            if last_count == page_len:   #reached the end, stop scrolling
                match = True

        return source_data

    def _seperate_post_soup(self, source_data):
        """Separate the HTML and parse out BeautifulSoup for every post"""
        post_soup = []
        for source in source_data:
            soup = BeautifulSoup(source, features="lxml")
            anchor_tags = soup.find_all("a")
            post_tags = [tag for tag in anchor_tags if tag.find(
                "div", {"class": "eLAPa"})]

            #Filter new posts that have not been stored yet
            new_posts = [tag for tag in post_tags if tag not in post_soup]
            post_soup += new_posts

        return post_soup

    def _create_post_objects(self, post_soup):
        """Create a Post object from the given shortcode"""
        posts = []
        for post in post_soup:
            shortcode = post["href"].replace("/p/", "")[:-1]
            posts.append(Post(shortcode))
        return posts
