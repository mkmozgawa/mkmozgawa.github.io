---
title: "Informacje publiczne"
permalink: /informacje-publiczne/
layout: archive
author_profile: true
---

Wnioski o udostępnienie informacji publicznej wysłane do instytucji publicznych oraz otrzymane odpowiedzi.

{% assign public_information_posts = site.public_information | sort: "date" | reverse %}
{% for post in public_information_posts %}
  {% unless post.archive == false %}
    {% include archive-single.html %}
  {% endunless %}
{% endfor %}
