"""Render the news-image-20261118 v3 front page, deterministically.

48 verified stories from Wednesday 18 November 2026: 3 illustrated
leads, 10 illustrated cards, 35 briefs, full-width dotted world map.
Run: python3 main.py  ->  entry.png (1024x1024)
"""
import hashlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PIL import Image  # noqa: E402

import render as R  # noqa: E402
from render import (BLUE, BROWN, CARD_LINE, GOLD, GREEN, INK, MARGIN,  # noqa: E402
                    MUTED, PAPER, RED, REGION_COLORS, RULE, SANS, SANS_B,
                    SERIF, SERIF_IT, SOFT_INK, TEAL, draw_wrapped, font,
                    lead_frame, card_frame, num_badge, tag_line, text_w)

LEADS = [
    dict(n=1, region="Middle East", topic="War", scene="gulf",
         color=RED, lon=57, lat=26.5,
         headline="US and Iran trade fire over the Gulf",
         deck="US jets hit an Iranian missile site on Qeshm; drones hit "
              "US radar in Bahrain, Patriots in Kuwait."),
    dict(n=2, region="Europe", topic="Ukraine War", scene="kerch",
         color=BLUE, lon=36.5, lat=45.2,
         headline="Crimea bridge span falls into the sea",
         deck="Kyiv says a second strike destroyed the road arch; Moscow "
              "says it downed 1,441 drones."),
    dict(n=3, region="Asia", topic="Diplomacy", scene="manila",
         color=GOLD, lon=121, lat=14.6,
         headline="Trump meets Marcos, then flies to Shenzhen",
         deck="Talks and lunch in Manila after the first Quad in two "
              "years; APEC opens in Shenzhen."),
]

CARDS = [
    dict(n=4, region="United States", topic="Business", scene="nvidia",
         color=GREEN, lon=-122, lat=37.4,
         headline="Nvidia's revenue doubles to $115.8bn",
         deck="Sales rose 103% on data-centre demand; Huang stays out."),
    dict(n=5, region="United States", topic="Politics", scene="peltola",
         color=GREEN, lon=-152, lat=64,
         headline="Peltola wins Alaska; Senate now 56\u201344",
         deck="AP calls it: 144,302 to 131,844. First Alaska Native "
              "senator."),
    dict(n=6, region="Israel", topic="Politics", scene="knesset",
         color=RED, lon=35.2, lat=31.8,
         headline="Knesset elects Kahana as speaker, 66\u201352",
         deck="Kahana, an Eisenkot ally, replaces Amir Ohana after a "
              "long debate."),
    dict(n=7, region="South Asia", topic="Weather", scene="akvan",
         color=GOLD, lon=88, lat=16,
         headline="Cyclone Akvan heads for Andhra Pradesh",
         deck="Landfall Friday, gusts to 110 km/h. Odisha moves people "
              "inland."),
    dict(n=8, region="United States", topic="Markets", scene="wallstreet",
         color=GREEN, lon=-74, lat=40.7,
         headline="Wall Street slides as the Dow drops 849",
         deck="S&P at its lowest since July; NSA outage blamed on "
              "maintenance."),
    dict(n=9, region="Europe", topic="Ukraine", scene="eu_loan",
         color=BLUE, lon=4.4, lat=50.8,
         headline="EU proposes a \u20ac45bn loan for Ukraine",
         deck="Covers two-thirds of Kyiv's 2027 gap; repaid only if "
              "Russia pays up."),
    dict(n=10, region="Middle East", topic="Gaza", scene="gaza",
         color=RED, lon=34.5, lat=31.5,
         headline="Board warns Gaza truce may collapse",
         deck="UN: \u2018another winter in tents and rubble\u2019 as rains "
              "flood camps."),
    dict(n=11, region="Africa", topic="Health", scene="ebola",
         color=BROWN, lon=23, lat=-2.5,
         headline="Ebola in Congo passes 11,000 cases",
         deck="Cases doubled in three months, the WHO says; 5,400 have "
              "died."),
    dict(n=12, region="Oceania", topic="Weather", scene="xavier",
         color=TEAL, lon=-160, lat=-21,
         headline="Cyclone Xavier reaches Category 5",
         deck="220 km/h winds by the Northern Cook Islands; Pukapuka "
              "warned."),
    dict(n=13, region="Europe", topic="Economy", scene="uk_inflation",
         color=BLUE, lon=-0.1, lat=51.5,
         headline="UK inflation rises to 3.6%, a one-year high",
         deck="CPI up from 3.5% as fuel jumps 33.2%; Bank sees near 5% "
              "in 2027."),
]

