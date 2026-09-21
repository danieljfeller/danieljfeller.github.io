#!/usr/bin/env python3
"""Generate two quantitative book figures (family 3) as SVG with synthetic data.

    python3 book/_build/figures/gen_ecg_and_timeline.py

Writes images/book/ecg-intervals-structured.svg and
images/book/multimodal-timeline.svg. Deterministic; no dependencies.
Palette and type follow .claude/skills/health-data-figure/references/.
"""
import math, pathlib, random

OUT = pathlib.Path(__file__).resolve().parents[3] / "images/book"
INK, SEC, RULE, BLUE, VERM, GREEN, PURPLE, AMBER = "#1f2328", "#59636e", "#d0d7de", "#0969da", "#d55e00", "#009e73", "#7d55c7", "#e69f00"
FONT = "'Inter', Arial, Helvetica, sans-serif"
MONO = "ui-monospace, 'JetBrains Mono', Menlo, Consolas, monospace"

def head(w, h, title, desc):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}"\n'
            f'     role="img" text-rendering="geometricPrecision"\n'
            f'     font-family="{FONT}">\n  <title>{title}</title>\n  <desc>{desc}</desc>\n')

def path(pts, color, width=1.5, dash=None):
    d = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    return f'  <path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linejoin="round" stroke-linecap="round"{extra}/>\n'

def text(x, y, s, size=11, color=SEC, weight=400, anchor="start", mono=False):
    fam = f' font-family="{MONO}"' if mono else ""
    return f'  <text x="{x:.2f}" y="{y:.2f}" font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}"{fam}>{s}</text>\n'

def gauss(t, mu, sig, amp):
    return amp * math.exp(-0.5 * ((t - mu) / sig) ** 2)

# ---------------------------------------------------------------- ECG ---
def ecg_beat(t):
    """One beat, t in seconds within the RR interval (0.833 s at 72 bpm). mV."""
    v = 0.0
    v += gauss(t, 0.12, 0.022, 0.15)            # P wave (onset ~0.06)
    v += gauss(t, 0.27, 0.006, -0.12)           # q
    v += gauss(t, 0.285, 0.010, 1.10)           # R
    v += gauss(t, 0.305, 0.008, -0.28)          # s
    v += gauss(t, 0.56, 0.045, 0.30)            # T wave (ends ~0.66)
    return v

