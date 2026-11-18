"""Drawing helpers for the news-image-20261118 v3 front page.

All art is original, drawn with Pillow primitives. No external images.
Canvas is 1024x1024, warm newsprint paper.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 14
GUT = 8

# --- palette ---
PAPER = (247, 243, 232)
INK = (26, 26, 30)
SOFT_INK = (68, 64, 58)
MUTED = (120, 114, 102)
RULE = (40, 40, 44)
CARD_BG = (255, 253, 247)
CARD_LINE = (205, 198, 184)
RED = (178, 34, 34)
BLUE = (31, 78, 140)
GOLD = (176, 124, 22)
GREEN = (42, 110, 62)
BROWN = (122, 74, 32)
TEAL = (18, 120, 122)
PURPLE = (104, 74, 150)
MAP_DOT = (122, 136, 152)
MAP_LAND = (214, 206, 188)

REGION_COLORS = {
    "Americas": GREEN, "Europe": BLUE, "Africa": BROWN,
    "Middle East": RED, "Asia": GOLD, "Oceania": TEAL, "Global": PURPLE,
}

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_IT = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS_O = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"

_fonts = {}


def font(path, size):
    key = (path, size)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(path, size)
    return _fonts[key]


def new_page():
    img = Image.new("RGB", (W, H), PAPER)
    return img, ImageDraw.Draw(img)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def wrap(draw, text, f, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, f, max_w, fill=INK, leading=None, max_lines=None):
    """Draw wrapped text; returns (total_lines_needed, bottom_y).

    total_lines_needed counts ALL wrapped lines, even when max_lines
    truncates what is drawn, so callers can detect overflow.
    """
    if leading is None:
        leading = f.size + 2
    lines = wrap(draw, text, f, max_w)
    total = len(lines)
    shown = lines if max_lines is None else lines[:max_lines]
    for i, line in enumerate(shown):
        draw.text((x, y + i * leading), line, font=f, fill=fill)
    return total, y + len(shown) * leading


def num_badge(draw, cx, cy, n, color, r=9):
    """Numbered circle badge centred at (cx, cy)."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color,
                 outline=(255, 255, 255), width=1)
    f = font(SANS_B, 11 if r >= 9 else 9)
    tw = draw.textlength(str(n), font=f)
    th = f.size
    draw.text((cx - tw / 2, cy - th / 2 - 1), str(n), font=f,
              fill=(255, 255, 255))


def tag_line(draw, x, y, n, region, topic, color):
    """Number badge + REGION . TOPIC small caps tag. Returns bottom y."""
    num_badge(draw, x + 9, y + 8, n, color, r=9)
    f = font(SANS_B, 10)
    draw.text((x + 22, y + 3), region.upper() + "  \u00b7  " + topic.upper(),
              font=f, fill=color)
    return y + 18


def card_frame(draw, x, y, w, h, accent):
    """Card outline with a coloured top accent bar."""
    draw.rectangle([x, y, x + w, y + h], fill=CARD_BG, outline=CARD_LINE, width=1)
    draw.rectangle([x, y, x + w, y + 4], fill=accent)


def lead_frame(draw, x, y, w, h, accent):
    draw.rectangle([x, y, x + w, y + h], fill=CARD_BG, outline=CARD_LINE, width=1)
    draw.rectangle([x, y, x + w, y + 4], fill=accent)


# --- illustrated scenes (original drawings, one per story) ---