BRIEFS = [
    (14, "Measles", "US loses status held since 2000 (5,400+ cases, 10 deaths)", -98, 39),
    (15, "An-12 crash", "Russian military plane down in Siberia; all 19 aboard killed", 87, 55),
    (16, "Dhoni retires", "Ends IPL career; named Chennai mentor for 2027", 80, 13),
    (17, "Amazon", "$7bn for Indian renewables by 2030", 72, 20),
    (18, "Canada\u2013China", "Extend trade deals as Xi meets Carney ahead of APEC", -75, 45),
    (19, "Anthropic", "Prices IPO today; ANT trades Thursday, $70\u201378 a share", -122, 37),
    (20, "Voyager 1", "First craft one light-day from Earth, 25.9bn km out", -95, 29),
    (21, "GTA VI", "Midnight launch begins in New Zealand, 13 years after GTA V", 172, -41),
    (22, "Sudan", "UN counts 2,230 civilian deaths in 10 months, most by drones", 30, 13),
    (23, "Tokyo", "Japan scrambles jets as suspected Russian planes near airspace", 139, 35.7),
    (24, "Papua New Guinea", "6.0 quake strikes", 147, -6),
    (25, "Romania", "5.3 quake in Vrancea", 25, 45.7),
    (26, "Waymo", "Halts driverless rides on US freeways after California ban", -118, 34),
    (27, "UK sanctions", "Britain sanctions 8 firms building West Bank settlements", -2, 53),
    (28, "Australia sanctions", "Lists 7, incl. settler leader Daniella Weiss", 133, -25),
    (29, "COP31", "Talks in Antalya stall on finance and fossil fuels", 30.7, 36.9),
    (30, "Senegal", "First team to qualify for AFCON 2027", -17, 14.7),
    (31, "India beat Pakistan", "2\u20131, SAFF final, 10th title", 77, 28),
    (32, "Nations League", "N. Ireland, Austria, Sweden promoted", 10, 50),
    (33, "Estonia", "To shut Russia border crossings on 1 Dec over sabotage plot", 25, 59),
    (34, "Thailand", "Trump signs reciprocal trade deal", 100, 13.7),
    (35, "Guinea", "224 jailed over illegal gold mining", -13, 10),
    (36, "Costa Rica", "Journalist shot dead over drug probe", -84, 10),
    (37, "Bulgaria", "Gas tanker sinks; 19 crew rescued", 25, 42.7),
    (38, "Fishermen sue US", "16 sue over Pacific drone strike", -120, 15),
    (39, "Telegram", "Jordan and Iraq block the app", 40, 32),
    (40, "Optimizely", "Cyberattack hits code used by 178 organisations", -87, 41),
    (41, "Peru", "M5.9 quake off south coast, no damage reported", -77, -12),
    (42, "Indonesia", "Prabowo apologises over haze; 16 died", 106, -6),
    (43, "South Africa", "Inflation jumps to 5.2%, highest since 2024", 28, -26),
    (44, "Tencent", "Q3 revenue up 8% to \u00a5207.3bn, below forecasts", 114, 22.5),
    (45, "Riyadh", "Coalition says it downed a Houthi cruise missile", 46.7, 24.6),
    (46, "Berlin", "OPCW confirms chemical-agent use; Germany points at Russia", 13.4, 52.5),
    (47, "Cambridge", "\u201cHuman\u201d named Word of the Year for 2026", 3, 53),
    (48, "Brent", "Falls 1.2% to $91.99 as US crude stocks rise 5.28m barrels", 5, 55),
]