def ecg_svg():
    W, H = 900, 420
    s = head(W, H, "What the EHR keeps from an ECG",
             "Panel a shows a ten-second single-lead ECG waveform. Panel b enlarges one beat with the PR interval, "
             "QRS duration, and QT interval bracketed, beside a box listing the few measured values and the interpretation "
             "text that reach the structured EHR record. Synthetic waveform.")
    # ---- panel a: 10 s strip ----
    x0, x1, yb = 60, 880, 120
    rr, fs = 60/72, 500
    n = int(10 * fs)
    pts = []
    rnd = random.Random(7)
    for i in range(0, n, 3):                      # draw every 3rd sample; keeps the file small
        t = i / fs
        v = ecg_beat(t % rr) + 0.012 * math.sin(2*math.pi*0.25*t) + rnd.gauss(0, 0.006)
        pts.append((x0 + (x1-x0) * t/10, yb - v * 60))
    s += text(24, 40, "a", 15, INK, 700)
    s += text(44, 40, "Full waveform: one lead, 10 s at 500 Hz. Lives in the cardiology information system (e.g., MUSE), not the EHR database.", 12, INK, 500)
    s += path(pts, BLUE, 1.2)
    s += f'  <line x1="{x0}" y1="{yb+40}" x2="{x1}" y2="{yb+40}" stroke="{SEC}" stroke-width="0.75"/>\n'
    for sec in range(0, 11, 2):
        x = x0 + (x1-x0)*sec/10
        s += f'  <line x1="{x:.1f}" y1="{yb+40}" x2="{x:.1f}" y2="{yb+44}" stroke="{SEC}" stroke-width="0.75"/>\n'
        s += text(x, yb+58, f"{sec} s", 11, SEC, anchor="middle")
    # mV scale bar
    s += f'  <line x1="{x0-14}" y1="{yb}" x2="{x0-14}" y2="{yb-60}" stroke="{SEC}" stroke-width="0.75"/>\n'
    s += text(x0-18, yb-24, "1 mV", 10, SEC, anchor="end")
    # ---- panel b: one beat enlarged ----
    bx0, bx1, byb = 60, 520, 330
    tb0, tb1 = 0.02, 0.78
    bp = []
    for i in range(400):
        t = tb0 + (tb1-tb0)*i/399
        bp.append((bx0 + (bx1-bx0)*(t-tb0)/(tb1-tb0), byb - ecg_beat(t)*95))
    def bx(t): return bx0 + (bx1-bx0)*(t-tb0)/(tb1-tb0)
    s += text(24, 215, "b", 15, INK, 700)
    s += text(44, 215, "One beat, enlarged: the intervals that are measured", 12, INK, 500)
    s += path(bp, BLUE, 1.6)
    # brackets: PR (P onset 0.065 -> QRS onset 0.262), QRS (0.262 -> 0.322), QT (0.262 -> 0.665)
    def bracket(t_a, t_b, y, label, ms, color=INK):
        xa, xb = bx(t_a), bx(t_b)
        out = f'  <path d="M {xa:.1f} {y-6} L {xa:.1f} {y} L {xb:.1f} {y} L {xb:.1f} {y-6}" fill="none" stroke="{color}" stroke-width="1"/>\n'
        out += text((xa+xb)/2, y+14, f"{label} {ms} ms", 11, INK, 600, "middle")
        return out
    s += bracket(0.065, 0.262, byb+28, "PR", 160)
    s += bracket(0.262, 0.322, byb+58, "QRS", 92)
    s += bracket(0.262, 0.665, byb+88, "QT", 380)
    # wave labels
    s += text(bx(0.12), byb-30, "P", 11, SEC, anchor="middle")
    s += text(bx(0.285)+8, byb-98, "R", 11, SEC)
    s += text(bx(0.56), byb-42, "T", 11, SEC, anchor="middle")
    # ---- structured record box ----
    rx, ry, rw, rh = 566, 230, 314, 168
    s += f'  <rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="4" fill="{GREEN}" fill-opacity="0.12" stroke="{GREEN}" stroke-width="1"/>\n'
    s += text(rx+14, ry+22, "What reaches the structured EHR record", 12, INK, 600)
    rows = [("Heart rate", "72 bpm"), ("PR interval", "160 ms"), ("QRS duration", "92 ms"), ("QT / QTc", "380 / 410 ms")]
    for i, (k, v) in enumerate(rows):
        y = ry + 46 + i*20
        s += text(rx+14, y, k, 11, SEC)
        s += text(rx+rw-14, y, v, 11, INK, 500, "end", mono=True)
    s += f'  <line x1="{rx+14}" y1="{ry+130}" x2="{rx+rw-14}" y2="{ry+130}" stroke="{RULE}" stroke-width="0.75"/>\n'
    s += text(rx+14, ry+148, "Interpretation (free text):", 11, SEC)
    s += text(rx+14, ry+160, "“Normal sinus rhythm. No acute ST changes.”", 10, INK, mono=True)
    # arrow from brackets to box
    s += f'  <path d="M 528 {byb+70} L 556 {byb+70}" stroke="{SEC}" stroke-width="1.5" fill="none" marker-end="url(#arrow)"/>\n'
    s = s.replace("  <title>", '  <defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 1 L 9 5 L 0 9 z" fill="#59636e"/></marker></defs>\n  <title>', 1)
    s += "</svg>\n"
    (OUT / "ecg-intervals-structured.svg").write_text(s)

