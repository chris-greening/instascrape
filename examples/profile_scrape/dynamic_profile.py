import os
import sys 
import time 

from pandas import DataFrame
from selenium.webdriver import Chrome, ChromeOptions
from bs4 import BeautifulSoup

sys.path.insert(0, os.path.abspath('..'))
from instascrape import Profile, Post

chrome_options = ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)

class DynamicProfile(Profile):
    """Subclass of Profile to provide some dynamic functionality"""
    def get_all_posts(self):
        """Scroll the users Profile page and load all posts into Post objects"""
        source_data, browser = self._scroll_page()
        post_soup = self._seperate_posts(source_data)
        self._create_post_object(post_soup)
        self._grab_useful_data()
        browser.close()
        
    def _scroll_page(self):
        """Scroll page and load the source code"""
        browser = Chrome(r'C:\Users\Chris\chromedriver.exe',
                         chrome_options=chrome_options)
        browser.get(self.url)

        source_data = []
        js_script = 'window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;'
        lenOfPage = browser.execute_script(js_script)
        match=False
        while not match:
            time.sleep(3)
            lastCount = lenOfPage
            lenOfPage = browser.execute_script(js_script)
            source_data.append(browser.page_source)
            if lastCount==lenOfPage:
                match=True
        return source_data, browser

    def _seperate_posts(self, source_data):

        post_soup = []
        for source in source_data:
            soup = BeautifulSoup(source, features='lxml')
            posts = soup.find("span", {"id":"react-root"})

            anchor_tags = soup.find_all("a")
            found = [tag for tag in anchor_tags if tag.find("div", {"class":"eLAPa"})]

            for tag in found:
                if tag not in post_soup:
                    post_soup.append(tag)
        return post_soup

    def _create_post_object(self, post_soup):
        #create post objects for each post on the page 
        self.posts = []
        for post in post_soup:
            shortcode = post["href"]
            shortcode = shortcode.replace("/p/", "")
            shortcode = shortcode[:-1]
            self.posts.append(Post.from_shortcode(shortcode))

    def _grab_useful_data(self):
        for post in self.posts: 
            post.static_load()

if __name__ == '__main__':
    chris = DynamicProfile.from_username('chris_greening')
    chris.get_all_posts()