def scene_gulf(d, x, y, w, h):
    """Strait of Hormuz: sea, two shores, dotted missile arcs, jets."""
    d.rectangle([x, y, x + w, y + h], fill=(186, 214, 228))
    d.polygon([(x, y), (x + w * 0.42, y), (x + w * 0.30, y + h * 0.42),
               (x, y + h * 0.55)], fill=(232, 214, 170))
    d.polygon([(x + w, y), (x + w * 0.66, y), (x + w * 0.74, y + h * 0.38),
               (x + w, y + h * 0.52)], fill=(222, 200, 152))
    for i in range(9):
        d.line([x + w * 0.10 + i * w * 0.085, y + h * 0.62,
                x + w * 0.10 + i * w * 0.085, y + h * 0.66], fill=(140, 175, 195), width=2)
    # dotted missile arcs
    for t in range(0, 11):
        fx = t / 10.0
        px = x + w * (0.18 + 0.55 * fx)
        py = y + h * (0.42 - 0.30 * (1 - (2 * fx - 1) ** 2))
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
    # ship + jets
    d.polygon([(x + w * 0.60, y + h * 0.72), (x + w * 0.72, y + h * 0.72),
               (x + w * 0.69, y + h * 0.80), (x + w * 0.63, y + h * 0.80)],
              fill=(52, 52, 58))
    d.rectangle([x + w * 0.64, y + h * 0.64, x + w * 0.66, y + h * 0.72],
                fill=(52, 52, 58))
    for jx, jy in ((0.30, 0.16), (0.44, 0.10)):
        d.polygon([(x + w * jx, y + h * jy), (x + w * (jx + 0.07), y + h * jy),
                   (x + w * (jx + 0.035), y + h * (jy + 0.05))], fill=(40, 40, 46))
    f = font(SANS_B, 10)
    d.text((x + 6, y + 4), "QESHM", font=f, fill=(90, 60, 20))
    d.text((x + 6, y + h - 16), "BAHRAIN", font=f, fill=(90, 60, 20))
    d.text((x + w - 52, y + h - 16), "HORMUZ", font=f, fill=(60, 90, 110))


def scene_kerch(d, x, y, w, h):
    """Kerch Strait bridge, middle span collapsed into the sea."""
    d.rectangle([x, y, x + w, y + h], fill=(170, 196, 216))
    d.rectangle([x, y + h * 0.55, x + w, y + h], fill=(120, 160, 190))
    for i in range(12):
        d.line([x + i * w / 11, y + h * 0.60, x + i * w / 11, y + h * 0.64],
               fill=(200, 225, 240), width=2)
    d.rectangle([x, y + h * 0.30, x + w, y + h * 0.38], fill=(70, 74, 80))
    # left + right arches standing
    d.arc([x + w * 0.02, y + h * 0.02, x + w * 0.34, y + h * 0.55],
          180, 360, fill=(50, 54, 60), width=4)
    d.arc([x + w * 0.66, y + h * 0.02, x + w * 0.98, y + h * 0.55],
          180, 360, fill=(50, 54, 60), width=4)
    # collapsed middle span: tilted deck in the water + smoke
    d.polygon([(x + w * 0.38, y + h * 0.62), (x + w * 0.60, y + h * 0.52),
               (x + w * 0.62, y + h * 0.58), (x + w * 0.40, y + h * 0.68)],
              fill=(90, 94, 100))
    for cx, cy, r in ((0.48, 0.30, 9), (0.52, 0.22, 12), (0.56, 0.30, 8)):
        d.ellipse([x + w * cx - r, y + h * cy - r, x + w * cx + r, y + h * cy + r],
                  fill=(120, 122, 126))
    d.ellipse([x + w * 0.84, y + h * 0.10, x + w * 0.84 + 18, y + h * 0.10 + 18],
              fill=(240, 200, 90))
    f = font(SANS_B, 10)
    d.text((x + 6, y + h - 16), "KERCH STRAIT  \u00b7  19 KM CROSSING",
           font=f, fill=(255, 255, 255))


