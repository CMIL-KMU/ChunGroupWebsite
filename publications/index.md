---
title: Publications
nav:
  order: 3
  tooltip: Published works
---

# {% include icon.html icon="fa-solid fa-book-open" %} Publications

{% include search-box.html %}

## Selected publications

{% include citation.html lookup="doi:10.48550/arXiv.2411.17839" style="rich" %}

{% include citation.html lookup="doi:10.1021/acs.jctc.5c00090" style="rich" %}

{% include citation.html lookup="doi:10.1038/s41524-024-01432-1" style="rich" %}

{% include citation.html lookup="doi:10.1016/j.checat.2021.06.001" style="rich" %}

{% include section.html %}


{% include button.html icon="fa-brands fa-google" text="More on Google Scholar" link="https://scholar.google.com/citations?hl=ko&user=ZrnibVwAAAAJ" %}


{% include search-info.html %}

<div class="publication-tabs">
  <button id="tab-papers" class="tab-btn active" onclick="switchPubTab('papers')">Papers & Preprints</button>
  <button id="tab-patents" class="tab-btn" onclick="switchPubTab('patents')">Patents</button>
</div>

<div id="papers-list">
  {% include list.html data="citations" component="citation" filter="type != 'patent'" %}
</div>

<div id="patents-list" style="display: none;">
  {% include list.html data="citations" component="citation" filter="type == 'patent'" %}
</div>

<script>
  function switchPubTab(tab) {
    const papersList = document.getElementById('papers-list');
    const patentsList = document.getElementById('patents-list');
    const tabPapers = document.getElementById('tab-papers');
    const tabPatents = document.getElementById('tab-patents');
    
    if (tab === 'papers') {
      papersList.style.display = 'block';
      patentsList.style.display = 'none';
      tabPapers.classList.add('active');
      tabPatents.classList.remove('active');
    } else {
      papersList.style.display = 'none';
      patentsList.style.display = 'block';
      tabPapers.classList.remove('active');
      tabPatents.classList.add('active');
    }
  }
</script>