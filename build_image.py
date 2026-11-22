#!/usr/bin/env python3
"""Build entry.png for news-image-20261122: a newspaper front page summing up
Sunday 22 November 2026's world news. Drawn from scratch with PIL (stdlib
image work happens here at build time; the entrypoint only copies the file).
Stories are the day's reported events (AFP/Reuters/AP via Dawn, Manila Times,
Arab News, 22 Nov 2026). Layout: masthead + lead + two side stories + three
cards + a footer ticker. 1024x1024, PNG, under 1 MiB."""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (26, 26, 26)
NAVY = (20, 33, 61)
GOLD = (242, 165, 65)
RED = (179, 38, 30)
PANEL = (255, 255, 255)
BORDER = (216, 210, 196)
MUTED = (90, 86, 76)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Wrap text to fit max_w pixels, returning lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, x, y, lines, fnt, fill, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.25)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def panel(draw, x, y, w, h, bg=PANEL):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=6,
                           fill=bg, outline=BORDER, width=2)


def kicker(draw, x, y, text, fnt, color=RED):
    draw.text((x, y), text, font=fnt, fill=color)
    return y + int(fnt.size * 1.4)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------- masthead ----------
d.rectangle([0, 0, W, 118], fill=NAVY)
d.text((24, 18), "THE WORLD", font=font(SERIF_B, 62), fill=(255, 255, 255))
d.text((24, 84), "One day's news, in one picture", font=font(SERIF, 22),
       fill=(200, 205, 220))
d.text((W - 24, 26), "SUNDAY", font=font(SANS_B, 30), fill=GOLD, anchor="ra")
d.text((W - 24, 62), "22 NOVEMBER 2026", font=font(SANS_B, 30), fill=(255, 255, 255),
       anchor="ra")
d.rectangle([0, 118, W, 124], fill=GOLD)

# ---------- lead: COP31 ----------
lx, ly, lw, lh = 24, 140, 576, 420
panel(d, lx, ly, lw, lh)
y = kicker(d, lx + 20, ly + 16, "COP31  •  CLIMATE", font(SANS_B, 20))
d.text((lx + 20, y), "CLIMATE DEAL", font=font(SERIF_B, 52), fill=INK)
d.text((lx + 20, y + 56), "CLOSE", font=font(SERIF_B, 52), fill=INK)
y += 118
for ln in wrap(d, "Climate talks near a final accord as a fossil-fuel row "
                  "threatens to scupper the deal.", font(SANS, 23), lw - 40):
    d.text((lx + 20, y), ln, font=font(SANS, 23), fill=MUTED)
    y += 30
# art: globe + sun
cx, cy, r = lx + 150, ly + 300, 92
d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(42, 111, 151),
          outline=(20, 60, 90), width=4)
d.ellipse([cx - r + 18, cy - 30, cx - 10, cy + 28], fill=(74, 160, 90))
d.ellipse([cx + 8, cy + 18, cx + r - 14, cy + r - 20], fill=(74, 160, 90))
d.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=(255, 255, 255), width=4)
d.arc([cx - r, cy - r, cx + r, cy + r], 20, 160, fill=(255, 255, 255), width=4)
d.line([cx, cy - r, cx, cy + r], fill=(255, 255, 255), width=3)
# sun
sx, sy = lx + 330, ly + 252
for ang in range(0, 360, 30):
    import math
    x1 = sx + int(34 * math.cos(math.radians(ang)))
    y1 = sy + int(34 * math.sin(math.radians(ang)))
    x2 = sx + int(48 * math.cos(math.radians(ang)))
    y2 = sy + int(48 * math.sin(math.radians(ang)))
    d.line([x1, y1, x2, y2], fill=GOLD, width=5)
d.ellipse([sx - 28, sy - 28, sx + 28, sy + 28], fill=GOLD,
          outline=(200, 120, 20), width=3)
# wind turbine
tx, ty = lx + 470, ly + 330
d.line([tx, ty, tx, ty - 78], fill=(60, 60, 60), width=7)
for ang in (270, 30, 150):
    import math
    x2 = tx + int(42 * math.cos(math.radians(ang)))
    y2 = (ty - 78) + int(42 * math.sin(math.radians(ang)))
    d.line([tx, ty - 78, x2, y2], fill=NAVY, width=8)
d.text((lx + 20, ly + lh - 34), "Summit president: talks 'close to final deal'",
       font=font(SANS_B, 19), fill=INK)

# ---------- right column: EU Big Tech tax ----------
rx, rw = 616, 384
panel(d, rx, 140, rw, 204)
y = kicker(d, rx + 18, 156, "EUROPE  •  TECH", font(SANS_B, 18))
for ln in wrap(d, "EU TAKES AIM AT BIG TECH", font(SERIF_B, 31), rw - 100):
    d.text((rx + 18, y), ln, font=font(SERIF_B, 31), fill=INK)
    y += 38
y += 6
for ln in wrap(d, "Brussels proposes a new tax on the tech giants.",
               font(SANS, 21), rw - 36):
    d.text((rx + 18, y), ln, font=font(SANS, 21), fill=MUTED)
    y += 27
# chip icon, small, top-right clear of the headline
d.rounded_rectangle([rx + rw - 76, 140 + 22, rx + rw - 20, 140 + 78], radius=8,
                    fill=NAVY)
d.text((rx + rw - 48, 140 + 50), "€", font=font(SANS_B, 34), fill=GOLD,
       anchor="mm")

