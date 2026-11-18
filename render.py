"""Draw the news-image-20261118 round-2 entry: one image summing up the world
news of Wednesday 18 November 2026.

Layout: a split screen. Two large illustrated scenes on the left (the Kerch
Bridge strike and the US-Iran Gulf escalation), a Manila band beneath them,
and a rail on the right carrying six more of the day's stories, each with a
small scene, a headline and a two-line summary. Everything is drawn in code
with Pillow at 3x and downscaled, so the picture is deterministic.

Run:  python3 render.py   ->  writes news.png (1024x1024)
"""
import math
import random
from PIL import Image, ImageDraw, ImageFilter, ImageFont

SS = 3
W = 1024 * SS

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

PAPER = (246, 241, 230)
INK = (18, 20, 26)
RED = (178, 32, 26)
RULE = (30, 30, 34)
BAND = (10, 14, 24, 238)
BAND_TXT = (205, 214, 226)


def font(path, px):
    return ImageFont.truetype(path, int(px * SS))


def fit(draw, text, path, max_w, start_px, min_px=10):
    px = start_px
    while px > min_px:
        f = font(path, px)
        if draw.textlength(text, font=f) <= max_w * SS:
            return f, px
        px -= 1
    return font(path, min_px), min_px


def wrap(draw, text, f, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if draw.textlength(t, font=f) <= max_w * SS or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def vgrad(size, top, bottom):
    w, h = size
    col = Image.new("RGB", (1, h))
    for y in range(h):
        t = y / max(1, h - 1)
        col.putpixel((0, y), tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3)))
    return col.resize((w, h))


# ---------------------------------------------------------------- scenes
def scene_kerch(img, box):
    """Bridge over a strait at dusk; one span dropped into the water."""
    x0, y0, x1, y1 = [int(v * SS) for v in box]
    w, h = x1 - x0, y1 - y0
    img.paste(vgrad((w, h), (38, 44, 84), (214, 116, 62)), (x0, y0))
    d = ImageDraw.Draw(img, "RGBA")
    horizon = y0 + int(h * 0.62)
    sx, sy, sr = x0 + int(w * 0.82), y0 + int(h * 0.30), int(h * 0.11)
    d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(246, 190, 92, 255))
    d.rectangle([x0, horizon, x1, y1], fill=(16, 34, 58, 255))
    for i in range(14):
        rng = random.Random(40 + i)
        yy = horizon + int((i + 0.5) * (y1 - horizon) / 14)
        xx = x0 + rng.randint(0, int(w * 0.8))
        ln = rng.randint(int(w * 0.03), int(w * 0.10))
        d.line([xx, yy, xx + ln, yy], fill=(90, 130, 170, 160), width=max(2, SS))
    deck_y = horizon - int(h * 0.06)
    for fx in (0.16, 0.84):
        tx = x0 + int(w * fx)
        d.rectangle([tx - int(w * 0.012), y0 + int(h * 0.16), tx + int(w * 0.012), deck_y],
                    fill=(10, 14, 26, 255))
        for k in range(5):
            t = k / 4
            px_ = tx + int((x0 + int(w * 0.5) - tx) * t * 0.92)
            py_ = y0 + int(h * 0.16) + int((deck_y - y0 - int(h * 0.16)) * t)
            d.line([tx, y0 + int(h * 0.16), px_, deck_y], fill=(10, 14, 26, 200), width=max(2, SS))
    gap_l, gap_r = x0 + int(w * 0.44), x0 + int(w * 0.62)
    d.rectangle([x0, deck_y, gap_l, deck_y + int(h * 0.035)], fill=(8, 11, 20, 255))
    d.rectangle([gap_r, deck_y, x1, deck_y + int(h * 0.035)], fill=(8, 11, 20, 255))
    d.polygon([(gap_l, deck_y + int(h * 0.02)), (gap_r - int(w * 0.02), deck_y + int(h * 0.16)),
               (gap_r - int(w * 0.02), deck_y + int(h * 0.20)), (gap_l, deck_y + int(h * 0.06))],
              fill=(8, 11, 20, 255))
    for dx in (-0.02, 0.0, 0.02):
        cx = gap_r - int(w * 0.03) + int(w * dx)
        d.arc([cx - int(w * 0.03), deck_y + int(h * 0.10), cx + int(w * 0.03), deck_y + int(h * 0.24)],
              180, 360, fill=(210, 225, 240, 220), width=max(2, SS))
    bx, by = gap_l + int(w * 0.02), deck_y - int(h * 0.02)
    for r, c in ((0.055, (255, 122, 26, 255)), (0.038, (255, 176, 66, 255)), (0.022, (255, 226, 150, 255))):
        rr = int(h * r)
        d.ellipse([bx - rr, by - rr, bx + rr, by + rr], fill=c)
    rng = random.Random(7)
    smoke = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(smoke)
    for i in range(8):
        cx = bx + int(w * 0.010 * i) + rng.randint(-3, 3) * SS
        cy = by - int(h * 0.06) - int(h * 0.042 * i)
        rr = int(h * (0.034 + 0.012 * i))
        sd.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=(56, 54, 62, 150))
    smoke = smoke.filter(ImageFilter.GaussianBlur(7 * SS))
    img.paste(smoke, (0, 0), smoke)
    return img


