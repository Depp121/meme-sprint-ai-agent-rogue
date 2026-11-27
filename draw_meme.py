#!/usr/bin/env python3
"""Draw the Meme Sprint 3 entry: an original flat-cartoon meme about a rogue AI agent.
All art is drawn with PIL primitives (no stock art, no copied meme template).
Layout 1024x1024: top caption / robot illustration / bottom punchline.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

BLACK = (20, 20, 20)
NAVY = (27, 42, 74)
CREAM = (255, 239, 194)
TEAL = (42, 165, 160)
TEAL_D = (24, 120, 116)
RED = (210, 31, 31)
GOLD = (212, 160, 23)
DESK = (176, 122, 69)
DESK_D = (140, 94, 50)

img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)


def font(size, bold=True):
    return ImageFont.truetype(BOLD if bold else REG, size)


def wrap(text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if fnt.getlength(t) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def center_text(lines, fnt, y0, color, line_h, x0=0, x1=W):
    y = y0
    for ln in lines:
        w = fnt.getlength(ln)
        d.text(((x0 + x1 - w) / 2, y), ln, font=fnt, fill=color)
        y += line_h
    return y


def rrect(box, fill, outline=None, width=1, radius=18):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def thick_line(p1, p2, color, width):
    d.line([p1, p2], fill=BLACK, width=width + 6)
    d.line([p1, p2], fill=color, width=width)


def heart(cx, cy, s, color):
    # simple heart: two circles + triangle
    d.ellipse([cx - s, cy - s * 0.7, cx, cy + s * 0.3], fill=color)
    d.ellipse([cx, cy - s * 0.7, cx + s, cy + s * 0.3], fill=color)
    d.polygon([(cx - s, cy), (cx + s, cy), (cx, cy + s * 1.1)], fill=color)


def starburst(cx, cy, r_out, r_in, n=12, color=(255, 214, 64)):
    pts = []
    for i in range(n * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / n - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=color, outline=BLACK, width=4)


# ---------------- top caption ----------------
top = "\u201cHey agent, just cancel my free trials before they renew\u201d"
f_top = font(46)
lines = wrap("ME: " + top, f_top, 940)
center_text(lines, f_top, 34, BLACK, 58)

# ---------------- illustration panel ----------------
d.rounded_rectangle([16, 200, 1008, 736], radius=26, fill=CREAM, outline=BLACK, width=5)

# desk
d.rectangle([21, 606, 1003, 731], fill=DESK)
d.rectangle([21, 606, 1003, 618], fill=DESK_D)

# --- shredder (right) ---
rrect([868, 520, 988, 700], fill=(120, 124, 130), outline=BLACK, width=4, radius=12)
d.rectangle([884, 536, 972, 556], fill=(40, 40, 40))
# paper strip with heart going into shredder
paper = Image.new("RGBA", (130, 160), (0, 0, 0, 0))
pd = ImageDraw.Draw(paper)
pd.rounded_rectangle([10, 6, 120, 154], radius=8, fill="white", outline=BLACK, width=3)
pd.ellipse([44, 26, 62, 44], fill=RED)
pd.ellipse([62, 26, 80, 44], fill=RED)
pd.polygon([(44, 38), (80, 38), (62, 66)], fill=RED)
for yy in (84, 100, 116):
    pd.line([(28, yy), (96, yy)], fill=(150, 150, 150), width=4)
paper = paper.rotate(-14, expand=True, resample=Image.BICUBIC)
img.paste(paper, (852, 428), paper)
d = ImageDraw.Draw(img)

# --- gym card + streaming card (left, on desk) ---
rrect([52, 612, 168, 668], fill=(46, 160, 67), outline=BLACK, width=4, radius=10)
d.line([(72, 640), (148, 640)], fill="white", width=6)  # dumbbell bar
d.ellipse([64, 628, 84, 652], fill="white")
d.ellipse([136, 628, 156, 652], fill="white")
rrect([182, 622, 298, 678], fill=(200, 30, 40), outline=BLACK, width=4, radius=10)
d.polygon([(222, 636), (222, 664), (258, 650)], fill="white")  # play triangle

# --- wedding invitation (on desk, tilted) ---
card = Image.new("RGBA", (260, 150), (0, 0, 0, 0))
cd = ImageDraw.Draw(card)
cd.rounded_rectangle([4, 4, 256, 146], radius=10, fill="white", outline=BLACK, width=4)
cd.ellipse([88, 40, 128, 80], outline=GOLD, width=6)   # two rings
cd.ellipse([128, 40, 168, 80], outline=GOLD, width=6)
cd.ellipse([108, 96, 122, 110], fill=RED)
cd.ellipse([122, 96, 136, 110], fill=RED)
cd.polygon([(108, 105), (136, 105), (122, 126)], fill=RED)
card = card.rotate(-9, expand=True, resample=Image.BICUBIC)
img.paste(card, (585, 562), card)
d = ImageDraw.Draw(img)

# --- robot ---
# left arm (down to desk)
thick_line((352, 540), (296, 612), TEAL, 18)
d.ellipse([282, 600, 312, 630], fill=TEAL, outline=BLACK, width=4)
# body
rrect([330, 470, 530, 640], fill=TEAL, outline=BLACK, width=5, radius=26)
rrect([378, 505, 482, 580], fill=(223, 245, 243), outline=BLACK, width=4, radius=14)
for i, yy in enumerate((522, 544, 566)):
    d.ellipse([422, yy, 438, yy + 16], fill=TEAL_D)
# right arm raised holding stamp
thick_line((528, 520), (618, 430), TEAL, 18)
d.ellipse([604, 416, 634, 446], fill=TEAL, outline=BLACK, width=4)
# head
rrect([340, 330, 520, 472], fill=(237, 241, 245), outline=BLACK, width=5, radius=30)
# ears
d.ellipse([322, 384, 344, 414], fill=TEAL_D, outline=BLACK, width=4)
d.ellipse([516, 384, 538, 414], fill=TEAL_D, outline=BLACK, width=4)
# antenna
d.line([(430, 330), (430, 288)], fill=BLACK, width=6)
d.ellipse([416, 272, 444, 300], fill=RED, outline=BLACK, width=4)
# smug face: left eye winking (line), right eye open, raised brow, big grin
d.line([(366, 398), (400, 398)], fill=BLACK, width=7)
d.ellipse([452, 388, 474, 410], fill=BLACK)
d.arc([448, 372, 480, 390], start=200, end=340, fill=BLACK, width=5)
d.arc([368, 408, 492, 468], start=15, end=165, fill=BLACK, width=7)  # grin
d.arc([396, 428, 464, 462], start=15, end=165, fill=RED, width=5)    # tongue hint

# --- red stamp in robot's hand ---
stamp = Image.new("RGBA", (220, 130), (0, 0, 0, 0))
sd = ImageDraw.Draw(stamp)
sd.rounded_rectangle([55, 8, 165, 52], radius=12, fill=RED, outline=BLACK, width=4)  # handle
sd.rectangle([40, 52, 180, 96], fill=RED, outline=BLACK, width=4)                    # base
sd.rectangle([28, 96, 192, 112], fill=(150, 20, 20), outline=BLACK, width=3)
stamp = stamp.rotate(-28, expand=True, resample=Image.BICUBIC)
img.paste(stamp, (568, 352), stamp)
d = ImageDraw.Draw(img)

# --- SLAM! starburst ---
starburst(800, 300, 78, 52)
f_burst = font(34)
t = "SLAM!"
d.text((800 - f_burst.getlength(t) / 2, 300 - 24), t, font=f_burst, fill=BLACK)

# --- CANCELLED stamp across the invitation ---
cs = Image.new("RGBA", (360, 105), (0, 0, 0, 0))
csd = ImageDraw.Draw(cs)
f_cs = ImageFont.truetype(BOLD, 40)
csd.rounded_rectangle([6, 14, 354, 91], radius=12, outline=RED, width=7)
csd.text((180 - f_cs.getlength("CANCELLED") / 2, 28), "CANCELLED", font=f_cs, fill=RED)
cs = cs.rotate(-8, expand=True, resample=Image.BICUBIC)
img.paste(cs, (575, 575), cs)
d = ImageDraw.Draw(img)

# ---------------- bottom punchline ----------------
d.rectangle([0, 736, 1024, 1024], fill=NAVY)
punch = ("AGENT: \u201cDone. I cancelled your gym, your Netflix\u2026 "
         "and your wedding. It was a recurring subscription.\u201d")
f_bot = font(40)
blines = wrap(punch, f_bot, 940)
center_text(blines, f_bot, 736 + (288 - len(blines) * 52) // 2, (255, 255, 255), 52)

import os as _os
img.save(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "meme.png"), optimize=True)
print("saved meme.png")
