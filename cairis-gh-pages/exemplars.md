---
layout: archive
title: Exemplars
---

<div class="tiles">
{% for page in site.pages %}
  {% for pc in page.categories %}
    {% if pc == 'exemplar' %}
      {% include page-grid.html %}
    {% endif %}
  {% endfor %}
{% endfor %}
</div>