def scene_gulf(img, box):
    """Night coast: a missile site on an island, a jet streak, drones at a radar dome."""
    x0, y0, x1, y1 = [int(v * SS) for v in box]
    w, h = x1 - x0, y1 - y0
    img.paste(vgrad((w, h), (10, 16, 38), (30, 44, 78)), (x0, y0))
    d = ImageDraw.Draw(img, "RGBA")
    rng = random.Random(3)
    for _ in range(40):
        d.point((x0 + rng.randint(0, w), y0 + rng.randint(0, int(h * 0.5))), fill=(220, 230, 255, 200))
    sea_y = y0 + int(h * 0.78)
    d.rectangle([x0, sea_y, x1, y1], fill=(8, 20, 38, 255))
    isl = [(x0, sea_y), (x0 + int(w * 0.10), sea_y - int(h * 0.16)),
           (x0 + int(w * 0.30), sea_y - int(h * 0.20)), (x0 + int(w * 0.44), sea_y)]
    d.polygon(isl, fill=(14, 18, 26, 255))
    mx, my = x0 + int(w * 0.24), sea_y - int(h * 0.20)
    d.polygon([(mx, my), (mx + int(w * 0.02), my - int(h * 0.17)), (mx + int(w * 0.04), my)],
              fill=(200, 210, 220, 255))
    for r, c in ((0.065, (255, 122, 26, 230)), (0.04, (255, 190, 80, 255))):
        rr = int(h * r)
        d.ellipse([mx - rr + int(w * 0.02), my - int(h * 0.03) - rr,
                   mx + rr + int(w * 0.02), my - int(h * 0.03) + rr], fill=c)
    jx, jy = x0 + int(w * 0.52), y0 + int(h * 0.20)
    d.polygon([(jx, jy), (jx + int(w * 0.10), jy + int(h * 0.035)), (jx + int(w * 0.02), jy + int(h * 0.05))],
              fill=(190, 200, 215, 255))
    d.line([x0 + int(w * 0.30), jy + int(h * 0.075), jx, jy + int(h * 0.03)],
           fill=(255, 170, 90, 180), width=max(2, SS))
    dx, dy = x0 + int(w * 0.80), sea_y
    d.pieslice([dx - int(w * 0.07), dy - int(h * 0.17), dx + int(w * 0.07), dy + int(h * 0.17)],
               180, 360, fill=(36, 46, 66, 255))
    d.arc([dx - int(w * 0.07), dy - int(h * 0.17), dx + int(w * 0.07), dy + int(h * 0.17)],
          180, 360, fill=(150, 170, 200, 255), width=max(2, SS))
    d.rectangle([dx - int(w * 0.075), dy - int(h * 0.01), dx + int(w * 0.075), dy], fill=(36, 46, 66, 255))
    for fx, fy in ((0.66, 0.30), (0.74, 0.18), (0.60, 0.14)):
        cx, cy = x0 + int(w * fx), y0 + int(h * fy)
        s = int(w * 0.020)
        d.line([cx - s, cy, cx + s, cy], fill=(230, 90, 70, 255), width=max(2, SS))
        d.line([cx, cy - s // 2, cx, cy + s // 2], fill=(230, 90, 70, 255), width=max(2, SS))
        d.ellipse([cx - SS, cy - SS, cx + SS, cy + SS], fill=(255, 120, 90, 255))
    for r in (0.05, 0.09, 0.13):
        rr = int(h * r)
        d.arc([dx - rr, dy - int(h * 0.02) - rr, dx + rr, dy - int(h * 0.02) + rr],
              200, 320, fill=(90, 220, 140, 200), width=max(2, SS))
    return img


def scene_summit(img, box):
    """City skyline at dawn with three flags."""
    x0, y0, x1, y1 = [int(v * SS) for v in box]
    w, h = x1 - x0, y1 - y0
    img.paste(vgrad((w, h), (24, 32, 66), (196, 110, 70)), (x0, y0))
    d = ImageDraw.Draw(img, "RGBA")
    rng = random.Random(5)
    bw = w // 9
    for i in range(9):
        bh = int(h * rng.uniform(0.30, 0.62))
        bx = x0 + i * bw
        d.rectangle([bx + SS * 2, y1 - bh, bx + bw - SS * 2, y1], fill=(12, 16, 28, 255))
        for wy in range(y1 - bh + SS * 4, y1 - SS * 4, SS * 7):
            for wx in range(bx + SS * 5, bx + bw - SS * 5, SS * 6):
                if rng.random() < 0.5:
                    d.rectangle([wx, wy, wx + SS * 2, wy + SS * 3], fill=(250, 205, 110, 230))
    for i, c in enumerate([(214, 40, 44), (240, 240, 240), (60, 90, 200)]):
        px_ = x0 + int(w * (0.38 + 0.12 * i))
        d.line([px_, y1, px_, y0 + int(h * 0.30)], fill=(230, 230, 230, 255), width=max(2, SS * 2))
        d.polygon([(px_, y0 + int(h * 0.30)), (px_ + int(w * 0.085), y0 + int(h * 0.345)),
                   (px_, y0 + int(h * 0.39))], fill=c + (255,))
    return img


def scene_virus(img, box, bg=(52, 14, 18), color=(238, 84, 74)):
    x0, y0, x1, y1 = [int(v * SS) for v in box]
    w, h = x1 - x0, y1 - y0
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([x0, y0, x1, y1], fill=bg + (255,))
    rng = random.Random(11)
    for cx_f, cy_f, r_f in ((0.32, 0.52, 0.20), (0.68, 0.34, 0.13), (0.74, 0.70, 0.10)):
        cx, cy, r = x0 + int(w * cx_f), y0 + int(h * cy_f), int(min(w, h) * r_f)
        for k in range(10):
            a = k * math.tau / 10 + rng.uniform(-0.1, 0.1)
            ex, ey = cx + int(r * 1.35 * math.cos(a)), cy + int(r * 1.35 * math.sin(a))
            d.line([cx, cy, ex, ey], fill=color + (255,), width=max(2, SS * 2))
            d.ellipse([ex - SS * 2, ey - SS * 2, ex + SS * 2, ey + SS * 2], fill=color + (255,))
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color + (255,))
        d.ellipse([cx - r // 3, cy - r // 3, cx + r // 3, cy + r // 3], fill=(255, 170, 150, 255))
    return img


def scene_shield(img, box, bg=(16, 40, 34)):
    """A cracked shield and an escaping virus: protection lost."""
    x0, y0, x1, y1 = [int(v * SS) for v in box]
    w, h = x1 - x0, y1 - y0
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([x0, y0, x1, y1], fill=bg + (255,))
    cx, cy = x0 + int(w * 0.42), y0 + int(h * 0.52)
    sw, sh = int(w * 0.32), int(h * 0.64)
    pts = [(cx - sw // 2, cy - sh // 2), (cx + sw // 2, cy - sh // 2),
           (cx + sw // 2, cy - int(sh * 0.02)), (cx + int(sw * 0.30), cy + int(sh * 0.30)),
           (cx, cy + sh // 2), (cx - int(sw * 0.30), cy + int(sh * 0.30)),
           (cx - sw // 2, cy - int(sh * 0.02))]
    d.polygon(pts, outline=(120, 220, 170, 255), width=max(3, SS * 2))
    crack = [(cx - int(sw * 0.05), cy - sh // 2), (cx + int(sw * 0.08), cy - int(sh * 0.18)),
             (cx - int(sw * 0.04), cy + int(sh * 0.05)), (cx + int(sw * 0.06), cy + int(sh * 0.26))]
    d.line(crack, fill=(255, 120, 90, 255), width=max(3, SS * 2), joint="curve")
    vx, vy, vr = x0 + int(w * 0.76), y0 + int(h * 0.30), int(min(w, h) * 0.10)
    for k in range(8):
        a = k * math.tau / 8
        ex, ey = vx + int(vr * 1.4 * math.cos(a)), vy + int(vr * 1.4 * math.sin(a))
        d.line([vx, vy, ex, ey], fill=(238, 84, 74, 255), width=max(2, SS * 2))
        d.ellipse([ex - SS * 2, ey - SS * 2, ex + SS * 2, ey + SS * 2], fill=(238, 84, 74, 255))
    d.ellipse([vx - vr, vy - vr, vx + vr, vy + vr], fill=(238, 84, 74, 255))
    return img


def scene_cyclone(img, box, bg=(13, 44, 66)):
    x0, y0, x1, y1 = [int(v * SS) for v in box]
    w, h = x1 - x0, y1 - y0
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([x0, y0, x1, y1], fill=bg + (255,))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    R = min(w, h) * 0.44
    prev = None
    for i in range(91):
        t = i / 90
        ang = t * 4.6 * math.pi
        r = R * (0.10 + 0.90 * t)
        px_, py_ = cx + r * math.cos(ang), cy + r * math.sin(ang) * 0.92
        if prev is not None:
            wd = max(2, int(min(w, h) * 0.028 * (0.35 + 0.65 * t)))
            d.line([prev[0], prev[1], px_, py_], fill=(238, 246, 252, int(150 + 100 * t)), width=wd)
        prev = (px_, py_)
    er = min(w, h) * 0.055
    d.ellipse([cx - er, cy - er, cx + er, cy + er], fill=(250, 200, 90, 255))
    return img


def scene_capitol(img, box, bg=(18, 30, 58)):
    x0, y0, x1, y1 = [int(v * SS) for v in box]
    w, h = x1 - x0, y1 - y0
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([x0, y0, x1, y1], fill=bg + (255,))
    cx = (x0 + x1) // 2
    base = y0 + int(h * 0.82)
    d.pieslice([cx - int(w * 0.16), base - int(h * 0.52), cx + int(w * 0.16), base + int(h * 0.10)],
               180, 360, fill=(225, 230, 240, 255))
    d.rectangle([cx - int(w * 0.30), base - int(h * 0.26), cx + int(w * 0.30), base], fill=(225, 230, 240, 255))
    d.rectangle([cx - int(w * 0.34), base, cx + int(w * 0.34), base + int(h * 0.05)], fill=(225, 230, 240, 255))
    d.line([cx, base - int(h * 0.52), cx, base - int(h * 0.62)], fill=(225, 230, 240, 255), width=max(2, SS * 2))
    ck = [(x0 + int(w * 0.66), y0 + int(h * 0.52)), (x0 + int(w * 0.76), y0 + int(h * 0.64)),
          (x0 + int(w * 0.94), y0 + int(h * 0.26))]
    d.line(ck, fill=(90, 220, 140, 255), width=max(4, SS * 4), joint="curve")
    return img


def scene_crash(img, box):
    """Snowy ridge, a broken aircraft, a thin smoke trail."""
    x0, y0, x1, y1 = [int(v * SS) for v in box]
    w, h = x1 - x0, y1 - y0
    img.paste(vgrad((w, h), (52, 62, 84), (150, 158, 175)), (x0, y0))
    d = ImageDraw.Draw(img, "RGBA")
    ridge = [(x0, y1), (x0, y0 + int(h * 0.66)), (x0 + int(w * 0.35), y0 + int(h * 0.52)),
             (x0 + int(w * 0.62), y0 + int(h * 0.70)), (x1, y0 + int(h * 0.58)), (x1, y1)]
    d.polygon(ridge, fill=(226, 232, 240, 255))
    fx, fy = x0 + int(w * 0.40), y0 + int(h * 0.60)
    d.polygon([(fx, fy), (fx + int(w * 0.26), fy - int(h * 0.045)), (fx + int(w * 0.30), fy + int(h * 0.01)),
               (fx + int(w * 0.03), fy + int(h * 0.05))], fill=(40, 46, 58, 255))
    d.polygon([(fx + int(w * 0.30), fy - int(h * 0.02)), (fx + int(w * 0.335), fy - int(h * 0.10)),
               (fx + int(w * 0.345), fy)], fill=(40, 46, 58, 255))
    rng = random.Random(9)
    for i in range(5):
        cx = fx + int(w * 0.10) + rng.randint(-3, 3) * SS
        cy = fy - int(h * 0.07) - int(h * 0.05 * i)
        rr = int(h * (0.026 + 0.011 * i))
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=(60, 60, 66, 130))
    return img


# ---------------------------------------------------------------- layout
RAIL = [
    ("summit", "APEC OPENS IN SHENZHEN",
     "Xi urges AI partnership and free trade, meets Putin; a first Trump-Xi-Putin summit follows Thursday."),
    ("virus", "EBOLA DOUBLES IN CONGO",
     "The outbreak passes 11,000 cases and 5,400 deaths, more than doubling in three months."),
    ("shield", "US LOSES MEASLES-FREE STATUS",
     "A status held for 26 years ends: 5,400 cases and 10 deaths reported this year."),
    ("cyclone", "CYCLONE AKVAN BUILDS",
     "The Bay of Bengal storm turns severe by Thursday toward the Andhra coast; flights cancelled."),
    ("capitol", "DEMOCRATS FLIP ALASKA",
     "Peltola defeats Sullivan for the Senate seat; Democrats reach 56 seats."),
    ("crash", "SIBERIA PLANE CRASH KILLS 19",
     "A Russian military plane comes down in the Kemerovo region; all aboard die."),
]
SCENES = {"summit": scene_summit, "virus": scene_virus, "shield": scene_shield,
          "cyclone": scene_cyclone, "capitol": scene_capitol, "crash": scene_crash}


def build():
    img = Image.new("RGB", (W, W), PAPER)
    d = ImageDraw.Draw(img, "RGBA")

    # masthead: title left, the date on a red block right
    f_m, _ = fit(d, "THE WORLD IN ONE DAY", SERIF_B, 560, 44)
    d.text((24 * SS, 26 * SS), "THE WORLD IN ONE DAY", font=f_m, fill=INK, anchor="la")
    d.rectangle([612 * SS, 22 * SS, 1000 * SS, 78 * SS], fill=RED)
    f_dt, _ = fit(d, "WEDNESDAY, 18 NOVEMBER 2026", SANS_B, 368, 25)
    d.text((806 * SS, 50 * SS), "WEDNESDAY, 18 NOVEMBER 2026", font=f_dt, fill=(255, 255, 255), anchor="ma")
    d.line([24 * SS, 92 * SS, 1000 * SS, 92 * SS], fill=RULE, width=3 * SS)

    # left lead scene: the Kerch Bridge
    scene_kerch(img, (24, 108, 600, 428))
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([24 * SS, 336 * SS, 600 * SS, 428 * SS], fill=BAND)
    f_h, _ = fit(d, "KERCH BRIDGE FALLS", SERIF_B, 540, 40)
    d.text((40 * SS, 346 * SS), "KERCH BRIDGE FALLS", font=f_h, fill=(255, 255, 255), anchor="la")
    f_d = font(SANS, 16.5)
    dek = ("Ukraine hits the Crimea link a second day; a road span drops into the strait. "
           "Russia replies against Kyiv's Dnipro bridges.")
    for i, ln in enumerate(wrap(d, dek, f_d, 540)[:2]):
        d.text((40 * SS, (388 + i * 20) * SS), ln, font=f_d, fill=BAND_TXT, anchor="la")

    # left second scene: the Gulf escalation
    scene_gulf(img, (24, 452, 600, 736))
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([24 * SS, 644 * SS, 600 * SS, 736 * SS], fill=BAND)
    f_h2, _ = fit(d, "US STRIKES IRAN; GULF ANSWERS", SERIF_B, 540, 34)
    d.text((40 * SS, 654 * SS), "US STRIKES IRAN; GULF ANSWERS", font=f_h2, fill=(255, 255, 255), anchor="la")
    dek2 = ("Jets hit a missile site on Qeshm Island. Iran drones a US radar base in "
            "Bahrain and Patriot systems in Kuwait.")
    for i, ln in enumerate(wrap(d, dek2, f_d, 540)[:2]):
        d.text((40 * SS, (692 + i * 20) * SS), ln, font=f_d, fill=BAND_TXT, anchor="la")

    # left bottom band: Manila
    d.rectangle([24 * SS, 760 * SS, 600 * SS, 946 * SS], fill=(24, 34, 54))
    scene_summit(img, (36, 772, 220, 934))
    d = ImageDraw.Draw(img, "RGBA")
    f_h3, _ = fit(d, "TRUMP IN MANILA", SANS_B, 330, 27)
    d.text((236 * SS, 786 * SS), "TRUMP IN MANILA", font=f_h3, fill=(255, 255, 255), anchor="la")
    dek3 = ("Quad talks open in the Philippines ahead of the president's China visit "
            "and Thursday's Shenzhen summit.")
    for i, ln in enumerate(wrap(d, dek3, f_d, 330)[:5]):
        d.text((236 * SS, (822 + i * 21) * SS), ln, font=f_d, fill=BAND_TXT, anchor="la")

    # right rail
    rx = 624
    d.text((rx * SS, 112 * SS), "THE REST OF THE DAY", font=font(SANS_B, 21), fill=RED, anchor="la")
    d.line([rx * SS, 140 * SS, 1000 * SS, 140 * SS], fill=RULE, width=2 * SS)
    iy = 152
    for key, head, dek_r in RAIL:
        SCENES[key](img, (rx, iy, rx + 118, iy + 84))
        d = ImageDraw.Draw(img, "RGBA")
        f_t, _ = fit(d, head, SANS_B, 244, 19.5)
        for i, ln in enumerate(wrap(d, head, f_t, 244)[:2]):
            d.text(((rx + 130) * SS, (iy + i * 23) * SS), ln, font=f_t, fill=INK, anchor="la")
        f_b = font(SANS, 14.5)
        for i, ln in enumerate(wrap(d, dek_r, f_b, 372)[:3]):
            d.text((rx * SS, (iy + 88 + i * 18) * SS), ln, font=f_b, fill=(52, 54, 60), anchor="la")
        iy += 132
        if key != "crash":
            d.line([rx * SS, (iy - 10) * SS, 1000 * SS, (iy - 10) * SS], fill=(200, 194, 178), width=SS)

    # bottom strip
    d.line([24 * SS, 958 * SS, 1000 * SS, 958 * SS], fill=RULE, width=2 * SS)
    strip = ("ALSO TODAY — Four nations press Israel to open Gaza aid  •  "
             "World Court to rule on Myanmar genocide case  •  "
             "Dhoni retires from IPL play  •  Huang open to a Nvidia return")
    f_s, _ = fit(d, strip, SANS_B, 952, 15)
    d.text((512 * SS, 970 * SS), strip, font=f_s, fill=INK, anchor="ma")

    return img.resize((1024, 1024), Image.LANCZOS)


if __name__ == "__main__":
    build().save("news.png")
    print("wrote news.png")
