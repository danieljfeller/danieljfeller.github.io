# Palette — *The Health Data Handbook* figures

Colorblind-safe, site-anchored. These are the **only** colors a figure may use.
Where a token overlaps the website, its value mirrors `assets/css/main.css`
`:root` so figures sit natively on the page.

## Structural tokens

| Token | Hex | Role |
|---|---|---|
| Ink | `#1f2328` | Text, neutral structure, primary data on white |
| Secondary | `#59636e` | Axes, ticks, quiet labels, secondary structure |
| Rule | `#d0d7de` | Hairlines, gridlines (when unavoidable), box strokes |
| Surface tint | `#f6f8fa` | Subtle panel/zone fill when a fill is needed |
| Canvas | `#ffffff` | Background (page is white; usually leave transparent) |

## Categorical sequence (use in this order)

Add a color only when the figure needs another category. Series 1 is the site
blue; the rest are an Okabe–Ito-derived, colorblind-safe set adjusted to sit
beside it.

| # | Name | Hex | Notes |
|---|---|---|---|
| 1 | Primary blue | `#0969da` | Site accent. First series, primary flow, emphasis. |
| 2 | Vermillion | `#d55e00` | Strong contrast to blue for red-green-safe pairs. |
| 3 | Green | `#009e73` | |
| 4 | Purple | `#7d55c7` | |
| 5 | Amber | `#e69f00` | |
| 6 | Sky | `#56b4e9` | Use late; can read close to primary blue at small sizes. |

**Tints:** for a box/zone fill behind dark text, use the series color at ~12%
opacity (`fill-opacity="0.12"`), never the solid color.

## Colorblind-safe pairings

When two series must be told apart, prefer these pairs (each survives deuteran-,
protan-, and tritan-type color vision) — and still add a non-color cue (label,
dash pattern, position):

- Primary blue `#0969da` + Vermillion `#d55e00`  ← best 2-series default
- Primary blue `#0969da` + Amber `#e69f00`
- Vermillion `#d55e00` + Green `#009e73` (pair with dash/label; safe but close for some)
- Ink `#1f2328` + Primary blue `#0969da` (neutral vs. emphasis)

Avoid Green `#009e73` + Vermillion `#d55e00` as the *only* distinction without a
second cue.

## Validating a palette choice

For any figure that plots data, **invoke the `dataviz` skill** and run its
palette *validator* against the subset of colors you use, feeding `#0969da` as
the brand primary and the sequence above as the categorical ramp. Treat its
contrast/CVD output as authoritative for charts. For non-data diagrams
(workflows, format layouts), the pairings above are sufficient.

## Quick contrast facts (on white `#ffffff`)

- Ink `#1f2328` — ~15.9:1 (text ✓, marks ✓)
- Secondary `#59636e` — ~4.8:1 (text ✓ at body size, marks ✓)
- Primary `#0969da` — ~4.4:1 (marks ✓; ok for large/bold text, thin small text is borderline)
- Vermillion `#d55e00` — ~3.6:1 (marks ✓; not for small text)

Rule of thumb: use ink or secondary for anything that must be *read*; use the
categorical colors for *marks* (lines, fills, arrowheads), labeled in ink.
