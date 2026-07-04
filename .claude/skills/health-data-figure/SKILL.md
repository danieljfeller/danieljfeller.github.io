---
name: health-data-figure
description: >-
  Create or regenerate figures for the book "Decoding Health Data" (book/ in this
  repo) as Nature-style SVGs to the project's visual standard. Use whenever making
  a book figure, health-data diagram, or illustration of how health data is
  generated/structured — file-format layouts (FASTQ, SAM/BAM, VCF, CRAM, claims,
  code structures), workflow/pipeline diagrams, quantitative charts/time series,
  or conceptual schematics. Triggers: "book figure", "health data figure",
  "regenerate figure", "Nature-style figure", "diagram of how <data> is generated",
  "format diagram", "pipeline diagram", "add a figure to <chapter>".
---

# Health-data figure

Produce figures for *Decoding Health Data* that read as one publication, styled
like *Nature* graphics but tinted to the book's website. Output is always **SVG**
saved to `images/book/<slug>.svg` and referenced from a chapter's `<figure>`.

Before drawing anything, read [references/visual-standard.md](references/visual-standard.md)
(the full spec) and [references/palette.md](references/palette.md) (the only
allowed colors). Everything below assumes those tokens.

## Workflow

### 1. Classify the figure into one family
Every book figure is one of four. Pick the family — it selects your template and
your rules:

| Family | Looks like | Template |
|---|---|---|
| **1 · File-format layout** | annotated monospace record/table + callouts | `templates/format-layout.svg` |
| **2 · Workflow / pipeline** | labeled boxes joined by arrows | `templates/workflow.svg` |
| **3 · Quantitative chart** | plotted signal(s) with axes | `templates/quant-chart.svg` |
| **4 · Conceptual schematic** | illustrative diagram (e.g. puzzle) | start from the closest of the above |

For **family 3 only**, also invoke the **`dataviz`** skill and follow its mark and
color-validator rules; feed it `#0969da` as the brand primary and the palette.md
categorical sequence as the ramp. This standard owns how book figures *look*;
dataviz owns how a *correct chart* is built.

### 2. Start from the template
Copy the family's file from `templates/`. It already encodes the canvas margin,
`viewBox` width (~460 single-column, ~900 double), font stack, axis weights, and
`role="img"` + `<title>`/`<desc>` scaffolding. Delete the guidance comments as you
fill it in.

### 3. Author to the standard
Apply the tokens: white/transparent canvas, `'Inter', Arial, Helvetica,
sans-serif` (mono stack for data glyphs), sentence case, no title inside the
figure, colors only from palette.md with primary anchored on `#0969da`, thin
outward-tick axes, bold-lowercase panel labels top-left for multi-panel figures.
If plotting data, decide real vs. illustrative-synthetic — you'll state it in the
caption.

### 4. Save
Write to `images/book/<slug>.svg`. Reuse the existing slug when regenerating a
figure so the chapter reference and file line up.

### 5. Wire it into the chapter
Point the chapter's existing `<figure>` at the SVG (keep the `<figcaption>`):
```html
<figure>
  <img src="{{ '/images/book/<slug>.svg' | relative_url }}" alt="...">
  <figcaption>...</figcaption>
</figure>
```
Use **straight ASCII quotes** in the Liquid tag — curly quotes break
`relative_url`. Update the `alt` to match the new figure; if the caption used
uppercase panel letters `(A)(B)(C)`, switch it to lowercase `a b c` to match the
figure. If replacing a `.png`, delete the superseded PNG. (Adding a brand-new
figure to the book also means the three-place sync in `book/CLAUDE.md` if it's a
new chapter — but a figure inside an existing chapter is just the `<figure>` block.)

### 6. Validate
- Open the `.svg` directly in a browser: it must render standalone (Arial/
  Helvetica fallback is expected and correct).
- Check it against the "Checklist before saving" at the end of visual-standard.md.
- For charts, confirm color pairings against palette.md (or dataviz's validator)
  and that no distinction is color-only.
- Confirm the chapter caption states data provenance (real vs. illustrative).

## The book's figure inventory (for reference)
Existing figures live in `images/book/`. Canonical worked examples of each family:
`fastq-format.svg` (family 1), `sequencing-pipeline.svg` (family 2),
`accelerometer-axes.svg` (family 3). Match their construction when adding new ones.