# ----------------------------------------------------------- Timeline ---
def timeline_svg():
    W, H = 900, 470
    s = head(W, H, "Twelve months of data for one patient, one stream per track",
             "Five stacked tracks over January to December: SSRI fills from pharmacy claims with a gap in late March "
             "through mid May, hemoglobin A1c from EHR labs falling from 8.4 to 7.6 percent, PHQ-9 scores falling from 16 "
             "to 8 with a plateau during the gap, CGM time in range rising from 52 to 68 percent, and average daily steps "
             "dipping in the spring. A shaded band marks the adherence gap across all tracks. Synthetic data.")
    x0, x1 = 210, 870
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    def xd(day):  # day of year 0..365
        return x0 + (x1-x0)*day/365
    mstart = [0,31,59,90,120,151,181,212,243,273,304,334,365]
    tracks = [("Pharmacy claims", "SSRI fills (30-day supply)"),
              ("EHR labs", "Hemoglobin A1c (%)"),
              ("Patient-reported", "PHQ-9 depression score"),
              ("Patient-generated", "CGM time in range (%)"),
              ("Patient-generated", "Wearable: avg daily steps")]
    top, th, gap = 40, 66, 12
    # adherence gap band (Mar 20 - May 18)
    gx0, gx1 = xd(79), xd(138)
    s += f'  <rect x="{gx0:.1f}" y="{top-14}" width="{gx1-gx0:.1f}" height="{5*(th+gap)+4}" fill="{AMBER}" fill-opacity="0.12"/>\n'
    s += text((gx0+gx1)/2, top-18, "Adherence gap seen in claims", 11, "#9a6a00", 600, "middle")
    for i, (src, name) in enumerate(tracks):
        ty = top + i*(th+gap)
        yb = ty + th  # baseline
        s += text(24, ty+16, src, 10, SEC, 600)
        s += text(24, ty+32, name, 11, INK, 500)
        s += f'  <line x1="{x0}" y1="{yb}" x2="{x1}" y2="{yb}" stroke="{RULE}" stroke-width="0.75"/>\n'
        if i == 0:
            fills = [3, 33, 63, 79, 138, 168, 198, 228, 258, 288, 318, 348]
            for f in fills:
                s += f'  <rect x="{xd(f):.1f}" y="{yb-22}" width="{xd(f+30)-xd(f):.1f}" height="14" rx="2" fill="{BLUE}" fill-opacity="0.85"/>\n'
            s += text(xd(105), yb-28, "no fills", 10, VERM, 600, "middle")
        elif i == 1:
            pts = [(12, 8.4), (190, 8.0), (285, 7.6)]
            def ya(v): return yb - (v-7.2)/(8.8-7.2)*(th-16)
            s += path([(xd(d), ya(v)) for d, v in pts], BLUE, 1.5, dash="3 3")
            for d, v in pts:
                s += f'  <circle cx="{xd(d):.1f}" cy="{ya(v):.1f}" r="3.5" fill="{BLUE}"/>\n'
                s += text(xd(d)+8, ya(v)-6, f"{v}%", 10, INK, mono=True)
        elif i == 2:
            pts = [(40, 16), (100, 15), (135, 11), (220, 8), (310, 7)]
            def yp(v): return yb - (v-4)/(20-4)*(th-16)
            s += path([(xd(d), yp(v)) for d, v in pts], BLUE, 1.5)
            for d, v in pts:
                s += f'  <circle cx="{xd(d):.1f}" cy="{yp(v):.1f}" r="3.5" fill="{BLUE}"/>\n'
                s += text(xd(d)+7, yp(v)-6, str(v), 10, INK, mono=True)
            s += text(xd(100), yb-52, "stalls", 10, VERM, 600, "middle")
        elif i == 3:
            rnd = random.Random(3)
            pts = []
            for w in range(52):
                d = w*7+3
                base = 52 + 16*(1/(1+math.exp(-(d-200)/60)))
                if 79 <= d <= 138: base -= 5
                pts.append((xd(d), yb - (base + rnd.gauss(0,1.5) - 40)/(80-40)*(th-16)))
            s += path(pts, BLUE, 1.5)
            s += text(xd(3)+2, yb-4, "52%", 10, INK, mono=True)
            s += text(xd(360)-2, yb-46, "68%", 10, INK, mono=True, anchor="end")
        elif i == 4:
            rnd = random.Random(11)
            for w in range(52):
                d = w*7
                v = 6200 + 900*math.sin(w/8) + rnd.gauss(0, 350)
                if 79 <= d <= 138: v -= 2000
                if d > 200: v += 600
                h = (v-2000)/(9000-2000)*(th-16)
                s += f'  <rect x="{xd(d):.1f}" y="{yb-h:.1f}" width="{(x1-x0)/52-1.5:.1f}" height="{h:.1f}" fill="{BLUE}" fill-opacity="0.55"/>\n'
    # month axis
    ay = top + 5*(th+gap) + 2
    s += f'  <line x1="{x0}" y1="{ay}" x2="{x1}" y2="{ay}" stroke="{SEC}" stroke-width="0.75"/>\n'
    for m in range(12):
        xm = xd(mstart[m])
        s += f'  <line x1="{xm:.1f}" y1="{ay}" x2="{xm:.1f}" y2="{ay+4}" stroke="{SEC}" stroke-width="0.75"/>\n'
        s += text((xd(mstart[m])+xd(mstart[m+1]))/2, ay+18, months[m], 11, SEC, anchor="middle")
    s += "</svg>\n"
    (OUT / "multimodal-timeline.svg").write_text(s)

if __name__ == "__main__":
    ecg_svg(); timeline_svg()
    print("wrote", OUT / "ecg-intervals-structured.svg", "and", OUT / "multimodal-timeline.svg")