def scene_manila(d, x, y, w, h):
    """Manila skyline at dusk, flags of US, China, Russia, Japan."""
    d.rectangle([x, y, x + w, y + h], fill=(44, 52, 84))
    d.ellipse([x + w * 0.80, y + h * 0.08, x + w * 0.80 + 26, y + h * 0.08 + 26],
              fill=(240, 190, 80))
    heights = [0.42, 0.60, 0.50, 0.72, 0.58, 0.66, 0.46, 0.62, 0.54, 0.70]
    bw = w / len(heights)
    for i, hh in enumerate(heights):
        bx = x + i * bw
        d.rectangle([bx + 1, y + h * (1 - hh), bx + bw - 1, y + h], fill=(22, 26, 44))
        for wy in range(3):
            d.rectangle([bx + 3, y + h * (1 - hh) + 6 + wy * 12, bx + 6,
                         y + h * (1 - hh) + 10 + wy * 12], fill=(240, 200, 90))
    # flags on poles
    flags = [((0.14, (200, 60, 60))), ((0.30, (220, 40, 40))),
             ((0.46, (40, 90, 200))), ((0.62, (230, 230, 230)))]
    for fx, col in flags:
        d.line([x + w * fx, y + h * 0.22, x + w * fx, y + h * 0.52],
               fill=(200, 200, 200), width=2)
        d.rectangle([x + w * fx, y + h * 0.22, x + w * fx + 18, y + h * 0.22 + 11],
                    fill=col)
    f = font(SANS_B, 10)
    d.text((x + 6, y + h - 16), "MANILA  \u00b7  FIRST QUAD IN TWO YEARS",
           font=f, fill=(255, 255, 255))


def scene_nvidia(d, x, y, w, h):
    """Green chip + steep rising chart, $115.8bn."""
    d.rectangle([x, y, x + w, y + h], fill=(18, 46, 30))
    d.rectangle([x + 8, y + 8, x + 52, y + 52], fill=(34, 120, 60),
                outline=(140, 230, 160), width=2)
    d.rectangle([x + 20, y + 20, x + 40, y + 40], fill=(140, 230, 160))
    for px in (14, 30, 46):
        d.line([x + px, y + 4, x + px, y + 8], fill=(140, 230, 160), width=2)
        d.line([x + px, y + 52, x + px, y + 56], fill=(140, 230, 160), width=2)
    pts = [(x + 58, y + h - 14), (x + w * 0.45, y + h * 0.62),
           (x + w * 0.65, y + h * 0.55), (x + w * 0.82, y + h * 0.30),
           (x + w - 8, y + h * 0.14)]
    d.line(pts, fill=(120, 230, 140), width=3, joint="curve")
    d.polygon([(pts[-1][0] - 7, pts[-1][1] + 2), (pts[-1][0] + 2, pts[-1][1] - 2),
               (pts[-1][0] - 2, pts[-1][1] + 8)], fill=(120, 230, 140))
    f = font(SANS_B, 15)
    d.text((x + w - 92, y + h - 22), "$115.8bn", font=f, fill=(255, 255, 255))


def scene_peltola(d, x, y, w, h):
    """Capitol dome + Alaska map + 56-44 vote bars."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 240))
    d.rectangle([x + 8, y + h * 0.42, x + 58, y + h * 0.95], fill=(250, 250, 250),
                outline=(120, 120, 120), width=1)
    d.pieslice([x + 18, y + h * 0.12, x + 48, y + h * 0.48], 180, 360,
               fill=(70, 90, 120))
    d.rectangle([x + 30, y + h * 0.05, x + 36, y + h * 0.16], fill=(70, 90, 120))
    for col in range(3):
        d.rectangle([x + 14 + col * 14, y + h * 0.55, x + 22 + col * 14,
                     y + h * 0.85], fill=(120, 140, 160))
    # Alaska shape (stylised)
    d.polygon([(x + w * 0.42, y + h * 0.30), (x + w * 0.55, y + h * 0.18),
               (x + w * 0.78, y + h * 0.22), (x + w * 0.92, y + h * 0.42),
               (x + w * 0.80, y + h * 0.55), (x + w * 0.60, y + h * 0.52),
               (x + w * 0.45, y + h * 0.45)], fill=(90, 140, 190))
    f = font(SANS_B, 11)
    d.text((x + w * 0.58, y + h * 0.28), "ALASKA", font=f, fill=(255, 255, 255))
    # vote bars
    d.rectangle([x + w * 0.42, y + h * 0.66, x + w * 0.42 + 56, y + h * 0.78],
                fill=BLUE)
    d.rectangle([x + w * 0.42, y + h * 0.82, x + w * 0.42 + 44, y + h * 0.94],
                fill=RED)
    f2 = font(SANS_B, 10)
    d.text((x + w * 0.42 + 60, y + h * 0.66), "56", font=f2, fill=BLUE)
    d.text((x + w * 0.42 + 48, y + h * 0.82), "44", font=f2, fill=RED)


def scene_knesset(d, x, y, w, h):
    """Parliament hall: podium, seats arc, ballot box, 66-52."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 224, 200))
    d.polygon([(x + w * 0.10, y + h * 0.30), (x + w * 0.90, y + h * 0.30),
               (x + w * 0.82, y + h * 0.92), (x + w * 0.18, y + h * 0.92)],
              fill=(150, 130, 95))
    for r in range(3):
        for c in range(7 - r):
            sx = x + w * (0.28 + r * 0.05 + c * 0.075)
            sy = y + h * (0.42 + r * 0.16)
            d.ellipse([sx, sy, sx + 9, sy + 9],
                      fill=BLUE if (r + c) % 3 else GOLD)
    d.rectangle([x + w * 0.44, y + h * 0.62, x + w * 0.56, y + h * 0.92],
                fill=(90, 60, 30))
    f = font(SANS_B, 15)
    d.text((x + 4, y + 2), "66\u201352", font=f, fill=INK)


