# Visual standard — *The Health Data Handbook* figures

This is the single source of truth for how every figure in the book looks. The
goal: a reader flipping between the medical-claims chapter and the genomics
chapter should feel they are looking at figures from **one publication**, styled
like the graphics in *Nature* but tinted to the book's website.

Read this in full before authoring or editing any figure. Color tokens live in
[palette.md](./palette.md).

---

## Principles (the "why")

*Nature*'s figures are legible because they spend ink only on information. We
inherit four habits from that house style:

1. **High data-ink ratio.** Every stroke earns its place. No drop shadows, no 3-D
   bevels, no decorative gradients, no boxes around things that don't need boxing.
2. **The figure has no title.** The one-line title and all explanation live in the
   Markdown `<figcaption>`, never baked into the SVG. This keeps figures reusable
   and keeps text selectable/translatable/accessible.
3. **Sentence case, everywhere.** Axis labels, node labels, annotations: "Read
   quality (Phred)", not "Read Quality (Phred)" or "READ QUALITY".
4. **One restrained palette.** Color encodes data, not decoration. Anchor on the
   site blue; extend only into the colorblind-safe sequence in palette.md.

---

## Canvas

- **Background: white `#ffffff` only.** The site has no dark mode (confirmed:
  `assets/css/book.css` has no `prefers-color-scheme` block), so figures need a
  single light-on-white variant. Do **not** author a dark variant.
- **Internal margin ≥ 12 units on every side.** The site CSS draws a
  `1px solid #d0d7de` border with `6px` radius around `.book-main figure img`;
  content flush to the edge gets visually clipped by the rounded corner. Keep all
  marks inside the margin.
- Emit no `<rect>` background fill — transparent SVG on the page's white is
  correct and keeps files small. (Author previews on white; the page is white.)

## Sizing

Author with an explicit `viewBox`; the page scales it down with
`max-width: 100%`. Use one of two nominal widths so line weights and type stay
consistent across figures:

| Class | `viewBox` width (units) | Use for |
|---|---|---|
| Single-column | ~460 | one narrow diagram, a single small chart |
| Double-column | ~900 | multi-panel figures, wide pipelines, format layouts |

Height is whatever the content needs at a sensible aspect ratio. Units are
abstract (they are not px, pt, or mm) — everything below is expressed in these
`viewBox` units so it scales together.

## Type

```
font-family: 'Inter', Arial, Helvetica, sans-serif;
```

Figures are referenced as `<img src="*.svg">`, so they render in isolation and
**cannot** inherit the page's Inter webfont. The fallback matters: Arial /
Helvetica *is Nature's real typeface*, so the degraded path is the
print-authentic one. Never rely on a font outside this stack; never embed a
base64 webfont (it bloats the file for no gain).

| Role | Size (units) | Weight | Color |
|---|---|---|---|
| Panel label (`a`, `b`, `c`) | 15 | 700 | ink `#1f2328` |
| Axis / node label | 13 | 500 | ink `#1f2328` |
| Tick label, small annotation | 11 | 400 | secondary `#59636e` |
| Monospace data (format figures) | 13 | 400 | ink, `ui-monospace, 'JetBrains Mono', Menlo, Consolas, monospace` |

- **Sentence case** for all of it. No ALL-CAPS except where the data itself is
  literal (e.g. a `CHROM` column header in a VCF, an `@` FASTQ identifier).
- Set `text-rendering="geometricPrecision"` on the root `<svg>`.

## Panels & labels

- Multi-panel figures get a **bold lowercase** label — `a`, `b`, `c` — in the
  **top-left** corner of each panel. This is the *Nature* convention. (Some
  existing captions use uppercase `(A)(B)(C)`; when you regenerate a figure,
  switch the figure to lowercase and update the caption to match.)
- Panels in a stack share the same left edge and x-scale so the reader can trace
  a vertical line across them.
- No box around a panel unless the box is load-bearing (e.g. it groups a legend).

## Marks

- **Axis lines: `0.75` units, color secondary `#59636e`.** Ticks point *outward*,
  length ~4 units. Show only the axes that carry meaning (a time series usually
  needs a baseline and a labeled y-axis, not a full frame).
- **No gridlines** unless a value must be read off precisely; if needed, use
  `#d0d7de` at `0.5` units, behind the data.
- **Data strokes: `1.5`–`2` units**, round line joins and caps.
- **Arrows** (workflows): single arrowhead via a shared `<marker>`, stroke
  `1.5` units in secondary or ink; keep heads small (~6 units).
- **Boxes / nodes** (workflows, format layouts): `1` unit stroke, `4`-unit corner
  radius, fill a 12%-opacity tint of the box's accent color (see palette.md), or
  none. Never a hard saturated fill behind dark text.
- Round coordinates to ≤2 decimals to keep files legible and small.

## Color

Full tokens, ordered categorical sequence, and colorblind-safe pairings are in
[palette.md](./palette.md). The short version:

- **Primary = site blue `#0969da`.** First data series, primary flow arrow,
  emphasis.
- Ink `#1f2328` for text and neutral structure; secondary `#59636e` for axes and
  quiet labels; rules `#d0d7de` for hairlines.
- Extend into `#d55e00 · #009e73 · #7d55c7 · #e69f00 · #56b4e9` **in that order**
  only when you need more categories. Don't reach for a color the figure doesn't
  need.

## For quantitative charts (family 3): defer to the `dataviz` skill

When a figure plots data (time series, distributions, AGP reports, trend lines),
**invoke the `dataviz` skill** and follow its mark specs and its palette
*validator* for color choices and contrast. This standard's palette is the
brand override to feed it: use `#0969da` as the primary and the ordered sequence
above as the categorical ramp, then let dataviz's rules govern legend, axis,
tooltip, and encoding decisions. The two are complementary — dataviz owns "how to
build a correct chart," this doc owns "how book figures look."

## Data honesty

If a chart shows **synthetic or illustrative** data (e.g. a stylized walking
accelerometer trace), say so in the `<figcaption>` ("Illustrative synthetic
data"). If it shows real measured or published data, cite the source in the
caption. Never present invented numbers as if measured.

## Accessibility

- Root `<svg>` gets `role="img"` and a `<title>` (concise) plus `<desc>` (fuller)
  as the first children — screen readers use these, and they complement the
  `alt` on the `<img>`.
- Never encode a distinction by color alone. Pair color with a direct label, a
  line style, or position so the figure survives grayscale and color blindness.
- Target ≥ 3:1 contrast for graphical marks against white and ≥ 4.5:1 for text
  (both satisfied by the ink/secondary tokens on white).

## Checklist before saving

- [ ] `viewBox` set; nominal width is ~460 or ~900; ≥12-unit internal margin.
- [ ] Font stack is exactly `'Inter', Arial, Helvetica, sans-serif` (+ mono stack
      for data glyphs).
- [ ] No title inside the figure; sentence case throughout.
- [ ] Colors drawn only from palette.md, primary anchored on `#0969da`.
- [ ] Panels labeled bold-lowercase top-left (if multi-panel).
- [ ] `role="img"` + `<title>`/`<desc>` present.
- [ ] No color-only encodings; grayscale-legible.
- [ ] Caption states data provenance (real vs. illustrative).