REGION_OF = {
    1: "Middle East", 2: "Europe", 3: "Asia", 4: "Americas",
    5: "Americas", 6: "Middle East", 7: "Asia", 8: "Americas",
    9: "Europe", 10: "Middle East", 11: "Africa", 12: "Oceania",
    13: "Europe",
}

WARNINGS = []


def check(cond, msg):
    if not cond:
        WARNINGS.append(msg)


def draw_masthead(d):
    f_kick = font(SANS_B, 13)
    left = "THE DAY IN WORLD NEWS"
    right = "48 STORIES  \u00b7  6 CONTINENTS  \u00b7  ONE DAY"
    d.text((MARGIN, 12), left, font=f_kick, fill=SOFT_INK)
    d.text((1024 - MARGIN - d.textlength(right, font=f_kick), 12),
           right, font=f_kick, fill=RED)
    f_title = font(SERIF, 52)
    d.text((MARGIN - 2, 30), "Wednesday 18 November 2026",
           font=f_title, fill=INK)
    f_sub = font(SERIF_IT, 15)
    d.text((MARGIN, 90),
           "Every story on this page happened, or was first reported, on this day.",
           font=f_sub, fill=SOFT_INK)
    # coloured rule
    y = 110
    segs = [RED, BLUE, GOLD, GREEN, BROWN, TEAL]
    seg_w = (1024 - 2 * MARGIN) // len(segs)
    for i, col in enumerate(segs):
        d.rectangle([MARGIN + i * seg_w, y,
                     MARGIN + (i + 1) * seg_w - 2, y + 3], fill=col)
    d.line([MARGIN, y + 5, 1024 - MARGIN, y + 5], fill=RULE, width=1)


def draw_lead(d, s, x, y, w, h):
    lead_frame(d, x, y, w, h, s["color"])
    R.SCENES[s["scene"]](d, x + 1, y + 5, w - 2, 88)
    tag_line(d, x + 6, y + 97, s["n"], s["region"], s["topic"], s["color"])
    f_h = font(SERIF, 20)
    n, bottom = draw_wrapped(d, x + 8, y + 117, s["headline"], f_h, w - 16,
                             leading=23, max_lines=2)
    check(n <= 2, "lead %d headline wraps to %d lines" % (s["n"], n))
    f_d = font(SANS, 11)
    n2, _ = draw_wrapped(d, x + 8, y + 117 + 2 * 23 + 2, s["deck"], f_d,
                         w - 16, fill=SOFT_INK, leading=13, max_lines=2)
    check(n2 <= 2, "lead %d deck wraps to %d lines" % (s["n"], n2))


def draw_card(d, s, x, y, w, h):
    card_frame(d, x, y, w, h, s["color"])
    R.SCENES[s["scene"]](d, x + 1, y + 5, w - 2, 52)
    tag_line(d, x + 5, y + 60, s["n"], s["region"], s["topic"], s["color"])
    f_h = font(SERIF, 14)
    n, _ = draw_wrapped(d, x + 6, y + 78, s["headline"], f_h, w - 12,
                        leading=16, max_lines=2)
    check(n <= 2, "card %d headline wraps to %d lines" % (s["n"], n))
    f_d = font(SANS, 10)
    n2, _ = draw_wrapped(d, x + 6, y + 78 + 2 * 16 + 2, s["deck"], f_d,
                         w - 12, fill=SOFT_INK, leading=12, max_lines=2)
    check(n2 <= 2, "card %d deck wraps to %d lines" % (s["n"], n2))


# Pixel nudges for map pins that would otherwise overlap each other
# (Kerch/Knesset/Gaza cluster; London/Brussels cluster), with leader lines.
PIN_NUDGES = {2: (16, -12), 6: (0, 0), 10: (-18, 12), 9: (18, 10),
              13: (-16, -8)}


