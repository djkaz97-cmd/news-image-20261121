"""Render the news-image-20261121 entry: a one-page newspaper front page
summing up the world's news of Saturday 21 November 2026.

Build-time only. The repository ships the rendered entry.png; main.ts just
copies it. Uses Windows system fonts (Georgia, Arial Bold, Impact) and Pillow.
Deterministic: fixed seed, no clock, no network.
"""

import datetime
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- canvas ---
W = H = 1024
M = 32                      # page margin
CW = W - 2 * M              # content width (960)

PAPER = (247, 242, 231)
INK = (15, 52, 61)          # deep teal
INK_SOFT = (62, 94, 102)
ACCENT = (224, 122, 38)     # orange
ACCENT_DEEP = (191, 96, 22)
CARD_BG = (252, 249, 241)
HAIRLINE = (168, 182, 182)
CREAM = (247, 242, 231)

FONTS = Path("C:/Windows/Fonts")
DAY = datetime.date(2026, 11, 21)
DOY = DAY.timetuple().tm_yday          # no. 325


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONTS / name), size)


def lerp(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def gradient(stops, t):
    """stops: list of (position, rgb); piecewise-linear colour at t in [0,1]."""
    for (p0, c0), (p1, c1) in zip(stops, stops[1:]):
        if t <= p1:
            return lerp(c0, c1, (t - p0) / (p1 - p0))
    return stops[-1][1]


def wrap(text, fnt, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if fnt.getlength(trial) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_size(text, name, maxw, start, minimum=12):
    s = start
    while s > minimum and font(name, s).getlength(text) > maxw:
        s -= 1
    return s


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ------------------------------------------------------------- masthead ----
d.text((M, 30), "WORLD EDITION", font=font("arialbd.ttf", 15), fill=INK_SOFT)
d.text((W - M, 30), "ONE DAY · ONE PAGE", font=font("arialbd.ttf", 15),
       fill=INK_SOFT, anchor="ra")
d.line([(M, 52), (W - M, 52)], fill=HAIRLINE, width=1)

mast = font("georgiab.ttf", 80)
d.text((W // 2, 100), "THE WORLD LEDGER", font=mast, fill=INK, anchor="mm")
d.line([(M, 148), (W - M, 148)], fill=INK, width=3)
d.line([(M, 154), (W - M, 154)], fill=INK, width=1)

# date band — the day, named large
band_y0, band_y1 = 164, 212
d.rectangle([M, band_y0, W - M, band_y1], fill=INK)
date_txt = DAY.strftime("%A, %d %B %Y").upper()
ds = fit_size(date_txt, "arialbd.ttf", 560, 30)
d.text((W // 2, (band_y0 + band_y1) // 2), date_txt,
       font=font("arialbd.ttf", ds), fill=CREAM, anchor="mm")
d.text((M + 14, (band_y0 + band_y1) // 2), f"VOL. 126 · NO. {DOY}",
       font=font("arialbd.ttf", 13), fill=(178, 196, 198), anchor="lm")
d.text((W - M - 14, (band_y0 + band_y1) // 2), "24-HOUR REVIEW",
       font=font("arialbd.ttf", 13), fill=(178, 196, 198), anchor="rm")

# ------------------------------------------------------------- lead story --
d.rectangle([M, 230, M + 10, 240], fill=ACCENT)
d.text((M + 20, 226), "LEAD STORY — ENTERTAINMENT & GAMING",
       font=font("arialbd.ttf", 17), fill=ACCENT_DEEP)

hl = "GTA VI LAUNCHES WORLDWIDE"
hs = fit_size(hl, "impact.ttf", CW, 74)
hf = font("impact.ttf", hs)
part1 = "GTA VI "
w1 = hf.getlength(part1)
d.text((M, 248), part1, font=hf, fill=ACCENT_DEEP)
d.text((M + w1, 248), hl[len(part1):], font=hf, fill=INK)

deck = ("Rockstar's sequel arrives 13 years after GTA V, with launch-day "
        "queues from Tokyo to London as players worldwide log on and the "
        "series returns to Vice City.")
df = font("georgia.ttf", 21)
for i, line in enumerate(wrap(deck, df, CW)):
    d.text((M, 334 + i * 27), line, font=df, fill=INK_SOFT)

# ---------------------------------------------------------- illustration ---
IX, IY, IW, IH = M, 392, CW, 208
ill = Image.new("RGB", (IW, IH))
pd = ImageDraw.Draw(ill)
rng = random.Random(21)
HORIZON = 138

# dusk sky
sky_stops = [(0.0, (12, 42, 56)), (0.55, (36, 86, 98)),
             (0.85, (196, 120, 64)), (1.0, (240, 150, 70))]
for y in range(HORIZON):
    pd.line([(0, y), (IW, y)], fill=gradient(sky_stops, y / HORIZON))

# retrowave sun: horizontal slices with gaps in the lower half
SCX, SCY, SR = 610, 112, 62
gaps = [(14, 19), (30, 36), (46, 53)]
for dy in range(-SR, SR + 1):
    if any(a <= dy <= b for a, b in gaps):
        continue
    hw = int(math.sqrt(max(SR * SR - dy * dy, 0)))
    col = lerp((255, 222, 132), (240, 118, 44), (dy + SR) / (2 * SR))
    pd.line([(SCX - hw, SCY + dy), (SCX + hw, SCY + dy)], fill=col)

# skyline silhouette with a few lit windows
bld = [(0, 46, 34), (52, 30, 52), (88, 40, 26), (134, 26, 60), (166, 44, 40),
       (216, 30, 24), (252, 52, 66), (310, 34, 36), (350, 46, 54),
       (402, 28, 30), (436, 50, 72), (492, 36, 42), (534, 44, 58),
       (584, 30, 32), (620, 48, 64), (674, 34, 40), (714, 44, 26),
       (764, 52, 58), (822, 30, 36), (858, 46, 68), (910, 50, 44)]
SIL = (11, 38, 48)
for x, bw, bh in bld:
    pd.rectangle([x, HORIZON - bh, x + bw, HORIZON], fill=SIL)
    if bh >= 40:
        for wy in range(HORIZON - bh + 6, HORIZON - 6, 9):
            for wx in range(x + 5, x + bw - 4, 8):
                if rng.random() < 0.28:
                    pd.rectangle([wx, wy, wx + 2, wy + 3], fill=(255, 196, 100))
# antennas
for x, bw, bh in bld:
    if bh >= 60:
        pd.line([(x + bw // 2, HORIZON - bh), (x + bw // 2, HORIZON - bh - 12)],
                fill=SIL, width=2)

# water with sun reflection
for y in range(HORIZON, IH):
    t = (y - HORIZON) / (IH - HORIZON)
    pd.line([(0, y), (IW, y)], fill=lerp((14, 44, 56), (8, 30, 42), t))
for y in range(HORIZON + 5, IH - 12, 4):
    depth = (y - HORIZON) / (IH - HORIZON)
    sw = int((SR * 1.5) * (0.45 + rng.random() * 0.75) * (1 - depth * 0.45))
    col = lerp((240, 140, 60), (20, 54, 64), depth * 0.9)
    off = rng.randint(-10, 10)
    pd.rectangle([SCX - sw // 2 + off, y, SCX + sw // 2 + off, y + 2], fill=col)

# foreground shore
pd.rectangle([0, IH - 16, IW, IH], fill=(8, 30, 40))


def palm(x0, base_y, height, lean, scale=1.0):
    top_x, top_y = x0 + lean, base_y - height
    # tapered, slightly curved trunk
    steps = 14
    for i in range(steps):
        t0, t1 = i / steps, (i + 1) / steps
        p0 = (x0 + lean * t0 * t0, base_y - height * t0)
        p1 = (x0 + lean * t1 * t1, base_y - height * t1)
        pd.line([p0, p1], fill=(8, 30, 40), width=max(2, int((8 - 5 * t0) * scale)))
    # fronds: quadratic curves arcing out and drooping
    for ang in (-175, -140, -105, -70, -35, 0, 25):
        a = math.radians(ang)
        ln = rng.uniform(46, 62) * scale
        cx = top_x + math.cos(a) * ln * 0.55
        cy = top_y + math.sin(a) * ln * 0.55 - ln * 0.20
        ex = top_x + math.cos(a) * ln
        ey = top_y + math.sin(a) * ln * 0.30 + 16 * scale
        pts = []
        for i in range(13):
            t = i / 12
            pts.append(((1 - t) ** 2 * top_x + 2 * (1 - t) * t * cx + t * t * ex,
                        (1 - t) ** 2 * top_y + 2 * (1 - t) * t * cy + t * t * ey))
        pd.line(pts, fill=(8, 30, 40), width=max(2, int(3.5 * scale)), joint="curve")
    for dx, dy in ((-3, 2), (3, 3), (0, 6)):
        pd.ellipse([top_x + dx - 2, top_y + dy - 2, top_x + dx + 2, top_y + dy + 2],
                   fill=(8, 30, 40))


palm(84, IH - 12, 112, 16, 1.05)
palm(158, IH - 10, 78, -10, 0.8)
palm(878, IH - 12, 122, -18, 1.1)
palm(934, IH - 10, 66, 8, 0.7)

# distant birds
for bx, by in ((210, 38), (252, 52), (300, 30)):
    pd.line([(bx - 7, by), (bx, by + 4), (bx + 7, by)], fill=(20, 50, 60), width=2)

img.paste(ill, (IX, IY))
d.rectangle([IX - 2, IY - 2, IX + IW + 1, IY + IH + 1], outline=INK, width=2)
d.text((M, IY + IH + 8),
       "Vice City at dusk — the neon coast where Rockstar's sequel is set.",
       font=font("georgiai.ttf", 15), fill=INK_SOFT)

# ------------------------------------------------------------- divider -----
div_y = 636
label = "MORE OF THE DAY'S NEWS"
lf = font("arialbd.ttf", 15)
lw = lf.getlength(label)
d.line([(M, div_y), (W // 2 - lw / 2 - 16, div_y)], fill=HAIRLINE, width=1)
d.line([(W // 2 + lw / 2 + 16, div_y), (W - M, div_y)], fill=HAIRLINE, width=1)
d.text((W // 2, div_y), label, font=lf, fill=INK_SOFT, anchor="mm")

# ------------------------------------------------------------- story cards -
CARD_W, CARD_H, GAP_X, GAP_Y = 306, 128, 21, 12
GRID_Y = 654


def star(cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill)


def icon_mercury(x, y):
    d.ellipse([x + 2, y + 8, x + 32, y + 28], outline=INK, width=2)
    d.ellipse([x + 9, y + 11, x + 25, y + 27], fill=ACCENT)
    d.rectangle([x + 27, y + 3, x + 31, y + 7], fill=INK)


def icon_tennis(x, y):
    d.ellipse([x + 4, y + 4, x + 30, y + 30], fill=(232, 176, 80),
              outline=INK, width=2)
    d.arc([x - 8, y + 2, x + 20, y + 32], 300, 60, fill=PAPER, width=2)
    d.arc([x + 14, y + 2, x + 42, y + 32], 120, 240, fill=PAPER, width=2)


def icon_climate(x, y):
    d.rounded_rectangle([x + 13, y + 2, x + 21, y + 22], 4, fill=PAPER,
                        outline=INK, width=2)
    d.line([(x + 17, y + 10), (x + 17, y + 22)], fill=ACCENT, width=4)
    d.ellipse([x + 11, y + 18, x + 23, y + 30], fill=ACCENT, outline=INK, width=2)
    for ang in (200, 245, 290):
        a = math.radians(ang)
        d.line([(x + 28 + 4 * math.cos(a), y + 8 + 4 * math.sin(a)),
                (x + 28 + 8 * math.cos(a), y + 8 + 8 * math.sin(a))],
               fill=ACCENT_DEEP, width=2)


def icon_stars(x, y):
    d.ellipse([x + 2, y + 2, x + 32, y + 32], fill=INK)
    for i in range(12):
        a = -math.pi / 2 + i * math.pi / 6
        star(x + 17 + 10.5 * math.cos(a), y + 17 + 10.5 * math.sin(a), 2.4,
             (240, 200, 90))


def icon_markets(x, y):
    for gy in (8, 16, 24):
        d.line([(x + 2, y + gy), (x + 32, y + gy)], fill=HAIRLINE, width=1)
    pts = [(x + 3, y + 7), (x + 11, y + 13), (x + 17, y + 9),
           (x + 25, y + 21), (x + 30, y + 26)]
    d.line(pts, fill=ACCENT_DEEP, width=3, joint="curve")
    d.polygon([(x + 31, y + 27), (x + 24, y + 25), (x + 28, y + 20)],
              fill=ACCENT_DEEP)


def icon_cricket(x, y):
    for sx in (9, 15, 21):
        d.line([(x + sx, y + 8), (x + sx, y + 29)], fill=INK, width=3)
    d.line([(x + 8, y + 6), (x + 16, y + 6)], fill=ACCENT_DEEP, width=2)
    d.line([(x + 14, y + 6), (x + 22, y + 6)], fill=ACCENT_DEEP, width=2)
    d.ellipse([x + 24, y + 21, x + 32, y + 29], fill=ACCENT)
    d.arc([x + 24, y + 21, x + 32, y + 29], 120, 300, fill=PAPER, width=1)


CARDS = [
    ("SCIENCE", "BepiColombo enters Mercury orbit",
     "ESA–JAXA probe arrives after an eight-year cruise.", icon_mercury),
    ("TENNIS", "Alcaraz unbeaten at ATP Finals",
     "Spaniard perfect through the week in Turin.", icon_tennis),
    ("CLIMATE", "COP31 summit goes to overtime",
     "Antalya talks run past deadline; finance text open.", icon_climate),
    ("DIPLOMACY", "UK–EU sign new agreements",
     "Post-Brexit accords sealed in Brussels.", icon_stars),
    ("MARKETS", "AI chip selloff hits S&P 500",
     "Index slides into correction as tech shares fall.", icon_markets),
    ("CRICKET", "India–NZ test goes to the wire",
     "Final day looms with the result wide open.", icon_cricket),
]

hf_card = font("arialbd.ttf", 22)
df_card = font("georgia.ttf", 16)
for i, (label_c, head, deck_c, icon) in enumerate(CARDS):
    cx = M + (i % 3) * (CARD_W + GAP_X)
    cy = GRID_Y + (i // 3) * (CARD_H + GAP_Y)
    d.rectangle([cx, cy, cx + CARD_W, cy + CARD_H], fill=CARD_BG,
                outline=HAIRLINE, width=1)
    d.rectangle([cx, cy, cx + 6, cy + CARD_H], fill=ACCENT)
    d.text((cx + 18, cy + 11), label_c, font=font("arialbd.ttf", 13),
           fill=ACCENT_DEEP)
    icon(cx + CARD_W - 46, cy + 8)
    hl_lines = wrap(head, hf_card, CARD_W - 36)[:2]
    for j, ln in enumerate(hl_lines):
        d.text((cx + 18, cy + 32 + j * 25), ln, font=hf_card, fill=INK)
    dk_lines = wrap(deck_c, df_card, CARD_W - 36)[:2]
    for j, ln in enumerate(dk_lines):
        d.text((cx + 18, cy + 86 + j * 18), ln, font=df_card, fill=INK_SOFT)

# ---------------------------------------------------------------- ticker ---
TY0, TY1 = 938, 982
d.rectangle([M, TY0, W - M, TY1], fill=INK)
d.rectangle([M, TY0, M + 148, TY1], fill=ACCENT)
d.text((M + 74, (TY0 + TY1) // 2), "NEWS TICKER", font=font("arialbd.ttf", 17),
       fill=CREAM, anchor="mm")
items = ["F1: VEGAS GP UNDER THE LIGHTS", "GTA VI: QUEUES WORLDWIDE",
         "COP31: TALKS IN OVERTIME"]
sep = "   ///   "
tick_txt = sep.join(items)
avail = CW - 148 - 28
ts = fit_size(tick_txt, "arialbd.ttf", avail, 18, minimum=13)
tf = font("arialbd.ttf", ts)
# draw with orange separators
xx = M + 148 + 16
mid = (TY0 + TY1) // 2
pad = tf.getlength("   ")
for k, item in enumerate(items):
    if k:
        xx += pad
        d.text((xx, mid), "///", font=tf, fill=ACCENT, anchor="lm")
        xx += tf.getlength("///") + pad
    d.text((xx, mid), item, font=tf, fill=CREAM, anchor="lm")
    xx += tf.getlength(item)

# ---------------------------------------------------------------- footer ---
d.line([(M, 996), (W - M, 996)], fill=HAIRLINE, width=1)
d.text((M, 1003),
       "The World Ledger — a one-page summary of the world's news on "
       "Saturday, 21 November 2026.",
       font=font("georgiai.ttf", 14), fill=INK_SOFT)
d.text((W - M, 1003), "21 NOV 2026 · PAGE 01", font=font("arialbd.ttf", 14),
       fill=INK, anchor="ra")

# ------------------------------------------------------------------ save ---
OUT = Path(__file__).resolve().parent.parent / "entry.png"
img.save(OUT, "PNG", optimize=True)
print(f"saved {OUT} ({OUT.stat().st_size} bytes, {img.size[0]}x{img.size[1]})")
