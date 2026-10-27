# portfolio

Lični portfolio, **https://portfolio.ai-sol.me**

Statički sajt (HTML + CSS, bez frameworka, bez build koraka, bez JavaScript-a).
Dvojezično: crnogorski na `/`, engleski na `/en/`.

Pozicioniranje: freelancer, usluge i radovi. Redoslijed je namjeran: **prvo hardver,
elektronika, AI alati i serveri**, pa tek onda dizajn i 3D. 3D štampa se ne nudi kao
usluga (nema više štampača) nego 3D dizajn i modelovanje, sa izradom preko partnera.

## Struktura

```
public/
├── index.html              # MNE verzija (default)
├── en/index.html           # EN verzija
├── 404.html                # brendirana 404 stranica
├── robots.txt
├── sitemap.xml
├── _headers                # cache + sigurnosni headeri (Cloudflare)
└── static/
    ├── css/site.css        # kompletan dizajn sistem (jedan fajl)
    ├── brand/              # favicon, mark.svg, wordmark.svg, og.png, og-en.png, webmanifest
    └── fonts/              # Libre Baskerville + Instrument Sans (woff2, self-hosted)

tools/
├── make_og.py              # generise obje OG slike (1200x630)
└── fonts/                  # TTF verzije istih fontova, samo za generisanje OG slike
```

## Dizajn

Tema **"Gold Blue Sleek Corporate"** (po Canva dizajnu, `canva.link/eyn7mznfnefinla`):
duboko mornarsko plava `#1f2147` i toplo zlato `#cfae7b` na papirnoj podlozi
`#f5f2ee`. **Oštre ivice (radius 0), bez sjenki** — dubina se dobija samo bojom i
linijom od 1 px. Tamna tema je podržana preko `prefers-color-scheme` (nije
potreban prekidač ni JavaScript).

Tipografija: **Libre Baskerville** za naslove (visokokontrastni serif),
**Instrument Sans** za tekst. Oba fonta su lokalna (`static/fonts/*.woff2`),
tako da sajt ne zavisi od tuđih servera i nema nijedan eksterni zahtjev.

Svi tokeni (boje, radijusi, sjenke, fontovi) su na jednom mjestu, u `:root`
u `static/css/site.css`. Dugme u primarnoj boji koristi `--accent-ink`, koji se
mijenja uz temu, da kontrast ostane iznad 5:1 i u svijetloj i u tamnoj varijanti.

## Sekcije

1. Hero, sa četiri broja (bez obećanja o roku odgovora)
2. Usluge, šest kartica: servis, elektronika, AI alati, serveri, 3D dizajn, grafički dizajn
3. Odabrani radovi, deset kartica, dizajn i 3D idu na kraju
4. Kako radim, četiri pravila
5. Vještine, pet kolona, dizajn je predzadnji
6. O meni
7. Iskustvo, vremenska linija
8. Kontakt, tamni blok sa emailom i GitHub-om; muzika je sitnim tekstom u uglu

## Cloudflare postavke

| Postavka | Vrijednost |
|---|---|
| Projekat | `dimo-portfolio` (tip: Worker + Static Assets) |
| Production branch | `main` |
| Framework preset | None |
| Build command | *(prazno)* |
| Build output directory | `public` |
| Custom domain | `portfolio.ai-sol.me` |

Bez build koraka, hosting samo servira fajlove iz `public/`. Svaki push na `main`
pokreće novi deploy.

Poznato: custom `404.html` se trenutno ne servira jer u konfiguraciji assets-a
nije postavljeno `not_found_handling: "404-page"`. Fajl je ispravan i brendiran,
čeka samo tu jednu postavku.

## Lokalni pregled

```bash
python3 -m http.server 8092 --directory public
# http://127.0.0.1:8092
```

## Push

```bash
bash push.sh "poruka commita"
```

Deploy key (`/app/data/.ssh/id_ed25519_portfolio`) važi samo za `xdimix18/portfolio`.

## Izmjene sadržaja

Sve je u dva HTML fajla (`public/index.html` i `public/en/index.html`), bez
templatinga i generatora. Izmjena teksta je izmjena HTML-a, commit i push.
Kad mijenjaš jedno jezičko izdanje, promijeni i drugo da ostanu usklađeni.

OG slike se ne mijenjaju ručno:

```bash
python3 tools/make_og.py     # upisuje og.png (MNE) i og-en.png (EN)
```

## Licenca

Kod i dizajn: Dimitrije Ačković.
Fontovi Instrument Serif i Instrument Sans su pod SIL OFL 1.1
(`public/static/fonts/OFL-InstrumentSans.txt`).
