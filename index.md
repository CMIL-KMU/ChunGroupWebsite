---
---

{%- comment -%}
  Button labels go through t.html so they switch with the KOR/ENG toggle.
  They are captured up front because button.html takes its label as a
  parameter, and a Liquid parameter cannot itself contain a tag.
{%- endcomment -%}
{% capture explore_text %}{% include t.html key="home.explore" %}{% endcapture %}
{% capture all_pubs_text %}{% include t.html key="home.all_publications" %}{% endcapture %}
{% capture more_news_text %}{% include t.html key="home.more_news" %}{% endcapture %}
{% capture join_details_text %}{% include t.html key="home.join_details" %}{% endcapture %}

<div class="home-hero">
  <h1 class="home-hero-title">{% include t.html en="Computational Materials Intelligence Lab" ko="계산 소재 지능 연구실" %}</h1>
  <p class="home-hero-desc lang" data-lang="en">
    We are a computational research group working at the interface of artificial intelligence and atomistic simulations, with a focus on the predictive design of functional materials. We develop AI-accelerated computational frameworks that enable efficient exploration of complex materials design spaces.
  </p>
  <p class="home-hero-desc lang" data-lang="ko">
    인공지능과 계산과학 기반 모델링 및 시뮬레이션을 활용하여 기능성 소재의 예측 설계를 목표로 합니다. 복잡한 소재 설계 및 탐색 과정을 가속화 하기 위한 인공지능 모델 및 플랫폼을 개발하고 있습니다.
  </p>
  <div class="home-hero-cta">
    {%
      include button.html
      link="research"
      text=explore_text
      icon="fa-solid fa-arrow-right"
      flip=true
      style="bare"
    %}
  </div>
</div>

<!-- section break -->

# {% include icon.html icon="fa-solid fa-fire" %}{% include t.html key="home.featured" %}

{% assign sorted_publications = site.data.citations | sort: "date" | reverse %}
{% assign featured_publications = sorted_publications | where_exp: "citation", "citation.image != nil" | limit: 4 %}
<div class="slider-wrapper">
  <button class="slider-arrow prev" onclick="scrollSlider('research-slider', -1)" aria-label="Previous slider item">❮</button>
  <div class="slider-container" id="research-slider">
    {% for pub in featured_publications %}
      <div class="slide">
        {% include citation.html style="rich" lookup=pub.id %}
      </div>
    {% endfor %}
  </div>
  <button class="slider-arrow next" onclick="scrollSlider('research-slider', 1)" aria-label="Next slider item">❯</button>
</div>

<div style="text-align: center; margin-top: 25px;">
  {%
    include button.html
    link="publications"
    text=all_pubs_text
    icon="fa-solid fa-book"
    style="bare"
  %}
</div>

<!-- section break -->

# {% include icon.html icon="fa-solid fa-newspaper" %}{% include t.html key="home.updates" %}

{% assign sorted_posts = site.posts | sort: "date" | reverse %}
<div class="cols home-news-grid" style="--cols: 2; margin-top: 30px;">
  <div>
    <h2 class="home-news-column-title">
      {% include icon.html icon="fa-solid fa-trophy" %}{% include t.html key="home.honors" %}
    </h2>
    {% assign honors_posts = sorted_posts | where_exp: "post", "post.tags contains 'achievements'" | limit: 5 %}
    {% if honors_posts.size > 0 %}
      <div class="slider-wrapper">
        <button class="slider-arrow prev" onclick="scrollSlider('honors-slider', -1)" aria-label="Previous slider item">❮</button>
        <div class="slider-container" id="honors-slider">
          {% for post in honors_posts %}
            <div class="slide">
              {% include post-excerpt.html lookup=post.slug %}
            </div>
          {% endfor %}
        </div>
        <button class="slider-arrow next" onclick="scrollSlider('honors-slider', 1)" aria-label="Next slider item">❯</button>
      </div>
    {% else %}
      <p style="color: var(--gray); font-style: italic; margin-top: 15px;">{% include t.html key="home.no_honors" %}</p>
    {% endif %}
  </div>

  <div>
    <h2 class="home-news-column-title">
      {% include icon.html icon="fa-solid fa-users" %}{% include t.html key="home.lab_life" %}
    </h2>
    {% assign lab_life_posts = sorted_posts | where_exp: "post", "post.tags contains 'lab-life'" | limit: 5 %}
    {% if lab_life_posts.size > 0 %}
      <div class="slider-wrapper">
        <button class="slider-arrow prev" onclick="scrollSlider('lab-life-slider', -1)" aria-label="Previous slider item">❮</button>
        <div class="slider-container" id="lab-life-slider">
          {% for post in lab_life_posts %}
            <div class="slide">
              {% include post-excerpt.html lookup=post.slug %}
            </div>
          {% endfor %}
        </div>
        <button class="slider-arrow next" onclick="scrollSlider('lab-life-slider', 1)" aria-label="Next slider item">❯</button>
      </div>
    {% else %}
      <p style="color: var(--gray); font-style: italic; margin-top: 15px;">{% include t.html key="home.no_lab_life" %}</p>
    {% endif %}
  </div>
</div>

<div style="text-align: center; margin-top: 30px;">
  {%
    include button.html
    link="news"
    text=more_news_text
    icon="fa-solid fa-arrow-right"
    flip=true
    style="bare"
  %}
</div>

<!-- section break -->

<div class="home-recruitment-banner">
  <h2>{% include icon.html icon="fa-solid fa-user-plus" %}{% include t.html key="home.join_title" %}</h2>
  <p class="lang" data-lang="en">
    We welcome applications from motivated people with diverse backgrounds in Chemistry, Physics, Materials Science, Chemical Engineering, Computer Science, and energy engineering who are interested in computational materials chemistry.
  </p>
  <p class="lang" data-lang="ko">
    인공지능과 계산과학 연구에 관심있는 화학, 물리, 신소재공학, 화학공학, 컴퓨터공학 등 다양한 전공의 학부생, 대학원생, 박사후연구원들의 지원을 환영합니다!
  </p>
  <div class="recruitment-cta">
    {%
      include button.html
      link="recruitment"
      text=join_details_text
      icon="fa-solid fa-circle-info"
      style="bare"
    %}
  </div>
</div>
