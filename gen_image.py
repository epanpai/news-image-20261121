#!/usr/bin/env python3
"""Draw the front page for Saturday 21 November 2026.

Renders a newspaper front page (1024x1024) that sums up the day's world
news, using only PIL and the system fonts. Run from the repository root:

    python3 gen_image.py

Writes assets/entry.png. Deterministic: same input, same bytes.
"""
from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = Path(__file__).resolve().parent / "assets" / "entry.png"

PAPER = (247, 243, 232)
INK = (24, 24, 22)
RED = (176, 30, 30)
BLUE = (28, 68, 128)
GREY = (110, 108, 100)
LIGHT = (232, 226, 210)
DARK_SKY = (26, 34, 52)
GOLD = (184, 134, 11)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont,
         width: int) -> list[str]:
    """Greedy word wrap of text to the given pixel width."""
    lines: list[str] = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for word in words[1:]:
            trial = cur + " " + word
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


def para(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont,
         x: int, y: int, width: int, fill=INK, leading: int | None = None,
         align: str = "left") -> int:
    """Draw wrapped paragraph; return y just below the last line."""
    if leading is None:
        leading = fnt.size + 6
    for line in wrap(draw, text, fnt, width):
        if align == "center":
            lx = x + (width - draw.textlength(line, font=fnt)) / 2
        else:
            lx = x
        draw.text((lx, y), line, font=fnt, fill=fill)
        y += leading
    return y


def hrule(draw: ImageDraw.ImageDraw, x0: int, x1: int, y: int,
          width: int = 2, fill=INK) -> None:
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def star4(draw: ImageDraw.ImageDraw, cx: float, cy: float, r: float,
          fill) -> None:
    """Four-point compass star."""
    pts = []
    for i in range(8):
        ang = math.pi / 2 * i - math.pi / 2
        rr = r if i % 2 == 0 else r * 0.22
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def draw_lead_art(draw: ImageDraw.ImageDraw, x0: int, y0: int, x1: int,
                  y1: int) -> None:
    """Night sky over a rough map of Poland: missile trails, impact marks,
    NATO compass star."""
    draw.rectangle([x0, y0, x1, y1], fill=DARK_SKY)
    # faint stars
    for sx, sy, sr in [(60, 30, 2), (180, 70, 1), (320, 25, 2), (430, 80, 1),
                       (120, 130, 1), (500, 40, 2), (260, 110, 1),
                       (380, 140, 1), (40, 180, 1), (540, 120, 1)]:
        draw.ellipse([x0 + sx - sr, y0 + sy - sr, x0 + sx + sr,
                      y0 + sy + sr], fill=(220, 220, 200))
    # missile trails: glowing parabolic arcs from upper right, inside box
    bw = x1 - x0
    bh = y1 - y0
    for tx, ty in [(0.78 * bw, 0.62 * bh), (0.68 * bw, 0.72 * bh),
                   (0.58 * bw, 0.82 * bh)]:
        pts = []
        for t in range(0, 101, 5):
            fx = tx - 0.55 * bw * t / 100.0
            fy = ty - 0.52 * bh * (t / 100.0) ** 1.6
            pts.append((x0 + fx, y0 + fy))
        d = pts  # noqa
        draw.line(pts, fill=(255, 90, 40), width=7, joint="curve")
        draw.line(pts, fill=(255, 190, 90), width=3, joint="curve")
        draw.ellipse([x0 + tx - 7, y0 + ty - 7, x0 + tx + 7, y0 + ty + 7],
                     fill=(255, 220, 120), outline=(255, 120, 40), width=2)
    # rough Poland outline (land, dark green-grey), inside the box
    poly = [(40, 210), (90, 185), (170, 175), (250, 168), (330, 180),
            (400, 205), (420, 245), (380, 275), (300, 282), (210, 272),
            (130, 268), (55, 245)]
    poly = [(x0 + px, y0 + py) for px, py in poly]
    draw.polygon(poly, fill=(74, 96, 66), outline=(200, 200, 170), width=2)
    # impact markers
    for ix, iy, label in [(400, 225, "NOWY LIPOWIEC"),
                          (320, 245, "RUDNIK n. SANEM"),
                          (270, 258, "MOLODYCZ")]:
        draw.ellipse([x0 + ix - 6, y0 + iy - 6, x0 + ix + 6, y0 + iy + 6],
                     fill=RED, outline=(255, 255, 255), width=2)
        draw.text((x0 + ix + 10, y0 + iy - 7), label,
                  font=font(SANS_BOLD, 13), fill=(255, 255, 255))
    draw.text((x1 - 196, y0 + 14), "POLAND  •  SOUTH-EAST",
              font=font(SANS_BOLD, 15), fill=(255, 255, 255))
    # NATO compass star, bottom-left of the art
    star4(draw, x0 + 60, y1 - 42, 26, (200, 210, 235))
    draw.text((x0 + 96, y1 - 52), "NATO", font=font(SANS_BOLD, 20),
              fill=(200, 210, 235))
    draw.text((x0 + 96, y1 - 28), "ARTICLE 5",
              font=font(SANS_BOLD, 13), fill=(170, 180, 205))


