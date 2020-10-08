import json

from instascrape import Profile

google = Profile.from_username('google')

google.static_load()

google_data = google.to_dict()

import pandas as pd

google_serialized = json.dumps(google_data)

with open('google.json', 'w') as outfile:
     json.dump(google_data, outfile)

with open('google.json', encoding='utf-8-sig') as f_input:
    df = pd.read_json(f_input)

df.to_csv('google.csv', encoding='utf-8', index=False)

