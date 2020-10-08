import json # import needed libraries / pip3 install json

from instascrape import Profile # pip3 install insta-scrape

import pandas as pd # pip3 install pandas

google = Profile.from_username('google') # declare profile

google.static_load() # scrape profile

google_data = google.to_dict() # turn scraped data into python dictionary

google_serialized = json.dumps(google_data) # serialize dictionary into json

with open('google.json', 'w') as outfile: # write json data to "google.json"
     json.dump(google_data, outfile) 

with open('google.json', encoding='utf-8-sig') as f_input: # read json data from "google.json" and create pandas dataframe
    df = pd.read_json(f_input)

df.to_csv('google.csv', encoding='utf-8', index=False) # convert dataframe to csv and write to "google.csv"

