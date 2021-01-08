---
title: Important planned features for January 
---

Hello and happy new year everyone!


## A temporary problem... 

Over the last few weeks, Instagram has been making it harder and harder to scrape data. I've had quite a few people reach out to me because the `instascrape` scrapers are often raising the `InstagramLoginRedirectError` either immediately or after just a few scrapes.

## ...and a proposed solution

I believe I have found a solution to the problem and with that, I will be working on official `selenium` support as well as cookie and session handling to better emulate actual browser requests. 

It's going to take me a couple days/weeks to roll this out but I believe the solution is in sight and it's going to be a great improvement to the library. Whether or not it will be a major or minor release is TBD, I have some ideas for breaking changes that I might implement but I'll have a better idea once I make more progress. 

# For the time being

I've had to do some Instagram scraping since the advent of these new restrictions and was able to come up with some temporary workarounds. First, `selenium` still works fine so I used that instead of the `instascrape` scraper objects to request pages. Once the webpage was returned, I stored the HTML and used some of `instascrape`'s JSON tools to parse the data manually which was a bit more code but manageable 

Secondly, I just found today that cookies are the way to go! Should've been more obvious from the get go but it hasn't been a problem until now it seems. Go in your web browser and find your request headers. Copy the value for the cookie that gets sent to Instagram and this should let you bypass the InstagramLoginRedirectError by passing it in a header to `requests.get`. 

{% highlight python %}
import requests 

from instascrape import Profile 

headers = {
    "user-agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.66", 
    "cookie":'PASTE YOUR COOKIE HERE'
}

resp = requests.get("https://www.instagram.com/google/", headers=headers)

google = Profile(resp.text).scrape() 

{% endhighlight %}

Like I said, `instascrape` will be receiving dedicated support for these to make it a lot smoother but for now, these should work. 

Email me if you have questions: chris@christophergreening.com

Regards, 
Chris 