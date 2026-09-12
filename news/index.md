---
title: News
title_ko: 소식
nav:
  order: 4
  tooltip: Latest news from the lab
---

# {% include icon.html icon="fa-solid fa-newspaper" %}{% include t.html key="news.heading" %}

{% include tags.html tags=site.tags %}

{% include search-info.html %}

{% include list.html data="posts" component="post-excerpt" %}