def scene_cyclone(d, x, y, w, h, label="BAY OF BENGAL", wind="90\u2013100 KM/H"):
    """Cyclone spiral over a coast outline."""
    d.rectangle([x, y, x + w, y + h], fill=(206, 226, 238))
    d.polygon([(x + w * 0.62, y), (x + w, y), (x + w, y + h),
               (x + w * 0.72, y + h), (x + w * 0.66, y + h * 0.55),
               (x + w * 0.70, y + h * 0.30)], fill=(228, 214, 170))
    cx, cy = x + w * 0.34, y + h * 0.48
    for k, rr in enumerate((26, 20, 14, 8)):
        d.arc([cx - rr, cy - rr, cx + rr, cy + rr], k * 55, k * 55 + 250,
              fill=(40, 90, 140) if k % 2 == 0 else (90, 140, 190), width=4)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(40, 90, 140))
    for i in range(5):
        d.line([x + w * (0.06 + i * 0.05), y + h * 0.80,
                x + w * (0.02 + i * 0.05), y + h * 0.92],
               fill=(90, 140, 190), width=2)
    f = font(SANS_B, 10)
    d.text((x + w - 78, y + 4), wind, font=f, fill=(40, 90, 140))


def scene_wallstreet(d, x, y, w, h):
    """Falling red chart over a street of towers, -849."""
    d.rectangle([x, y, x + w, y + h], fill=(238, 226, 214))
    for i, hh in enumerate((0.55, 0.75, 0.60, 0.85, 0.65)):
        bx = x + 6 + i * 16
        d.rectangle([bx, y + h * (1 - hh), bx + 12, y + h], fill=(120, 110, 100))
    pts = [(x + 6, y + 10), (x + w * 0.35, y + h * 0.30),
           (x + w * 0.55, y + h * 0.26), (x + w * 0.75, y + h * 0.52),
           (x + w - 6, y + h * 0.78)]
    d.line(pts, fill=RED, width=3, joint="curve")
    d.polygon([(pts[-1][0] - 2, pts[-1][1] - 8), (pts[-1][0] + 6, pts[-1][1] - 2),
               (pts[-1][0] - 7, pts[-1][1] + 2)], fill=RED)
    f = font(SANS_B, 15)
    d.text((x + w - 62, y + 4), "\u2212849", font=f, fill=RED)


