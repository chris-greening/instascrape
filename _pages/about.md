---
permalink: /about/
title: "About"
excerpt: "instascrape is a powerful and lightweight Python library for scraping Instagram data"
---

## What is it?

{% highlight python %}
import instascrape
{% endhighlight %}

`instascrape` is a powerful, lightweight Python library for scraping Instagram data and content with no configurations necessary!
It is designed with flexibility and developer productivity in mind so you can stop wasting valuable time collecting data and just start analyzing it.

{% highlight python %}
from instascrape import Profile
google = Profile("Google")
google.scrape()
print(f"Google has {google.followers:,} followers.")
>>> Google has 12,283,945 followers.
{% endhighlight %}

## Key features

{% highlight python %}
for feature in key_features:
    print(feature)
{% endhighlight %}

* Powerful and flexible object-oriented scraping tools
* Download Instagram content to your computer
* Dynamically retrieve HTML embed code for Instagram posts
* Expressive and consistent API for concise and elegant code
* Designed for seamless integration with [_Selenium_](https://selenium-python.readthedocs.io/), [_Pandas_](https://pandas.pydata.org/), etc.
* Incredibly lightweight
* Leverages [_Requests_](https://requests.readthedocs.io/en/master/) and [_Beautiful Soup_](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) under the hood
* Proven to work as of December, 2020

## The philosophy

{% highlight python %}
import this
{% endhighlight %}

`instascrape` was designed with [The Zen of Python](https://www.python.org/dev/peps/pep-0020/) at its heart. Every design choice is carefully considered to make scraping Instagram data and content as smooth as possible. The syntax is expressive and concise, allowing for beautiful and explicit code that is clean and immediately obvious. There should never be a moment where you're questioning why the API does what it does; it is fluid and intuitive, designed for you the developer.

## About the author

{% highlight python %}
from chris_greening import bio
{% endhighlight %}

Chris Greening is a Python developer passionate about science, data, and computers. When he isn't programming he's probably playing video games or working on his photography.