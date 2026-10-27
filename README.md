# portfolio

Lični portfolio, **https://portfolio.ai-sol.me**

Statički sajt (HTML + CSS, bez frameworka, bez build koraka, bez JavaScript-a).
Dvojezično: crnogorski na `/`, engleski na `/en/`.

Pozicioniranje: freelancer, usluge i radovi (3D dizajn i štampa, grafički dizajn,
AI alati, serveri, elektronika, servis opreme), a ne klasičan CV studenta.

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
    ├── brand/              # favicon, mark.svg, wordmark.svg, og.png, webmanifest
    └── fonts/              # Instrument Serif + Instrument Sans (woff2, self-hosted)
```

## Dizajn

Svijetla, urednička tema: papirna podloga `#faf9f7`, indigo akcenat `#5b53d6` za
tehnički dio i topla terakota `#b4623c` za dizajn i 3D. Tamna tema je podržana
preko `prefers-color-scheme` (nije potreban prekidač ni JavaScript).

Tipografija: **Instrument Serif** za naslove, **Instrument Sans** za tekst.
Oba fonta su lokalna (`static/fonts/*.woff2`), tako da sajt ne zavisi od tuđih
servera i nema nijedan eksterni zahtjev.

Svi tokeni (boje, radijusi, sjenke, fontovi) su na jednom mjestu, u `:root`
u `static/css/site.css`.

## Sekcije

1. Hero, sa četiri broja i pozivom na upit
2. Usluge, šest kartica (3D, dizajn, AI alati, serveri, elektronika, servis)
3. Odabrani radovi, deset kartica sa SVG ilustracijom umjesto slika
4. Kako radim, četiri pravila
5. Vještine, pet kolona
6. O meni
7. Iskustvo, vremenska linija
8. Kontakt, tamni blok sa emailom, GitHub-om i Instagramom

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

## Licenca

Kod i dizajn: Dimitrije Ačković.
Fontovi Instrument Serif i Instrument Sans su pod SIL OFL 1.1
(`public/static/fonts/OFL-InstrumentSans.txt`).
