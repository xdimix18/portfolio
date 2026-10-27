#!/usr/bin/env python3
"""Generise OG slike (1200x630) za portfolio.ai-sol.me, u stilu sajta.

Fontovi: Instrument Serif (naslovi) + Instrument Sans (tekst), isti kao na sajtu.
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
CANVAS = (250, 249, 247)
INK = (23, 22, 26)
INK2 = (76, 74, 85)
INK3 = (113, 111, 122)
ACCENT = (91, 83, 214)
HAIRLINE = (231, 228, 222)
SOFT_ACCENT = (244, 242, 252)
SOFT_WARM = (251, 238, 231)
PAD = 84

SERIF = f"{FONTS}/InstrumentSerif-Regular.ttf"
SANS = f"{FONTS}/InstrumentSans-Regular.ttf"
SANS_B = f"{FONTS}/InstrumentSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size * SS)


def mark(d, x, y, size, color):
    """Brend mark iz mark.svg, nacrtan kao dva poligona."""
    s = size / 254.63
    outer = [(0, 254.63), (0, 72.75), (36.38, 72.75), (36.38, 36.37), (72.75, 36.37),
             (72.75, 0), (181.88, 0), (181.88, 36.37), (218.26, 36.37), (218.26, 72.75),
             (254.6, 72.75), (254.6, 254.63), (181.85, 254.63), (181.85, 181.88),
             (72.75, 181.88), (72.75, 254.63)]
    inner = [(72.75, 145.5), (181.88, 145.5), (181.88, 72.75), (145.51, 72.75),
             (145.51, 36.37), (109.13, 36.37), (109.13, 72.75), (72.75, 72.75)]
    d.polygon([(x + px * s, y + py * s) for px, py in outer], fill=color)
    d.polygon([(x + px * s, y + py * s) for px, py in inner], fill=CANVAS)


def render(title_lines, sub_lines, chips, place, out):
    img = Image.new("RGB", (W * SS, H * SS), CANVAS)
    d = ImageDraw.Draw(img)

    # mekani akcenti u uglovima, isti ton kao hero na sajtu
    d.ellipse([-260 * SS, -300 * SS, 520 * SS, 300 * SS], fill=SOFT_ACCENT)
    d.ellipse([900 * SS, 430 * SS, 1420 * SS, 900 * SS], fill=SOFT_WARM)

    mark(d, PAD, 78, 46, ACCENT)
    d.text((PAD + 64, 84 * SS), "Dimitrije Ačković", font=font(SANS_B, 22), fill=INK2)
    d.text((PAD + 64, 114 * SS), place, font=font(SANS, 20), fill=INK3)

    for i, line in enumerate(title_lines):
        d.text((PAD, (186 + i * 80) * SS), line, font=font(SERIF, 74), fill=INK)
    for i, line in enumerate(sub_lines):
        d.text((PAD, (372 + i * 36) * SS), line, font=font(SANS, 27), fill=INK2)

    d.line([PAD * SS, 486 * SS, (W - PAD) * SS, 486 * SS], fill=HAIRLINE, width=2 * SS)
    d.text((PAD, 516 * SS), "portfolio.ai-sol.me", font=font(SANS_B, 24), fill=ACCENT)

    x = W - PAD
    for c in chips:
        f = font(SANS, 20)
        w = d.textlength(c, font=f) / SS + 26
        x -= w
        d.rounded_rectangle([x * SS, 508 * SS, (x + w) * SS, 548 * SS],
                            radius=11 * SS, outline=HAIRLINE, width=2 * SS, fill=(255, 255, 255))
        d.text(((x + 13) * SS, 517 * SS), c, font=f, fill=INK2)
        x -= 10

    img.resize((W, H), Image.LANCZOS).save(out, "PNG", optimize=True)
    print(f"OK {out}")


def main():
    render(["Popravim, sklopim", "i postavim."],
           ["Servis i dijagnostika opreme · Elektronika i embedded",
            "AI alati i serveri · 3D dizajn i tehnički crteži"],
           ["Hardver", "AI", "Serveri", "3D dizajn"],
           "Podgorica, Crna Gora", OUT)

    render(["I fix it, build it", "and set it up."],
           ["Device repair · Electronics and embedded",
            "AI tooling and servers · 3D design and drawings"],
           ["Hardware", "AI", "Servers", "3D design"],
           "Podgorica, Montenegro", OUT.replace("og.png", "og-en.png"))


if __name__ == "__main__":
    main()
