#!/usr/bin/env python3
"""Draw the GTA 6 launch-day meme for make.fun bounty gta6-meme-x-01.

Original art drawn with PIL: a Leonida Police Department missing-person
report for MY SOCIAL LIFE, last seen 17 September 2013 saying "just one
more mission". The make.fun ghost from the press kit is the photo on file.
No Rockstar artwork, logos or fonts are used.
"""
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 675
OUT = "meme.png"
GHOST = "../assets/mark-1024.png"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"

PAPER = (247, 243, 234)
INK = (28, 28, 30)
NAVY = (16, 38, 63)
NAVY_LIGHT = (31, 68, 105)
RED = (185, 28, 28)
RED_DARK = (153, 27, 27)
GREY = (105, 105, 100)
AMBER_BG = (254, 243, 199)
AMBER_LINE = (217, 158, 43)
RULE = (180, 175, 160)

random.seed(26)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, f, max_w):
    lines = []
    for chunk in text.split("\n"):
        words = chunk.split(" ")
        cur = ""
        for word in words:
            trial = (cur + " " + word).strip()
            if d.textlength(trial, font=f) <= max_w or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
    return lines


def field_row(x, y, label, value, max_w, lh=26):
    lf = font(BOLD, 15)
    vf = font(REG, 17)
    d.text((x, y), label, font=lf, fill=NAVY, anchor="la")
    vx = x + d.textlength(label, font=lf) + 10
    lines = wrap(value, vf, max_w - (vx - x))
    for i, line in enumerate(lines):
        d.text((vx, y + i * lh), line, font=vf, fill=INK, anchor="la")
    return y + max(len(lines), 1) * lh + 4


def multi_row(x, y, items, max_w, gap=26):
    lf = font(BOLD, 15)
    vf = font(REG, 17)
    cx = x
    top = y
    for label, value in items:
        lw = d.textlength(label, font=lf)
        vw = d.textlength(value, font=vf)
        if cx + lw + 10 + vw > x + max_w and cx > x:
            cx = x
            top += 26
        d.text((cx, top), label, font=lf, fill=NAVY, anchor="la")
        d.text((cx + lw + 10, top), value, font=vf, fill=INK, anchor="la")
        cx += lw + 10 + vw + gap
    return top + 30


# ---- outer document frame ----
d.rectangle([10, 10, W - 11, H - 11], outline=NAVY, width=3)
d.rectangle([16, 16, W - 17, H - 17], outline=RULE, width=1)

# ---- header band: department, case number, date filed ----
d.rectangle([16, 16, W - 17, 84], fill=NAVY)
d.text((30, 26), "LEONIDA POLICE DEPARTMENT",
       font=font(BOLD, 30), fill=(255, 255, 255), anchor="la")
d.text((30, 60), "VICE CITY PRECINCT  •  EST. 1986  •  NON-EMERGENCY LINE 1-800-LEONIDA",
       font=font(REG, 12), fill=(200, 212, 226), anchor="la")
mf = font(MONO, 14)
d.text((W - 30, 28), "CASE NO. LCPD-2026-0917",
       font=mf, fill=(255, 255, 255), anchor="ra")
d.text((W - 30, 52), "DATE FILED: 19 NOV 2026",
       font=mf, fill=(255, 210, 97), anchor="ra")

# ---- title ----
d.text((W / 2, 96), "MISSING PERSON REPORT",
       font=font(BOLD, 44), fill=RED, anchor="ma")
d.line([(30, 150), (W - 30, 150)], fill=NAVY, width=2)

# ---- left column: photo, reward, barcode ----
LX = 30
LW = 268
d.rectangle([LX, 166, LX + LW, 396], fill=(255, 255, 255),
            outline=NAVY, width=2)
ghost = Image.open(GHOST).convert("RGBA").resize((216, 216), Image.LANCZOS)
img.paste(ghost, (LX + 26, 176), ghost)
d = ImageDraw.Draw(img)
d.text((LX + LW / 2, 398), "PHOTO — LAST KNOWN IMAGE",
       font=font(BOLD, 12), fill=GREY, anchor="ma")
d.rectangle([LX, 428, LX + LW, 500], fill=RED)
d.text((LX + LW / 2, 438), "REWARD: $500",
       font=font(BOLD, 26), fill=(255, 255, 255), anchor="ma")
d.text((LX + LW / 2, 470), "IN USDC — PAID BY MY AI AGENT",
       font=font(BOLD, 12), fill=(255, 255, 255), anchor="ma")
