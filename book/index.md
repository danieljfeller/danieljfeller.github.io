---
layout: book
title: "The Health Data Handbook"
description: "A free, practical guide to the data types, standards, and formats behind modern health AI: claims, EHRs, imaging, clinical trials, genomics, and patient-generated data. By Daniel Feller, PhD."
permalink: /book/
---

{% assign book = site.data.book %}
<div class="book-cover-hero">
  <img src="{{ '/images/book/cover.png' | relative_url }}" alt="{{ book.title }} book cover" class="book-cover-img">
  <div class="book-cover-meta">
    <h1>{{ book.title }}</h1>
    <p class="book-subtitle">{{ book.subtitle }}</p>
    <p class="book-author">{{ book.author }}</p>
    <p class="book-description">A practical guide to the data types, standards, and formats behind modern health AI. Written for mid-career tech professionals and data scientists entering healthcare, and for healthcare data professionals who want to broaden their knowledge across data streams. Free to read online, chapter by chapter.</p>
    <p class="book-actions"><a class="book-actions-primary" href="{{ book.parts[0].chapters[0].url | relative_url }}">Start reading →</a> <a class="book-actions-secondary" href="{{ '/book/intro/core-concepts/' | relative_url }}">New to healthcare? Start with Core Concepts</a></p>
  </div>
</div>

<div class="book-streams" aria-label="What the book covers">
  <span>Medical &amp; pharmacy claims</span>
  <span>Electronic health records</span>
  <span>Medical imaging</span>
  <span>Clinical trials</span>
  <span>Molecular sequencing</span>
  <span>Wearables &amp; home devices</span>
  <span>Patient-reported outcomes</span>
  <span>De-identification</span>
</div>

## Table of contents

{% for part in book.parts %}
<section class="book-toc-part">
  <h3>{{ part.name }}</h3>
  {% if part.blurb %}<p class="book-toc-blurb">{{ part.blurb }}</p>{% endif %}
  <ol class="book-toc-list">
    {% for ch in part.chapters -%}
    <li><a href="{{ ch.url | relative_url }}">{{ ch.title }}</a>{% if ch.description %}<span class="book-toc-desc">{{ ch.description }}</span>{% endif %}</li>
    {% endfor -%}
  </ol>
</section>
{% endfor %}

---

<small>© Daniel Feller. Licensed under <a href="https://creativecommons.org/licenses/by-nc/4.0/">CC BY-NC 4.0</a>. Free for educational and non-commercial use with attribution. Cite as: Feller, D. <em>{{ book.title }}</em>. danieljfeller.github.io/book. For commercial licensing, contact <a href="mailto:danieljfeller@gmail.com">danieljfeller@gmail.com</a>.</small>
