---
title: "The Reel and IGTV Scrapers"
---

Hey everyone,

The recent releases of versions 1.5.0 and 1.6.0 introduced the `Reel` and `IGTV` scrapers respectively. 

Both are subclasses of the `Post` scraper so you can expect behaviors and methods to be almost exactly the same. In terms of the JSON served back from Instagram, reels and IGTV videos are essentially specialized versions of normal posts and can thus be scraped as such.

## Available methods
- `scrape`
- `to_dict`
- `to_csv`
- `to_json`
- `download`
- `get_recent_comments`
- `embed`

## Sample Usage:

{% highlight python %}
from instascrape import Reel
google_reel = Reel("https://www.instagram.com/reel/CIrJSrFFHM_/")
google_reel.scrape()
{% endhighlight %}

## Design decision on IGTV scraper name

I debated back and forth with myself whether or not to name the class `IGTV` or `Igtv`. In the end, I ended up settling on the all caps variant. I know an all caps name is a little unconventional considering caps are usually reserved for constants. In the context of `instascrape` however, one of the driving design decisions has been readability and elegance in code appearence. IGTV is what Instagram calls the platform so I decided using this as the exact class name was the cleanest and most obvious looking (plus, `Igtv` just looks weird)

## Moving forward

Getting the scrapers into the hands of the public in a stable condition as soon as possible is what motivated me to push these out as quickly as I could. Now that they're ready to be used, I'll start expanding on them and finding neat features to implement; let me know if there is anything you want to see for these!