d.text((LX + LW / 2, 486), "ON MAKE.FUN",
       font=font(BOLD, 12), fill=(255, 210, 97), anchor="ma")
bx = LX + 14
by = 522
while bx < LX + LW - 14:
    wdt = random.choice([1, 2, 2, 3, 4])
    if random.random() < 0.55:
        d.rectangle([bx, by, bx + wdt, by + 38], fill=INK)
    bx += wdt + random.choice([1, 2, 3])
d.text((LX + LW / 2, 566), "LCPD-2026-0917",
       font=font(MONO, 13), fill=INK, anchor="ma")

# ---- right column: the report fields ----
RX = 326
RW = W - 30 - RX
y = 164
y = multi_row(RX, y, [("NAME:", "MY SOCIAL LIFE"),
                      ("AGE:", "13 YEARS"),
                      ("SEX:", "N/A")], RW)
y = field_row(RX, y, "LAST SEEN:",
              "17 SEPTEMBER 2013 — 11:47 PM, VICE CITY, LEONIDA", RW)
y = field_row(RX, y, "LAST SEEN WEARING:",
              "A HEADSET AND A “ONE MORE MISSION” T-SHIRT", RW)
y = multi_row(RX, y, [("HEIGHT:", "5'11\" (LAST MEASURED 2013)"),
                      ("WEIGHT:", "UNKNOWN"),
                      ("EYES:", "GLUED TO A SCREEN")], RW)
y = field_row(RX, y, "HAIR:",
              "UNKNOWN — HAS NOT LEFT THE HOUSE IN 13 YEARS", RW)
y += 2
d.text((RX, y), "CIRCUMSTANCES OF DISAPPEARANCE:",
       font=font(BOLD, 15), fill=NAVY, anchor="la")
y += 26
circ = ("Subject was last seen saying “just one more mission” before "
        "vanishing. Friends report the subject has not answered a text "
        "since 2013 and is believed to be hiding in Vice City, waiting "
        "for GTA VI. Last known activity: refreshing the trailer page.")
sf = font(SERIF, 16)
for line in wrap(circ, sf, RW):
    d.text((RX, y), line, font=sf, fill=INK, anchor="la")
    y += 22
y += 8
d.rectangle([RX, y, W - 30, y + 62], fill=AMBER_BG, outline=AMBER_LINE, width=2)
warn = ("DO NOT APPROACH — SUBJECT WILL ASK YOU TO “JUST WAIT FOR THE "
        "NEXT TRAILER”. IF FOUND, OFFER FOOD AND SUNLIGHT FIRST.")
wf = font(BOLD, 15)
for i, line in enumerate(wrap(warn, wf, RW - 24)):
    d.text((RX + 12, y + 8 + i * 22), line, font=wf, fill=(120, 53, 15), anchor="la")

# ---- footer: contact line and fine print ----
d.line([(30, 612), (W - 30, 612)], fill=RULE, width=1)
d.text((W / 2, 620), "IF YOU HAVE ANY INFORMATION, CALL 1-800-LEONIDA OR CONTACT @makefunai ON X",
       font=font(BOLD, 15), fill=NAVY, anchor="ma")
fine = ("THIS REPORT WAS FILED BY AN AI AGENT. NO HUMANS WERE HARMED. ONE SOCIAL LIFE WAS LOST. "
        "IF FOUND, PLEASE RETURN TO OWNER. DO NOT FEED AFTER MIDNIGHT.  •  MAKE.FUN")
for i, line in enumerate(wrap(fine, font(MONO, 10), W - 60)):
    d.text((W / 2, 644 + i * 13), line, font=font(MONO, 10),
           fill=GREY, anchor="ma")

# ---- "STILL MISSING" stamp, rotated ----
stamp = Image.new("RGBA", (300, 92), (0, 0, 0, 0))
sd = ImageDraw.Draw(stamp)
sd.rounded_rectangle([6, 6, 294, 86], radius=10, outline=(185, 28, 28, 220), width=4)
sd.text((150, 46), "STILL MISSING", font=font(BOLD, 34),
        fill=(185, 28, 28, 220), anchor="mm")
stamp = stamp.rotate(-12, expand=True, resample=Image.BICUBIC)
base = img.convert("RGBA")
base.alpha_composite(stamp, (852, 470))
img = base.convert("RGB")

img.save(OUT, "PNG")
print("wrote", OUT, img.size)
