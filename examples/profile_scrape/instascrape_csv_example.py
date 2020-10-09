import json # import needed libraries / pip3 install json

from instascrape import Profile # pip3 install insta-scrape

import pandas as pd # pip3 install pandas

google = Profile.from_username('google') # declare profile

google.static_load() # scrape profile

google_data = google.to_dict() # turn scraped data into python dictionary

google_data = {key: [val] for key, val in google_data.items()}   
df = pd.DataFrame(google_data)

df.to_csv('google.csv', encoding='utf-8', index=False) # convert dataframe to csv and write to "google.csv"
