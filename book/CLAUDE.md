# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this directory is

`book/` holds the chapter pages for *The Health Data Handbook* (formerly *Decoding Health Data*), a book written by Daniel Feller (PhD, Biomedical Informatics, Columbia, 2020; now builds health tech startups) and published as a section of his Jekyll portfolio site (repo root is one level up, at `../`). There is no separate build system here — chapters are plain Markdown files rendered by the site-wide Jekyll config and the shared `book` layout.

## Audience and purpose

The book has two intended audiences at once, and chapter content should serve both:
- Established data scientists/engineers moving into medical or clinical work who need grounding in how healthcare data is generated and structured.
- Practitioners already working in one healthcare/life-sciences domain (e.g. claims, EHR) who want to expand into adjacent domains they don't know well (e.g. genomics, medical imaging).

Chapters should stay accessible to both: don't assume deep clinical background, but don't over-explain general data/engineering concepts. It's distributed for free online at danieljfeller.github.io/book and promoted chapter-by-chapter on LinkedIn; Daniel intends to eventually pursue formal publication, so content should be treated as publication-quality prose, not blog-post drafts.

## The manuscript is the source of truth; chapters are generated

Daniel writes the book in a single Google Doc and drops it here as `book/ebook.md.docx` (untracked; excluded from the Jekyll build by `_config.yml`). **Do not hand-edit chapter prose** — regenerate it:

```bash
python3 book/_build/docx_to_chapters.py book/ebook.md.docx
```

`book/_build/docx_to_chapters.py` converts the DOCX (`docx2md.py`, stdlib only), splits it into chapters by the `source` headings in `../_data/book.yml`, promotes headings one level, replaces the manuscript's figure placeholders with `<figure>` blocks, applies a short list of explicit cleanups (`FIXES`), renumbers footnotes per page, and writes each chapter with front matter from `book.yml`. Everything that is *not* in the manuscript (figure captions, placements, cross-reference fixes) lives in that script, so it survives the next DOCX drop. After regenerating, review `git diff` — new `[FIGURE: ...]` author notes or `![][imageN]` placeholders that the script can't place are printed as warnings and need a new entry in `FIGURES`, `FIGURE_NOTES`, or `ANCHORED`.

Rendering notes that the script relies on: kramdown with GFM input (`_config.yml`), footnotes via `[^n]`, one-cell manuscript tables are emitted as fenced code blocks, `$..$` math is not supported (use `<sub>`).

## Site build

The Jekyll site (title, plugins, exclusions, per-path defaults) is configured in `../_config.yml`. There is no `Gemfile` checked in and the system Ruby (2.6) is too old for current Jekyll, so `bundle exec jekyll serve` will not work out of the box — GitHub Pages builds the site remotely on push to `main` using its default supported gems (`jekyll-seo-tag`, `jekyll-redirect-from`, `jekyll-sitemap`, `jekyll-feed` are all on its allowlist). To preview locally, install a modern Ruby (e.g. `brew install ruby`) and `gem install jekyll jekyll-seo-tag jekyll-redirect-from jekyll-sitemap jekyll-feed`, then `jekyll serve`.

## Book structure lives in one data file

`../_data/book.yml` is the single source of truth for parts, chapter titles, URLs, descriptions, redirects, and the `source` heading each chapter is extracted from. It drives:
1. The sidebar in `../_layouts/book.html`.
2. The table of contents and part blurbs on `book/index.md`.
3. Previous/next links at the bottom of every chapter.
4. The front matter the build script writes into each chapter (`title`, `description`, `permalink`, `redirect_from`).

**Adding, renaming, or moving a chapter is a `book.yml` edit plus a rebuild.** Keep old URLs working with `redirect_from` (jekyll-redirect-from) rather than breaking links that have been shared.

Every chapter is a Markdown file with front matter:

```yaml
---
layout: book
title: "Chapter Title"
description: "One sentence shown under the title and used as the social-share blurb."
permalink: /book/<part>/<slug>/
---
```

The layout renders the `<h1>` from `title`, so chapter files start at `##`.

## Styling and sharing

The book layout, sidebar, pager, and chapter styling live in `../_layouts/book.html` and `../assets/css/book.css`, shared across all chapters — don't duplicate layout HTML inside chapter Markdown. Custom HTML blocks (`<div class="book-cover-hero">`, the TOC loop) are only used on `index.md`.

Every page under `book/` gets Open Graph / Twitter meta tags from `jekyll-seo-tag` (`{% seo %}` in the layout) with `images/book/social-card.png` as the default share image (set in `_config.yml` defaults), so a chapter URL pasted into LinkedIn unfurls with a title, the chapter `description`, and an image. The cover (`images/book/cover.png`) and the share card are generated by `book/_build/figures/gen_cover.py`; regenerate both if the title or subtitle changes.

## Figures

Figures live in `../images/book/` and are embedded with a `<figure>` block (kramdown passes the HTML through):

```html
<figure>
  <img src="{{ '/images/book/<slug>.svg' | relative_url }}" alt="...">
  <figcaption>...</figcaption>
</figure>
```

Use **straight ASCII quotes** in the Liquid tag — curly quotes break the `relative_url` filter and the image won't resolve. Because chapters are generated, a figure block is added or edited in `book/_build/docx_to_chapters.py`, not in the chapter file.

Figures should be **SVG** authored to the book's visual standard (Nature-style, tinted to the site). The standard, palette, and starter templates are owned by the `health-data-figure` skill (`../.claude/skills/health-data-figure/`) — invoke it rather than styling a figure ad hoc. Every book figure fits one of four families it templates: file-format layouts, workflow/pipeline diagrams, quantitative charts/time series, and conceptual schematics. All chapter figures are SVG; the cover and share card are the only rasters. Several data figures use illustrative synthetic data — say so in the `<figcaption>`. Quantitative figures are generated by short deterministic Python scripts in `book/_build/figures/`; when a figure needs new data, regenerate rather than hand-editing path coordinates. Third-party images from the manuscript are never embedded directly (copyright); recreate the concept as a book-styled SVG.

## Licensing footer

Every chapter renders a shared CC BY-NC 4.0 attribution footer from the layout — don't add a per-chapter copy of it in Markdown.