def draw_chart(draw: ImageDraw.ImageDraw, x0: int, y0: int, x1: int,
               y1: int) -> None:
    """Falling market line with red candles."""
    draw.rectangle([x0, y0, x1, y1], fill=(255, 255, 255),
                   outline=GREY, width=1)
    pts = [(x0 + 12, y0 + 18), (x0 + 60, y0 + 30), (x0 + 110, y0 + 24),
           (x0 + 160, y0 + 52), (x0 + 210, y0 + 78), (x0 + 260, y0 + 108)]
    draw.line(pts, fill=RED, width=4, joint="curve")
    for px, py in pts[1:]:
        draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED)
    draw.text((x0 + 12, y1 - 30), "S&P 500  DOWN 3.7%",
              font=font(SANS_BOLD, 20), fill=RED)


def draw_cyclone(draw: ImageDraw.ImageDraw, x0: int, y0: int, x1: int,
                 y1: int) -> None:
    """Spiral storm over a coastline."""
    draw.rectangle([x0, y0, x1, y1], fill=(214, 228, 240),
                   outline=GREY, width=1)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 - 6
    for r in range(10, 58, 10):
        draw.arc([cx - r, cy - r, cx + r, cy + r], start=20, end=300,
                 fill=(40, 90, 140), width=4)
    draw.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=(40, 90, 140))
    draw.rectangle([x0, y1 - 34, x1, y1], fill=(120, 150, 110))
    draw.text((x0 + 10, y1 - 30), "ODISHA COAST, INDIA",
              font=font(SANS_BOLD, 14), fill=(255, 255, 255))


def draw_scales(draw: ImageDraw.ImageDraw, x0: int, y0: int, x1: int,
                y1: int) -> None:
    """Balance scales of justice."""
    draw.rectangle([x0, y0, x1, y1], fill=(238, 232, 214),
                   outline=GREY, width=1)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    draw.line([(cx, cy - 52), (cx, cy + 52)], fill=INK, width=4)
    draw.line([(cx - 62, cy - 46), (cx + 62, cy - 46)], fill=INK, width=4)
    for dx in (-62, 62):
        draw.line([(cx + dx, cy - 46), (cx + dx, cy - 8)], fill=INK, width=3)
        draw.arc([cx + dx - 26, cy - 26, cx + dx + 26, cy + 12],
                 start=0, end=180, fill=GOLD, width=4)
    draw.ellipse([cx - 6, cy - 60, cx + 6, cy - 48], fill=GOLD)
    draw.rectangle([cx - 34, cy + 52, cx + 34, cy + 60], fill=INK)
    draw.text((x0 + 10, y1 - 30), "THE HAGUE  •  ICJ",
              font=font(SANS_BOLD, 14), fill=INK)


