#!/usr/bin/env python3
"""Generise QR vizit kartu za terenske izlaske, u stilu sajta.

Izlaz (u tools/out/):
  vizit-karta-mne.png / .pdf   -> QR vodi na https://portfolio.ai-sol.me/
  vizit-karta-en.png  / .pdf   -> QR vodi na https://portfolio.ai-sol.me/en/

Stil: navy ploha, zlatni QR, Libre Baskerville za naslov.
Kartica je 85x55 mm (standard, staje u novcanik i u dzep) na 300 dpi.

Pokretanje: python3 tools/make_qr.py
"""
import os
import qrcode
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FONTS = os.path.join(HERE, "fonts")
OUTDIR = os.path.join(HERE, "out")

NAVY = (31, 33, 71)
NAVY_2 = (42, 45, 92)
NAVY_DEEP = (23, 25, 56)
GOLD = (207, 174, 123)
GOLD_LIGHT = (212, 180, 131)
ON_NAVY = (255, 255, 255)
ON_NAVY_2 = (199, 196, 218)

SERIF = f"{FONTS}/LibreBaskerville.ttf"
SANS = f"{FONTS}/InstrumentSans-Regular.ttf"
SANS_B = f"{FONTS}/InstrumentSans-Bold.ttf"

# 85 x 55 mm na 300 dpi
DPI = 300
MM = DPI / 25.4
W, H = round(85 * MM), round(55 * MM)
SS = 2  # supersampling


def font(path, size):
    return ImageFont.truetype(path, int(size * SS))


def mark(d, x, y, size, color, hole):
    """Brend mark iz mark.svg, kao dva poligona."""
    s = size / 254.63
    outer = [(0, 254.63), (0, 72.75), (36.38, 72.75), (36.38, 36.37), (72.75, 36.37),
             (72.75, 0), (181.88, 0), (181.88, 36.37), (218.26, 36.37), (218.26, 72.75),
             (254.6, 72.75), (254.6, 254.63), (181.85, 254.63), (181.85, 181.88),
             (72.75, 181.88), (72.75, 254.63)]
    inner = [(72.75, 145.5), (181.88, 145.5), (181.88, 72.75), (145.51, 72.75),
             (145.51, 36.37), (109.13, 36.37), (109.13, 72.75), (72.75, 72.75)]
    d.polygon([(x + px * s, y + py * s) for px, py in outer], fill=color)
    d.polygon([(x + px * s, y + py * s) for px, py in inner], fill=hole)


def make_qr(url, size):
    """Zlatni QR na navy podlozi. quiet_zone nula, jer podloga vec daje kontrast."""
    q = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_Q,  # 25% tolerancije
        box_size=10,
        border=0,
    )
    q.add_data(url)
    q.make(fit=True)
    img = q.make_image(fill_color="white", back_color="black").convert("L")
    img = img.resize((size, size), Image.NEAREST)

    # crni moduli -> zlato, bijeli -> providno (navy ispod)
    out = Image.new("RGBA", (size, size), NAVY + (0,))
    px = img.load()
    op = out.load()
    for yy in range(size):
        for xx in range(size):
            if px[xx, yy] < 128:  # tamni modul
                op[xx, yy] = GOLD + (255,)
    return out


def render(url, title_lines, name, role, place, out_png):
    img = Image.new("RGB", (W * SS, H * SS), NAVY)
    d = ImageDraw.Draw(img)

    # navy gradijent
    for i in range(H * SS):
        t = i / (H * SS - 1)
        if t < 0.5:
            k = t / 0.5
            c = tuple(round(NAVY_2[j] + (NAVY[j] - NAVY_2[j]) * k) for j in range(3))
        else:
            k = (t - 0.5) / 0.5
            c = tuple(round(NAVY[j] + (NAVY_DEEP[j] - NAVY[j]) * k) for j in range(3))
        d.line([(0, i), (W * SS, i)], fill=c)

    # dijagonalne linije
    step = int(34 * SS)
    x0 = -H * SS
    while x0 < W * SS + H * SS:
        d.line([(x0, H * SS), (x0 + H * SS, 0)], fill=(38, 41, 84), width=1 * SS)
        x0 += step

    # zlatna linija lijevo (akcenat)
    d.rectangle([0, 0, int(3 * SS), H * SS], fill=GOLD)

    pad = int(6 * MM)
    mark(d, pad, pad, int(5.2 * MM), GOLD, NAVY)
    d.text((pad + int(7 * MM), pad + int(0.6 * MM)), name, font=font(SANS_B, 10),
           fill=ON_NAVY)
    d.text((pad + int(7 * MM), pad + int(4.3 * MM)), role, font=font(SANS, 8),
           fill=GOLD_LIGHT)

    # naslov, serif
    y = int(20 * MM)
    for txt, italic in title_lines:
        d.text((pad, y), txt, font=font(SERIF, 15),
               fill=GOLD if italic else GOLD_LIGHT)
        y += int(7 * MM)

    # donja linija
    d.line([pad, int(47 * MM), W * SS - int(31 * MM), int(47 * MM)],
           fill=(60, 63, 110), width=1 * SS)
    d.text((pad, int(48.6 * MM)), "portfolio.ai-sol.me", font=font(SANS_B, 9), fill=GOLD)
    d.text((pad, int(51.4 * MM)), place, font=font(SANS, 8), fill=ON_NAVY_2)

    # QR, desno, u zlatnom okviru
    qr_size = int(30 * MM) * SS
    qr = make_qr(url, qr_size)
    qx, qy = W * SS - pad - qr_size, (H * SS - qr_size) // 2
    frame = int(1.6 * MM) * SS
    d.rectangle([qx - frame, qy - frame, qx + qr_size + frame, qy + qr_size + frame],
                fill=NAVY_DEEP, outline=GOLD, width=max(1, int(0.35 * MM * SS)))
    img.paste(qr, (qx, qy), qr)

    final = img.resize((W, H), Image.LANCZOS)
    final.save(out_png, "PNG", optimize=True, dpi=(DPI, DPI))
    final.save(out_png.replace(".png", ".pdf"), "PDF", resolution=DPI)
    print(f"OK {out_png}  ({W}x{H} px, 85x55 mm @ {DPI} dpi)")


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    place_mne = "Podgorica, Crna Gora · crnogorski, engleski"
    place_en = "Podgorica, Montenegro · English, Montenegrin"

    render("https://portfolio.ai-sol.me/",
           [("Sredjujem hardver", False), ("i postavljam alate.", True)],
           "DIMITRIJE ACKOVIC", "Servis · Serveri · AI alati",
           place_mne, os.path.join(OUTDIR, "vizit-karta-mne.png"))

    render("https://portfolio.ai-sol.me/en/",
           [("I fix hardware and", False), ("set up the tools.", True)],
           "DIMITRIJE ACKOVIC", "Repair · Servers · AI tooling",
           place_en, os.path.join(OUTDIR, "vizit-karta-en.png"))


if __name__ == "__main__":
    main()