def draw_map_section(d, y):
    """Full-width dotted world map with legend, pins 1-13, dots 14-48."""
    f_h = font(SANS_B, 12)
    d.text((MARGIN, y), "WHERE IT HAPPENED", font=f_h, fill=INK)
    d.line([MARGIN, y + 15, 1024 - MARGIN, y + 15], fill=CARD_LINE, width=1)
    legend_w = R.draw_legend(d, MARGIN, y + 118)
    f_c = font(SANS, 9)
    d.text((MARGIN, y + 118), "", font=f_c, fill=MUTED)
    pins = []
    for s in LEADS + CARDS:
        pins.append((s["n"], s["lon"], s["lat"], s["color"]))
    dots = [(b[3], b[4]) for b in BRIEFS]
    R.draw_world_map(d, MARGIN, y + 18, 1024 - 2 * MARGIN, 96, pins, dots,
                     nudges=PIN_NUDGES)
    f_note = font(SANS, 9)
    d.text((MARGIN + legend_w + 16, y + 118),
           "Numbered pins: stories 1\u201313 above.  Dots: briefs 14\u201348.",
           font=f_note, fill=MUTED)
    return y + 132


def draw_brief(d, b, x, y, max_w):
    """One brief line: bold red number + bold place, regular text."""
    n, place, text, _, _ = b
    f_b = font(SANS_B, 10)
    f_r = font(SANS, 10)
    head = "%d. %s \u2014 " % (n, place)
    d.text((x, y), head, font=f_b, fill=INK)
    hw = d.textlength(head, font=f_b)
    d.text((x + hw, y), text, font=f_r, fill=SOFT_INK)
    total = hw + d.textlength(text, font=f_r)
    check(total <= max_w, "brief %d too wide: %.0f > %d" % (n, total, max_w))


def draw_briefs(d, y):
    f_h = font(SANS_B, 12)
    d.text((MARGIN, y),
           "ALSO ON WEDNESDAY 18 NOVEMBER \u2014 35 MORE STORIES",
           font=f_h, fill=INK)
    d.line([MARGIN, y + 15, 1024 - MARGIN, y + 15], fill=CARD_LINE, width=1)
    col_w = (1024 - 2 * MARGIN - 16) // 2
    rows = 18
    pitch = 13
    y0 = y + 20
    for i, b in enumerate(BRIEFS):
        col = 0 if i < rows else 1
        row = i if col == 0 else i - rows
        draw_brief(d, b, MARGIN + col * (col_w + 16), y0 + row * pitch, col_w)
    return y0 + rows * pitch


def draw_footer(d, y):
    f = font(SANS, 9)
    line = ("Every story was reported on Wednesday 18 November 2026; "
            "disputed claims are attributed. Sources: Reuters, AP, AFP, "
            "BBC, Al Jazeera, UN News, IMD, ONS, NASA and others. "
            "Original drawings.")
    d.text((MARGIN, y), line, font=f, fill=MUTED)


def main():
    img, d = R.new_page()
    draw_masthead(d)
    lead_w = (1024 - 2 * MARGIN - 2 * 8) // 3
    lead_x0 = (1024 - (3 * lead_w + 2 * 8)) // 2
    for i, s in enumerate(LEADS):
        draw_lead(d, s, lead_x0 + i * (lead_w + 8), 118, lead_w, 186)
    card_w = (1024 - 2 * MARGIN - 4 * 8) // 5
    card_x0 = (1024 - (5 * card_w + 4 * 8)) // 2
    for row in range(2):
        for i in range(5):
            s = CARDS[row * 5 + i]
            draw_card(d, s, card_x0 + i * (card_w + 8),
                      310 + row * 146, card_w, 140)
    map_end = draw_map_section(d, 602)
    briefs_end = draw_briefs(d, 740)
    draw_footer(d, 1000)
    return img


if __name__ == "__main__":
    img = main()
    assert img.size == (1024, 1024), img.size
    img.save("entry.png")
    raw = open("entry.png", "rb").read()
    print("entry.png: %d bytes sha256=%s" % (
        len(raw), hashlib.sha256(raw).hexdigest()))
    print("stories: %d (3 leads + 10 cards + 35 briefs)" %
          (len(LEADS) + len(CARDS) + len(BRIEFS)))
    if WARNINGS:
        print("WARNINGS (%d):" % len(WARNINGS))
        for w in WARNINGS:
            print("  - " + w)
    else:
        print("no layout warnings")