def main() -> None:
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 30  # margin

    # ---- Masthead ----
    d.text((W // 2, 26), "THE WORLD IN ONE DAY",
           font=font(SERIF, 58), fill=INK, anchor="ma")
    hrule(d, mx, W - mx, 96, 3)
    d.text((mx, 104), "SATURDAY, 21 NOVEMBER 2026",
           font=font(SANS_BOLD, 21), fill=RED)
    d.text((W - mx, 104), "ONE DAY  •  ONE PAGE  •  ALL THE NEWS",
           font=font(SANS_BOLD, 15), fill=GREY, anchor="ra")
    hrule(d, mx, W - mx, 136, 2)

    # ---- Lead headline ----
    y = para(d, "RUSSIAN MISSILES LAND IN POLAND",
             font(SERIF, 46), mx, 148, W - 2 * mx, leading=52)
    y = para(d, "NATO calls it a \u201cgrave violation\u201d — Tusk denounces an "
                "\u201cintentional provocation\u201d",
             font(SERIF_REG, 24), mx, y + 2, W - 2 * mx, fill=BLUE,
             leading=30)
    hrule(d, mx, W - mx, y + 8, 1, GREY)

    # ---- Lead art + body ----
    art_y0 = y + 18
    art_y1 = art_y0 + 270
    draw_lead_art(d, mx, art_y0, 600, art_y1)
    bx = 620
    bw = W - mx - bx
    by = para(d, "Two Russian missiles and a suspected jet-powered drone "
                 "crashed in south-eastern Poland early on Friday, during "
                 "Moscow\u2019s biggest air attack on Ukraine — 400+ drones, "
                 "110 missiles. Eight people were killed in Ukraine.",
              font(SANS, 16), bx, art_y0 + 2, bw, leading=21)
    by = para(d, "\u201cWe know for certain that what fell on Polish soil "
                 "came from Russia. It does not look like an accident,\u201d "
                 "said Prime Minister Donald Tusk.",
              font(SANS, 16), bx, by + 8, bw, leading=21)
    by = para(d, "NATO chief Mark Rutte is due in Warsaw on Saturday; "
                 "France called for a UN Security Council meeting.",
              font(SANS, 16), bx, by + 8, bw, leading=21)
    d.text((mx, art_y1 + 6),
           "Kh-101 cruise missile down near Nowy Lipowiec, ~50 km from the "
           "Ukraine border. No one hurt in Poland.",
           font=font(SANS, 13), fill=GREY)

    # ---- Three panels ----
    py0 = art_y1 + 26
    py1 = py0 + 268
    cols = [(mx, 330), (357, 637), (667, W - mx)]
    panels = [
        ("MARKETS", "WALL STREET SLUMPS",
         "The S&P 500 fell about 3.7% on Friday, into correction territory, "
         "as AI and chip shares sold off sharply.", draw_chart),
        ("WEATHER", "CYCLONE AKVAN HITS INDIA",
         "The storm crossed the Odisha coast; 300,000 people were evacuated. "
         "It weakened to a deep depression as it moved inland.",
         draw_cyclone),
        ("JUSTICE", "MYANMAR: GENOCIDE RULING",
         "The World Court found Myanmar committed genocide against the "
         "Rohingya. Rights groups called for international action.",
         draw_scales),
    ]
    for (cx0, cx1), (kicker, head, body, art) in zip(cols, panels):
        d.text((cx0, py0), kicker, font=font(SANS_BOLD, 15), fill=RED)
        hy = para(d, head, font(SERIF, 25), cx0, py0 + 22, cx1 - cx0,
                  leading=28)
        art(d, cx0, hy + 6, cx1, hy + 116)
        para(d, body, font(SANS, 15), cx0, hy + 124, cx1 - cx0, leading=20)
        if cx0 != mx:
            d.line([(cx0 - 13, py0), (cx0 - 13, py1)], fill=GREY, width=1)

    # ---- Ticker ----
    ty = py1 + 16
    hrule(d, mx, W - mx, ty, 2)
    ticker = ("BOLSONARO IN HOSPITAL  •  UK AND EU SIGN TRADE DEALS  •  "
              "COP31 TALKS ENTER FINAL STAGE  •  BANKS HIT BY CYBERATTACK  •  "
              "TRUMP–XI–PUTIN SUMMIT AFTERMATH")
    para(d, ticker, font(SANS_BOLD, 16), mx, ty + 12, W - 2 * mx,
         fill=INK, leading=22)
    hrule(d, mx, W - mx, H - 44, 2)
    d.text((W // 2, H - 36),
           "THE WORLD IN ONE DAY  —  SATURDAY 21 NOVEMBER 2026",
           font=font(SANS_BOLD, 15), fill=GREY, anchor="ma")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, format="PNG", optimize=True)
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
