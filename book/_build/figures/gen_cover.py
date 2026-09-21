#!/usr/bin/env python3
"""Render the book cover and the social-share card as PNGs.

    python3 book/_build/figures/gen_cover.py

Writes images/book/cover.png (1200x1600, 3:4) and images/book/social-card.png
(1200x630, the Open Graph size LinkedIn, Slack, and X all crop to). Both use
the site palette and a five-track "data streams" motif that echoes the book's
closing multimodal-timeline figure. Requires Pillow and the macOS Helvetica
font (falls back to Arial / DejaVu when absent).
"""
import math, pathlib, random
from PIL import Image, ImageDraw, ImageFont

OUT = pathlib.Path(__file__).resolve().parents[3] / "images/book"
INK, SEC, RULE, SURF = (31, 35, 40), (89, 99, 110), (208, 215, 222), (246, 248, 250)
BLUE, VERM, GREEN, PURPLE, AMBER = (9, 105, 218), (213, 94, 0), (0, 158, 115), (125, 85, 199), (230, 159, 0)

def font(size, bold=False, light=False):
    for path, idx in [("/System/Library/Fonts/Helvetica.ttc", 1 if bold else (4 if light else 0)),
                      ("/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf", 0),
                      ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 0)]:
        try:
            return ImageFont.truetype(path, size, index=idx)
        except OSError:
            continue
    return ImageFont.load_default()

def tint(c, a=0.12):
    return tuple(int(255 - (255 - ch) * a) for ch in c)

def streams(d, x0, y0, w, h, seed=5):
    """Five horizontal data tracks: fills, lab points, scores, a dense signal, and bars."""
    rnd = random.Random(seed)
    th = h / 5
    def X(f): return x0 + w * f
    # track 1: pharmacy fills (bars with a gap)
    y = y0 + th * 0.5
    for f in [0.02, 0.11, 0.20, 0.29, 0.50, 0.59, 0.68, 0.77, 0.86]:
        d.rounded_rectangle([X(f), y - th*0.16, X(f + 0.08), y + th*0.16], radius=4, fill=BLUE)
    # track 2: sparse lab values (dots joined by a dashed line)
    y = y0 + th * 1.5
    pts = [(X(0.04), y + th*0.22), (X(0.36), y + th*0.05), (X(0.62), y - th*0.1), (X(0.93), y - th*0.25)]
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        n = 14
        for i in range(0, n, 2):
            d.line([(ax + (bx-ax)*i/n, ay + (by-ay)*i/n), (ax + (bx-ax)*(i+1)/n, ay + (by-ay)*(i+1)/n)], fill=GREEN, width=3)
    for px, py in pts:
        d.ellipse([px-8, py-8, px+8, py+8], fill=GREEN)
    # track 3: questionnaire scores (step line)
    y = y0 + th * 2.5
    vals = [0.3, 0.3, 0.2, 0.2, 0.05, -0.05, -0.1, -0.2, -0.25, -0.28]
    pts = [(X(0.03 + 0.1*i), y + th*v) for i, v in enumerate(vals)]
    d.line(pts, fill=PURPLE, width=4, joint="curve")
    for px, py in pts:
        d.ellipse([px-6, py-6, px+6, py+6], fill=PURPLE)
    # track 4: dense continuous signal (CGM-like)
    y = y0 + th * 3.5
    pts = []
    for i in range(160):
        f = i / 159
        v = 0.25*math.sin(f*22) + 0.12*math.sin(f*61+1) + rnd.gauss(0, 0.03) - 0.25*f
        pts.append((X(f), y + th*0.35*v))
    d.line(pts, fill=AMBER, width=3, joint="curve")
    # track 5: weekly bars (steps)
    y = y0 + th * 4.5
    n = 40
    for i in range(n):
        f = i / n
        v = 0.55 + 0.25*math.sin(i/6) + rnd.gauss(0, 0.06)
        if 0.28 < f < 0.48: v -= 0.3
        bh = th * 0.75 * max(0.08, v)
        d.rectangle([X(f) + 2, y + th*0.4 - bh, X(f + 1/n) - 4, y + th*0.4], fill=tint(VERM, 0.75))

def wrap_title(d, lines, x, y, f, fill, gap=0.02):
    for line in lines:
        d.text((x, y), line, font=f, fill=fill)
        y += f.size * (1 + gap)
    return y

def cover():
    W, H = 1200, 1600
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 18], fill=BLUE)
    f_title = font(128, bold=True)
    y = wrap_title(d, ["The", "Health Data", "Handbook"], 96, 120, f_title, INK)
    f_sub = font(38, light=True)
    d.text((100, y + 30), "A Practical Guide From Genomics", font=f_sub, fill=SEC)
    d.text((100, y + 80), "to EHRs to Insurance Claims", font=f_sub, fill=SEC)
    # motif panel
    px0, py0, pw, ph = 96, 760, W - 192, 560
    d.rounded_rectangle([px0, py0, px0 + pw, py0 + ph], radius=14, fill=SURF, outline=RULE, width=2)
    labels = ["Claims", "Labs", "Patient-reported", "Devices", "Activity"]
    f_lab = font(22)
    th = ph / 5
    for i, lab in enumerate(labels):
        d.text((px0 + 28, py0 + th*i + th*0.5 - 13), lab, font=f_lab, fill=SEC)
        if i: d.line([(px0 + 24, py0 + th*i), (px0 + pw - 24, py0 + th*i)], fill=RULE, width=1)
    streams(d, px0 + 260, py0 + 16, pw - 300, ph - 32)
    # author + url
    f_auth = font(52, bold=True)
    d.text((100, 1400), "Daniel Feller, PhD", font=f_auth, fill=INK)
    f_url = font(26)
    d.text((100, 1470), "danieljfeller.github.io/book", font=f_url, fill=BLUE)
    d.text((100, 1506), "Free to read online  ·  CC BY-NC 4.0", font=f_url, fill=SEC)
    im.save(OUT / "cover.png", optimize=True)

def social():
    W, H = 1200, 630
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 14, H], fill=BLUE)
    f_kicker = font(22, bold=True)
    d.text((72, 64), "FREE ONLINE BOOK", font=f_kicker, fill=BLUE)
    f_title = font(84, bold=True)
    y = wrap_title(d, ["The Health Data", "Handbook"], 68, 100, f_title, INK)
    f_sub = font(30, light=True)
    d.text((72, y + 22), "A practical guide from genomics to EHRs", font=f_sub, fill=SEC)
    d.text((72, y + 62), "to insurance claims, for data people.", font=f_sub, fill=SEC)
    f_auth = font(30, bold=True)
    d.text((72, 500), "Daniel Feller, PhD", font=f_auth, fill=INK)
    f_url = font(24)
    d.text((72, 546), "danieljfeller.github.io/book", font=f_url, fill=BLUE)
    # motif at right
    px0, py0, pw, ph = 760, 70, 380, 490
    d.rounded_rectangle([px0, py0, px0 + pw, py0 + ph], radius=12, fill=SURF, outline=RULE, width=2)
    th = ph / 5
    for i in range(1, 5):
        d.line([(px0 + 16, py0 + th*i), (px0 + pw - 16, py0 + th*i)], fill=RULE, width=1)
    streams(d, px0 + 24, py0 + 14, pw - 48, ph - 28, seed=9)
    im.save(OUT / "social-card.png", optimize=True)

if __name__ == "__main__":
    cover(); social()
    print("wrote", OUT / "cover.png", "and", OUT / "social-card.png")
