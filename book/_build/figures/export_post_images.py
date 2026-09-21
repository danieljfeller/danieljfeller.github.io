#!/usr/bin/env python3
"""Export one post-ready PNG per chapter for LinkedIn (native image posts).

    python3 book/_build/figures/export_post_images.py

For each chapter in POSTS, rasterizes the chapter's hero figure with macOS
Quick Look (`qlmanage`, no extra installs), crops the square render back to the
SVG's own aspect ratio, adds a slim attribution footer, and writes
book/_promo/images/NN-<slug>.png at 1600 px wide. Chapters without a figure get
the share card. macOS only (qlmanage); Pillow required.
"""
import pathlib, re, shutil, subprocess, tempfile
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parents[3]
IMG = ROOT / "images/book"
OUT = ROOT / "book/_promo/images"
INK, SEC, RULE, BLUE = (31, 35, 40), (89, 99, 110), (208, 215, 222), (9, 105, 218)
W, PAD, FOOT = 1600, 56, 64

# (number, slug, chapter title, hero figure or None)
POSTS = [
    (1,  "introduction",              "Introduction",                                  None),
    (2,  "core-concepts",             "Core Concepts",                                 "icd10-code-structure"),
    (3,  "medical-claims",            "Medical Claims",                                "medical-claims-structure"),
    (4,  "pharmacy-claims",           "Pharmacy Claims",                               None),
    (5,  "ehr",                       "Electronic Health Records",                     "ecg-intervals-structured"),
    (6,  "medical-imaging",           "Medical Imaging",                               "dicom-hierarchy"),
    (7,  "clinical-trials",           "Clinical Trial Data",                           "ecrf-components"),
    (8,  "molecular-sequencing",      "Molecular Sequencing",                          "sequencing-pipeline"),
    (9,  "vital-signs",               "Vital Signs Monitoring",                        "cgm-agp-report"),
    (10, "adherence",                 "Adherence Monitoring Technology",               None),
    (11, "activity-lifestyle",        "Activity & Lifestyle",                          "accelerometer-axes"),
    (12, "patient-reported-outcomes", "Patient-Reported Outcomes",                     None),
    (13, "complex-unstructured",      "Complex & Unstructured Data",                   "pgd-structure-spectrum"),
    (14, "future",                    "The Patient-Generated Data of the Future",      "patient-generated-data-types"),
    (15, "de-identification",         "Methods to De-Identify Health Data",            None),
    (16, "multimodal-streams",        "Putting It All Together: Multimodal Data Streams", "multimodal-timeline"),
]

def font(size, bold=False):
    for path, idx in [("/System/Library/Fonts/Helvetica.ttc", 1 if bold else 0),
                      ("/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf", 0)]:
        try:
            return ImageFont.truetype(path, size, index=idx)
        except OSError:
            continue
    return ImageFont.load_default()

def viewbox(svg):
    m = re.search(r'viewBox="([\d.\s-]+)"', svg.read_text())
    x, y, w, h = map(float, m.group(1).split())
    return w, h

def rasterize(svg, size=1600):
    """Quick Look renders the SVG scaled to fit a size×size white square; crop it back."""
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(["qlmanage", "-t", "-s", str(size), "-o", td, str(svg)], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        png = next(pathlib.Path(td).glob("*.png"))
        im = Image.open(png).convert("RGB")
    w, h = viewbox(svg)
    scale = min(size / w, size / h)
    rw, rh = w * scale, h * scale
    x0, y0 = (size - rw) / 2, (size - rh) / 2
    return im.crop((int(x0), int(y0), int(x0 + rw), int(y0 + rh)))

def compose(fig, title):
    fig = fig.resize((W - 2 * PAD, int(fig.height * (W - 2 * PAD) / fig.width)), Image.LANCZOS)
    im = Image.new("RGB", (W, fig.height + 2 * PAD + FOOT), "white")
    im.paste(fig, (PAD, PAD))
    d = ImageDraw.Draw(im)
    y = fig.height + PAD + 8
    d.line([(PAD, y), (W - PAD, y)], fill=RULE, width=2)
    d.text((PAD, y + 18), f"The Health Data Handbook  ·  {title}", font=font(22, bold=True), fill=INK)
    f = font(22)
    url = "danieljfeller.github.io/book"
    d.text((W - PAD - d.textlength(url, font=f), y + 18), url, font=f, fill=BLUE)
    return im

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for n, slug, title, figure in POSTS:
        dest = OUT / f"{n:02d}-{slug}.png"
        if figure is None:
            shutil.copy(IMG / "social-card.png", dest)
            print(f"{dest.name:40s} share card (chapter has no figure)")
            continue
        im = compose(rasterize(IMG / f"{figure}.svg"), title)
        im.save(dest, optimize=True)
        print(f"{dest.name:40s} {im.size[0]}x{im.size[1]}  from {figure}.svg")

if __name__ == "__main__":
    main()
