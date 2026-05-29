---
title: Team
nav:
  order: 2
  tooltip: About our team
---

# {% include icon.html icon="fa-solid fa-users" %}Team

{% include list.html data="members" component="portrait" filter="role == 'principal-investigator'" %}
{% include list.html data="members" component="portrait" filter="role == 'postdoc'" %}
{% include list.html data="members" component="portrait" filter="role == 'grad' and group == 'team'" %}
{% include list.html data="members" component="portrait" filter="role == 'undergrad' and group == 'team'" %}


## Alumni

{% include list.html  data="members"  component="portrait"  filter="group == 'alumni'" %}

{% include section.html %}

Please [reach out]({{ '/recruitment/' | relative_url }}) if you are interested in joining!
