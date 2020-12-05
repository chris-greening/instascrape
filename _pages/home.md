---
layout: splash
permalink: /
header: 
  overlay_image: images/instagram_gradient.jpeg
  cta_label: "<i class='fa fa-download'></i> pip install insta-scrape"
  cta_url: "https://pypi.org/project/insta-scrape/"
excerpt: Powerful and lightweight Instagram scraping with Python
---

{% for post in site.posts %}
  {% if year != written_year %}
    <h2 id="{{ year | slugify }}" class="archive__subtitle">{{ year }}</h2>
    {% capture written_year %}{{ year }}{% endcapture %}
  {% endif %}
  {% include archive-single.html %}
{% endfor %}