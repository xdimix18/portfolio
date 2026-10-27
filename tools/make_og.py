#!/usr/bin/env python3
"""Generise OG slike (1200x630) za portfolio.ai-sol.me, u stilu sajta.

Stil: tema "Gold Blue Sleek Corporate" — navy ploha sa zlatnim linijama,
zlatni serif naslov (Libre Baskerville) i neutralni sans za ostatak (Instrument Sans).
Brend mark se crta rucno, kao dva poligona (putanje iz mark.svg su pravougaone).

Pokretanje:  python3 tools/make_og.py
Izlaz:       public/static/brand/og.png      (MNE)
             public/static/brand/og-en.png   (EN)
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FONTS = os.path.join(HERE, "fonts")
OUT = os.path.join(ROOT, "public/static/brand/og.png")

W, H, SS = 1200, 630, 3  # SS = supersampling, zbog glatkih ivica
NAVY = (31, 33, 71)
NAVY_2 = (42, 45, 92)
NAVY_DEEP = (23, 25, 56)
GOLD = (207, 174, 123)
GOLD_LIGHT = (212, 180, 131)
ON_NAVY = (255, 255, 255)
ON_NAVY_2 = (199, 196, 218)
PAD = 84

SERIF = f"{FONTS}/LibreBaskerville.ttf"
SERIF_I = f"{FONTS}/LibreBaskerville-Italic.ttf"
SANS = f"{FONTS}/InstrumentSans-Regular.ttf"
SANS_B = f"{FONTS}/InstrumentSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size * SS)


def mark(d, x, y, size, color, hole):
    """Brend mark iz mark.svg, nacrtan kao dva poligona."""
    s = size / 254.63
    outer = [(0, 254.63), (0, 72.75), (36.38, 72.75), (36.38, 36.37), (72.75, 36.37),
             (72.75, 0), (181.88, 0), (181.88, 36.37), (218.26, 36.37), (218.26, 72.75),
             (254.6, 72.75), (254.6, 254.63), (181.85, 254.63), (181.85, 181.88),
             (72.75, 181.88), (72.75, 254.63)]
    inner = [(72.75, 145.5), (181.88, 145.5), (181.88, 72.75), (145.51, 72.75),
             (145.51, 36.37), (109.13, 36.37), (109.13, 72.75), (72.75, 72.75)]
    d.polygon([(x + px * s, y + py * s) for px, py in outer], fill=color)
    d.polygon([(x + px * s, y + py * s) for px, py in inner], fill=hole)


def render(title_lines, sub_lines, chips, place, out):
    img = Image.new("RGB", (W * SS, H * SS), NAVY)
    d = ImageDraw.Draw(img)

    # navy gradijent, kao hero na sajtu
    for i in range(H * SS):
        t = i / (H * SS - 1)
        if t < 0.5:
            k = t / 0.5
            c = tuple(round(NAVY_2[j] + (NAVY[j] - NAVY_2[j]) * k) for j in range(3))
        else:
            k = (t - 0.5) / 0.5
            c = tuple(round(NAVY[j] + (NAVY_DEEP[j] - NAVY[j]) * k) for j in range(3))
        d.line([(0, i), (W * SS, i)], fill=c)

    # dijagonalne zlatne linije, kao na tamnim plohama sajta
    line = (38, 41, 84)
    step = 68 * SS
    x0 = -H * SS
    while x0 < W * SS + H * SS:
        d.line([(x0, H * SS), (x0 + H * SS, 0)], fill=line, width=1 * SS)
        x0 += step

    # zlatna linija na dnu, sa ublazenim krajevima
    d.rectangle([0, (H - 3) * SS, W * SS, H * SS], fill=NAVY_DEEP)
    for i in range(60):
        a = i / 59
        x = int((PAD * 0.6 + (W - PAD * 1.2) * a) * SS)
        alpha = 1 - abs(a - 0.5) * 1.5
        if alpha > 0:
            d.rectangle([x, (H - 3) * SS, x + int(W * SS / 60) + 2, (H - 2) * SS], fill=GOLD)

    mark(d, PAD, 74, 44, GOLD, NAVY)
    d.text((PAD + 62, 78 * SS), "DIMITRIJE ACKOVIC", font=font(SANS_B, 20), fill=ON_NAVY)
    d.text((PAD + 62, 108 * SS), place.upper(), font=font(SANS, 17), fill=GOLD_LIGHT)

    y = 190
    for i, (line_txt, italic) in enumerate(title_lines):
        d.text((PAD, y * SS), line_txt, font=font(SERIF_I if italic else SERIF, 66),
               fill=GOLD_LIGHT if not italic else GOLD)
        y += 84

    y += 8
    for line_txt in sub_lines:
        d.text((PAD, y * SS), line_txt, font=font(SANS, 25), fill=ON_NAVY_2)
        y += 34

    d.line([PAD * SS, 500 * SS, (W - PAD) * SS, 500 * SS], fill=(60, 63, 110), width=1 * SS)
    d.text((PAD, 528 * SS), "portfolio.ai-sol.me", font=font(SANS_B, 22), fill=GOLD)

    x = W - PAD
    for c in chips:
        f = font(SANS, 18)
        w = d.textlength(c, font=f) / SS + 30
        x -= w
        d.rectangle([x * SS, 522 * SS, (x + w) * SS, 566 * SS], outline=GOLD, width=1 * SS)
        d.text(((x + 15) * SS, 533 * SS), c.upper(), font=f, fill=GOLD_LIGHT)
        x -= 12

    img.resize((W, H), Image.LANCZOS).save(out, "PNG", optimize=True)
    print(f"OK {out}")


def main():
    render([("Popravim, sklopim", False), ("i postavim.", True)],
           ["Servis i dijagnostika opreme · Elektronika i embedded",
            "AI alati i serveri · 3D dizajn i tehnicki crtezi"],
           ["Hardver", "AI", "Serveri", "3D dizajn"],
           "Podgorica, Crna Gora", OUT)

    render([("I fix it, build it", False), ("and set it up.", True)],
           ["Repair and diagnostics · Electronics and embedded",
            "AI tooling and servers · 3D design and drawings"],
           ["Hardware", "AI", "Servers", "3D design"],
           "Podgorica, Montenegro", OUT.replace("og.png", "og-en.png"))


if __name__ == "__main__":
    main()
