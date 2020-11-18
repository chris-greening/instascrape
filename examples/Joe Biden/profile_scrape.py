import time
import datetime

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from dynamic_profile import DynamicProfile

joe = DynamicProfile('https://www.instagram.com/joebiden')
posts = joe.get_all_posts()

#Scrape just the first 500 posts
print(len(posts))
for i, post in enumerate(posts[:500]):
    #sleep between requests so Insta doesn't get mad
    time.sleep(4)
    print(i)
    try:
        post.scrape()
    except Exception as e:
        print(e)