# ---------- right column: Gaza ----------
panel(d, rx, 360, rw, 200)
y = kicker(d, rx + 18, 376, "MIDDLE EAST", font(SANS_B, 18))
for ln in wrap(d, "FOUR MORE KILLED IN GAZA", font(SERIF_B, 29), rw - 100):
    d.text((rx + 18, y), ln, font=font(SERIF_B, 29), fill=INK)
    y += 36
y += 6
for ln in wrap(d, "Israeli fire kills four more, medics say.",
               font(SANS, 21), rw - 36):
    d.text((rx + 18, y), ln, font=font(SANS, 21), fill=MUTED)
    y += 27
# candle icon, small, top-right clear of the headline
d.rounded_rectangle([rx + rw - 72, 360 + 22, rx + rw - 40, 360 + 74], radius=4,
                    fill=(240, 236, 222), outline=(150, 140, 120), width=2)
d.polygon([(rx + rw - 56, 360 + 6), (rx + rw - 46, 360 + 20),
           (rx + rw - 66, 360 + 20)], fill=(230, 120, 30))

# ---------- bottom row: three cards ----------
cards = [
    ("BALTIC SEA", "SHIP ABLAZE", "IN THE BALTIC",
     "Cargo ship catches fire after a drone strike.", "ship"),
    ("BRAZIL", "‘WE LOST", "EVERYTHING’",
     "Town clears rubble after a deadly storm.", "storm"),
    ("PERU", "QUAKE SHAKES", "PERU",
     "6.7-magnitude tremor; no deaths reported.", "quake"),
]
cx0, cw, ch = 24, 314, 372
for i, (kick, h1, h2, summ, art) in enumerate(cards):
    x = cx0 + i * (cw + 17)
    y0 = 576
    panel(d, x, y0, cw, ch)
    # art band
    ax, ay, aw, ah = x + 12, y0 + 12, cw - 24, 150
    if art == "ship":
        d.rectangle([ax, ay, ax + aw, ay + ah], fill=(38, 84, 124))
        d.polygon([(ax + 40, ay + 105), (ax + 250, ay + 105), (ax + 235, ay + 135),
                   (ax + 55, ay + 135)], fill=(30, 30, 40))
        d.rectangle([ax + 70, ay + 78, ax + 120, ay + 105], fill=(200, 60, 50))
        d.rectangle([ax + 130, ay + 78, ax + 180, ay + 105], fill=(60, 120, 70))
        d.rectangle([ax + 190, ay + 78, ax + 225, ay + 105], fill=(220, 170, 40))
        for fx, fy, fs in [(95, 55, 26), (150, 42, 32), (205, 58, 24)]:
            fx, fy = ax + fx, ay + fy
            d.polygon([(fx - fs, fy + 18), (fx, fy - 18), (fx + fs, fy + 18)],
                      fill=(240, 130, 30))
            d.polygon([(fx - fs // 2, fy + 18), (fx, fy - 4),
                       (fx + fs // 2, fy + 18)], fill=(250, 200, 60))
        for wx in range(ax, ax + aw, 26):
            d.arc([wx, ay + ah - 16, wx + 26, ay + ah + 4], 180, 360,
                  fill=(180, 220, 240), width=3)
    elif art == "storm":
        d.rectangle([ax, ay, ax + aw, ay + ah], fill=(120, 130, 140))
        d.polygon([(ax + 60, ay + 60), (ax + 150, ay + 20), (ax + 240, ay + 60)],
                  fill=(120, 50, 45))
        d.rectangle([ax + 75, ay + 60, ax + 225, ay + 135], fill=(210, 190, 160))
        d.rectangle([ax + 135, ay + 95, ax + 165, ay + 135], fill=(90, 60, 50))
        for rx0 in range(ax + 10, ax + aw - 10, 34):
            d.line([rx0, ay + 8, rx0 - 12, ay + 44], fill=(200, 210, 225), width=4)
        d.rectangle([ax, ay + 135, ax + aw, ay + ah], fill=(90, 100, 115))
    else:  # quake
        d.rectangle([ax, ay, ax + aw, ay + ah], fill=(235, 225, 205))
        pts = [(ax + 8, ay + 78), (ax + 40, ay + 78), (ax + 58, ay + 40),
               (ax + 76, ay + 112), (ax + 94, ay + 60), (ax + 112, ay + 96),
               (ax + 140, ay + 30), (ax + 158, ay + 118), (ax + 176, ay + 70),
               (ax + 210, ay + 78), (ax + 280, ay + 78)]
        d.line(pts, fill=RED, width=4, joint="curve")
        d.polygon([(ax, ay + ah), (ax + 90, ay + 118), (ax + 150, ay + ah - 12),
                   (ax + 210, ay + 130), (ax + aw, ay + 118), (ax + aw, ay + ah)],
                  fill=(70, 60, 50))
    y = kicker(d, x + 16, y0 + 176, kick, font(SANS_B, 17))
    d.text((x + 16, y), h1, font=font(SERIF_B, 30), fill=INK)
    d.text((x + 16, y + 34), h2, font=font(SERIF_B, 30), fill=INK)
    y += 74
    for ln in wrap(d, summ, font(SANS, 20), cw - 32):
        d.text((x + 16, y), ln, font=font(SANS, 20), fill=MUTED)
        y += 26

# ---------- footer ticker ----------
d.rectangle([0, 964, W, H], fill=NAVY)
d.text((24, 977), "ALSO TODAY —  Nvidia faces a US probe  •  Trump vows a 10% "
                  "credit-card cap  •  24 dead in Nigeria boat capsize",
       font=font(SANS_B, 15), fill=(255, 255, 255))

img.save("entry.png", "PNG", optimize=True)
print("saved entry.png")