def scene_eu_loan(d, x, y, w, h):
    """Big euro sign, EU star circle, Ukraine blue-yellow band."""
    d.rectangle([x, y, x + w, y + h], fill=(30, 60, 130))
    for k in range(12):
        import math
        a = k * 30 * math.pi / 180
        sx = x + w * 0.68 + 26 * math.cos(a)
        sy = y + h * 0.38 + 22 * math.sin(a)
        d.polygon([(sx, sy - 4), (sx + 1.2, sy - 1.2), (sx + 4, sy),
                   (sx + 1.2, sy + 1.2), (sx, sy + 4), (sx - 1.2, sy + 1.2),
                   (sx - 4, sy), (sx - 1.2, sy - 1.2)], fill=(240, 210, 60))
    f = font(SERIF, 34)
    d.text((x + 10, y + 2), "\u20ac", font=f, fill=(255, 255, 255))
    f2 = font(SANS_B, 13)
    d.text((x + 52, y + 12), "45bn", font=f2, fill=(255, 255, 255))
    d.rectangle([x, y + h - 16, x + w, y + h - 8], fill=(40, 110, 200))
    d.rectangle([x, y + h - 8, x + w, y + h], fill=(240, 210, 60))


def scene_gaza(d, x, y, w, h):
    """Row of tents in rain under a grey sky, broken wall."""
    d.rectangle([x, y, x + w, y + h], fill=(168, 168, 158))
    for i in range(6):
        d.line([x + w * (0.08 + i * 0.12), y + h * 0.18,
                x + w * (0.04 + i * 0.12), y + h * 0.30],
               fill=(140, 140, 130), width=2)
    d.rectangle([x, y + h * 0.72, x + w, y + h], fill=(140, 120, 95))
    for i, tx in enumerate((0.06, 0.30, 0.54, 0.76)):
        d.polygon([(x + w * tx, y + h * 0.72), (x + w * (tx + 0.09), y + h * 0.48),
                   (x + w * (tx + 0.18), y + h * 0.72)],
                  fill=(235, 228, 210) if i % 2 == 0 else (210, 200, 180),
                  outline=(120, 110, 95))
    d.rectangle([x + w * 0.86, y + h * 0.30, x + w * 0.98, y + h * 0.72],
                fill=(110, 105, 95))
    d.line([x + w * 0.86, y + h * 0.42, x + w * 0.98, y + h * 0.36],
           fill=(80, 76, 70), width=2)
    f = font(SANS_B, 10)
    d.text((x + 6, y + 4), "ANOTHER WINTER IN TENTS", font=f, fill=(255, 255, 255))


def scene_ebola(d, x, y, w, h):
    """Virus particles with spikes + red case counter."""
    d.rectangle([x, y, x + w, y + h], fill=(240, 228, 210))
    for cx, cy, r, col in ((0.24, 0.42, 16, (150, 60, 40)),
                           (0.52, 0.30, 11, (180, 90, 50)),
                           (0.74, 0.55, 13, (150, 60, 40)),
                           (0.60, 0.72, 8, (180, 90, 50))):
        px, py = x + w * cx, y + h * cy
        for k in range(8):
            import math
            a = k * 45 * math.pi / 180
            d.line([px + r * 0.8 * math.cos(a), py + r * 0.8 * math.sin(a),
                    px + (r + 5) * math.cos(a), py + (r + 5) * math.sin(a)],
                   fill=col, width=2)
        d.ellipse([px - r, py - r, px + r, py + r], fill=col)
        d.ellipse([px - r * 0.4, py - r * 0.4, px + r * 0.1, py + r * 0.1],
                  fill=(240, 200, 170))
    f = font(SANS_B, 14)
    d.text((x + 6, y + h - 22), "11,000 cases", font=f, fill=(150, 40, 30))
    f2 = font(SANS_B, 9)
    d.text((x + w - 62, y + 4), "DR CONGO", font=f2, fill=SOFT_INK)


def scene_xavier(d, x, y, w, h):
    """Category 5 cyclone spiral over Pacific islands."""
    d.rectangle([x, y, x + w, y + h], fill=(150, 190, 215))
    for ix, iy, ir in ((0.16, 0.78, 7), (0.30, 0.84, 5), (0.85, 0.22, 6),
                       (0.78, 0.80, 5)):
        d.ellipse([x + w * ix - ir, y + h * iy - ir, x + w * ix + ir,
                   y + h * iy + ir], fill=(40, 110, 70))
    cx, cy = x + w * 0.50, y + h * 0.46
    for k, rr in enumerate((30, 23, 16, 9)):
        d.arc([cx - rr, cy - rr, cx + rr, cy + rr], k * 70, k * 70 + 260,
              fill=(250, 250, 250) if k % 2 == 0 else (220, 235, 245), width=5)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(250, 250, 250))
    f = font(SANS_B, 12)
    label = "CAT 5  \u00b7  220 KM/H"
    tw = d.textlength(label, font=f)
    d.rectangle([x + 4, y + 2, x + 10 + tw, y + 20], fill=(20, 50, 80))
    d.text((x + 7, y + 4), label, font=f, fill=(255, 255, 255))


