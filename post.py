import json
import datetime

import requests 
from bs4 import BeautifulSoup 

class Post: 
    def __init__(self, url):
        self.url = url
         
    def load(self):
        """Load the static HTML into a BeautifulSoup object at the url"""
        self.page_source = requests.get(self.url).text
        self.soup = BeautifulSoup(self.page_source, features='lxml')

        self._scrape_soup()

    def _scrape_soup(self):
        """Scrape data from the soup"""
        self.title = self.soup.find("title").text

        
        post_json = self._get_post_json()
        self._scrape_post_json(post_json)
        self._get_hashtags()

    def _get_hashtags(self):
        hashtags_meta = self.soup.find_all('meta', {'property':'instapp:hashtags'})
        self.hashtags = [tag['content'] for tag in hashtags_meta]

    def _get_post_json(self) -> dict: 
        """Get the posts json data as a dictionary"""
        post_json_script = [str(script) for script in self.soup.find_all('script') if 'config' in str(script)][0]
        left_index = post_json_script.find('{')
        right_index = post_json_script.rfind('}') + 1
        json_str = post_json_script[left_index:right_index]
        return json.loads(json_str)

    def _scrape_post_json(self, post_json: dict):
        """Scrape data from the posts json"""
        self.country_code = post_json['country_code']
        self.language_code = post_json['language_code']
        self.locale = post_json['locale']

        #Convenience definition for post info 
        post_info = post_json['entry_data']['PostPage'][0]['graphql']['shortcode_media']
        self.upload_date = datetime.datetime.fromtimestamp(post_info['taken_at_timestamp'])
        self.accessibility_caption = post_info['accessibility_caption']
        self.likes = post_info['edge_media_preview_like']['count']
        self.amount_of_comments = post_info['edge_media_preview_comment']['count']
        self.caption_is_edited = post_info['caption_is_edited']
        self.has_ranked_comments = post_info['has_ranked_comments']
        self.location = post_info['location']
        self.is_ad = post_info['is_ad']
        self.viewer_can_reshare = post_info['viewer_can_reshare']
        self.shortcode = post_info['shortcode']
        self.dimensions = post_info['dimensions']
        self.is_video = post_info['is_video']
        self.fact_check_overall_rating = post_info['fact_check_overall_rating']
        self.fact_check_information = post_info['fact_check_information']

        #Get caption and tagged users 
        self.caption = post_info['edge_media_to_caption']['edges'][0]['node']['text']
        self._get_tagged_users(post_info)

        #Owner json data
        owner = post_info['owner']
        self.is_verified = owner['is_verified']
        self.profile_pic_url = owner['profile_pic_url']
        self.username = owner['username']
        self.blocked_by_viewer = owner['blocked_by_viewer']
        self.followed_by_viewer = owner['followed_by_viewer']
        self.full_name = owner['full_name']
        self.has_blocked_viewer = owner['has_blocked_viewer']
        self.is_private = owner['is_private']

    def _get_tagged_users(self, post_info: dict):
        """Scrape the usernames of the tagged users""" 
        tagged_users = post_info['edge_media_to_tagged_user']['edges']
        self.tagged_users = [user['node']['user']['username'] for user in tagged_users]

    @classmethod
    def from_shortcode(cls, shortcode: str) -> 'Post':
        """Return a Post given a shortcode"""
        url = f'https://www.instagram.com/p/{shortcode}/'
        return cls(url)
    
if __name__ == '__main__':
    url = r'https://www.instagram.com/p/CFQNno8hSDX/'
    post = Post(url)
    post.load_page_source()