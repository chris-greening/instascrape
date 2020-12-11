---
title: "Latest feature: Instagram location scraping"
---

# Introducing the Location scraper

Someone opened a [feature request](https://github.com/chris-greening/instascrape/issues/49) today on the repo requesting a means for scraping Instagram location tags. 
An hour or two later and here we are, check it out:

The release of v1.4.0 comes with the new `Location` scraper that can scrape some neat goodies from these location tags. 

Just feed it a URL like any of the other scrapers in the library and it'll get you stuff like the latitude and logitude coordinates, the city name, the region, how many posts are in it, etc. as well as the ability to scrape the 14 most recent posts made to that tag! 

Syntax is just like any of the other scrapers in the library and it most closely resembles the `Hashtag` scraper with a `get_recent_posts` method that returns `Post` objects. 

{% highlight python %}
from instascrape import Location 
url = "https://www.instagram.com/explore/locations/212988663/new-york-new-york/"
new_york = Location(url)
new_york.scrape()
print(f"{new_york.amount_of_posts:,} people have been to New York"
>>> 61,202,403 people have been to New York
{% endhighlight %}

# Future expansions

Aside from expansions and updates to the `Location` scraper, there are also Location Directory pages that I plan on writing some scrapers for so keep an eye out for those. To do anything meaningful with them, I might need to employ some sort of JavaScript rendering (which I am very weary to do so we'll have to see).

Additionally, I had the idea to create a scraper for the Explore page which can be found at this [endpoint](https://www.instagram.com/explore/). This will probably come sometime in the next few days; this feature request definitely opened my eyes though for a couple fresh ideas that can be implemented for more robust scraping.

Stay safe everyone,
Chris