def scene_uk_inflation(d, x, y, w, h):
    """Petrol pump, rising price arrow, 3.6%."""
    d.rectangle([x, y, x + w, y + h], fill=(30, 60, 90))
    d.rectangle([x + 10, y + 12, x + 46, y + h - 8], fill=(220, 60, 50),
                outline=(255, 255, 255), width=1)
    d.rectangle([x + 18, y + 22, x + 38, y + 36], fill=(255, 255, 255))
    f = font(SANS_B, 9)
    d.text((x + 20, y + 24), "3.6%", font=f, fill=RED)
    d.rectangle([x + 40, y + 16, x + 44, y + 34], fill=(220, 220, 220))
    d.polygon([(x + 44, y + 16), (x + 54, y + 26), (x + 44, y + 30)],
              fill=(220, 220, 220))
    pts = [(x + 56, y + h - 12), (x + w * 0.55, y + h * 0.55),
           (x + w * 0.75, y + h * 0.45), (x + w - 8, y + h * 0.18)]
    d.line(pts, fill=(240, 210, 60), width=3, joint="curve")
    d.polygon([(pts[-1][0] - 7, pts[-1][1] + 2), (pts[-1][0] + 2, pts[-1][1] - 2),
               (pts[-1][0] - 2, pts[-1][1] + 8)], fill=(240, 210, 60))
    f2 = font(SANS_B, 10)
    d.text((x + w - 96, y + h - 18), "FUEL +33.2%", font=f2, fill=(255, 255, 255))


SCENES = {
    "gulf": scene_gulf, "kerch": scene_kerch, "manila": scene_manila,
    "nvidia": scene_nvidia, "peltola": scene_peltola,
    "knesset": scene_knesset, "akvan": scene_cyclone,
    "wallstreet": scene_wallstreet, "eu_loan": scene_eu_loan,
    "gaza": scene_gaza, "ebola": scene_ebola, "xavier": scene_xavier,
    "uk_inflation": scene_uk_inflation,
}


# --- dotted world map ---

# Rough continent outlines in (lon, lat). Stylised newspaper map.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 73),
     (-75, 72), (-60, 60), (-55, 47), (-65, 44), (-75, 35), (-80, 26),
     (-85, 30), (-90, 21), (-95, 19), (-105, 20), (-115, 28), (-125, 40),
     (-125, 49), (-140, 60), (-155, 58), (-165, 60)],
    [(-58, 64), (-45, 60), (-40, 70), (-55, 76), (-68, 76), (-60, 74)],
    [(-80, 10), (-72, 12), (-60, 8), (-50, 0), (-35, -8), (-40, -20),
     (-48, -28), (-58, -38), (-65, -45), (-70, -55), (-73, -37),
     (-70, -20), (-77, -12), (-80, -3)],
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31), (35, 28),
     (43, 12), (51, 11), (48, 0), (40, -10), (35, -20), (32, -29),
     (20, -35), (15, -27), (12, -18), (13, -10), (9, 4), (-8, 4),
     (-13, 8), (-17, 12)],
    [(-10, 36), (0, 38), (10, 38), (15, 40), (20, 40), (28, 36), (30, 36),
     (36, 36), (40, 38), (44, 39), (48, 42), (50, 46), (55, 50), (60, 55),
     (65, 60), (70, 68), (80, 72), (100, 76), (120, 73), (140, 72),
     (160, 70), (178, 66), (170, 60), (162, 56), (158, 52), (142, 50),
     (140, 40), (135, 35), (130, 33), (127, 35), (122, 38), (120, 30),
     (115, 22), (108, 18), (105, 10), (100, 8), (97, 15), (92, 20),
     (88, 22), (80, 15), (77, 8), (75, 20), (72, 20), (66, 25), (60, 25),
     (56, 27), (52, 28), (48, 30), (44, 29), (40, 36), (36, 36),
     (30, 36), (26, 38), (22, 37), (18, 40), (12, 44), (8, 44), (3, 43),
     (-2, 44), (-2, 48), (-5, 48), (-10, 44)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (129, -32), (132, -32),
     (135, -35), (140, -38), (145, -38), (150, -37), (153, -32), (153, -27),
     (150, -22), (146, -19), (142, -15), (142, -11), (137, -12), (135, -15),
     (132, -12), (130, -13), (126, -14), (122, -17), (118, -20)],
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51)],
    [(130, 31), (133, 34), (137, 35), (140, 38), (141, 41), (143, 44),
     (142, 44), (140, 40), (137, 36), (133, 33)],
    [(95, 5), (100, 0), (105, -5), (110, -7), (115, -8), (120, -10),
     (125, -8), (130, -5), (135, -4), (140, -5), (145, -8), (147, -9),
     (141, -8), (136, -6), (130, -3), (125, -2), (120, 0), (115, 3),
     (110, 5), (105, 6), (100, 6)],
    [(167, -45), (170, -42), (174, -39), (177, -38), (175, -40),
     (172, -43), (168, -46)],
]


