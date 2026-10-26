---
title: "Welcome the Earl of Quince!"
date: 2026-10-27 00:00:00 +0900
show_day: false
image: images/posts/Earl of Quince/EoQ_main.jpg
tags:
  - lab-life
---
<div class="eoq-description" markdown="1">
<!-- excerpt start -->
welcome the Earl of Quince, freshly “borrowed” from the school’s quince tree.
<!-- excerpt end -->
</div>

<style>
.eoq-description p { text-align: center; }
.eoq-gallery, .eoq-divider {
  width: min(100%, 820px, calc(520px * 2957 / 2218));
  margin-inline: auto;
}
.eoq-divider {
  height: 0;
  border: 0;
  border-top: 1px solid #d1d5db;
  margin-block: 48px;
}
.eoq-gallery img { height: auto; }
.eoq-gallery .figure:first-child { margin-top: 0; }
@media (max-width: 600px) {
  .eoq-gallery, .eoq-divider { width: min(100%, 820px, calc(60vh * 2957 / 2218)); }
}
</style>

<hr class="eoq-divider">

<div class="eoq-gallery" markdown="1">

{% include figure.html image="images/posts/Earl of Quince/EoQ_1.jpg" width="100%" %}

<video autoplay muted loop playsinline preload="metadata" aria-label="The Earl of Quince video" style="display: block; width: 100%; height: auto; margin: 40px auto; border-radius: var(--rounded); box-shadow: var(--shadow);">
  <source src="{{ '/images/posts/Earl of Quince/EoQ_2.mp4' | relative_url | uri_escape }}" type="video/mp4">
</video>

{% include figure.html image="images/posts/Earl of Quince/EoQ_3.jpg" width="100%" %}

</div>
