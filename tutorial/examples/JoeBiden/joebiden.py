# See this tutorial to find your sessionid:
# http://valvepress.com/how-to-get-instagram-session-cookie/

from selenium.webdriver import Chrome
from instascrape import Profile, scrape_posts

# Creating our webdriver
webdriver = Chrome("path/to/chromedriver.exe")

# Scraping Joe Biden's profile
SESSIONID = 'ENTER_YOUR_SESSION_ID_HERE'
headers = {"user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.57",
           "cookie": f"sessionid={SESSIONID};"}
joe = Profile("joebiden")
joe.scrape(headers=headers)

# Scraping the posts
posts = joe.get_posts(webdriver=webdriver, login_first=True)
scraped, unscraped = scrape_posts(posts, silent=False, headers=headers, pause=10)