def _inside(lon, lat, poly):
    inside = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if ((yi > lat) != (yj > lat)) and \
                (lon < (xj - xi) * (lat - yi) / (yj - yi) + xi):
            inside = not inside
        j = i
    return inside


def on_land(lon, lat):
    return any(_inside(lon, lat, p) for p in CONTINENTS)


def lonlat_to_xy(lon, lat, mx, my, mw, mh):
    px = mx + (lon + 168) / 360.0 * mw
    py = my + (80 - lat) / 135.0 * mh
    return px, py


def draw_world_map(d, mx, my, mw, mh, pins, dots, nudges=None):
    """Dotted land map, numbered pins for illustrated stories, dots for briefs.

    nudges: {story_n: (dx, dy)} pixel offsets for crowded pins, with a
    thin leader line back to the true spot.
    """
    nudges = nudges or {}
    d.rectangle([mx, my, mx + mw, my + mh], fill=(233, 238, 242))
    step = 3.4
    yy = my + 2
    while yy < my + mh - 1:
        xx = mx + 2
        while xx < mx + mw - 1:
            lon = (xx - mx) / mw * 360.0 - 168
            lat = 80 - (yy - my) / mh * 135.0
            if on_land(lon, lat):
                d.ellipse([xx - 1.1, yy - 1.1, xx + 1.1, yy + 1.1],
                          fill=MAP_DOT)
            xx += step
        yy += step
    for lon, lat in dots:
        px, py = lonlat_to_xy(lon, lat, mx, my, mw, mh)
        d.ellipse([px - 2.4, py - 2.4, px + 2.4, py + 2.4],
                  fill=(70, 90, 110), outline=(255, 255, 255), width=1)
    for n, lon, lat, color in pins:
        px, py = lonlat_to_xy(lon, lat, mx, my, mw, mh)
        dx, dy = nudges.get(n, (0, 0))
        if (dx, dy) != (0, 0):
            d.line([px, py, px + dx, py + dy], fill=color, width=1)
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=color)
        num_badge(d, px + dx, py + dy, n, color, r=9)


def draw_legend(d, x, y):
    """Region colour key. Returns width used."""
    f = font(SANS_B, 9)
    cx = x
    for name in ("Americas", "Europe", "Africa", "Middle East", "Asia",
                 "Oceania", "Global"):
        col = REGION_COLORS[name]
        d.ellipse([cx, y + 1, cx + 8, y + 9], fill=col)
        d.text((cx + 11, y), name, font=f, fill=SOFT_INK)
        cx += 11 + d.textlength(name, font=f) + 12
    return cx - x
