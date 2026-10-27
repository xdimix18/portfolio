# portfolio

Lični portfolio — **https://portfolio.ai-sol.me**

Statički sajt (HTML + CSS, bez frameworka, bez build koraka, bez JavaScript-a),
hostovan na **Cloudflare Pages** iz ovog repoa. Dvojezično: crnogorski na `/`,
engleski na `/en/`.

## Struktura

```
public/
├── index.html              # MNE verzija (default)
├── en/index.html           # EN verzija
├── 404.html                # Cloudflare Pages 404
├── robots.txt
├── sitemap.xml
├── _headers                # Cloudflare Pages headers (cache + sigurnost)
└── static/
    ├── css/site.css        # kompletan dizajn sistem (jedan fajl)
    ├── brand/              # favicon, mark.svg, wordmark.svg, og.png, webmanifest
    └── fonts/              # Press Start 2P (pixel font za eyebrow/badge), OFL licenca
```

## Cloudflare Pages postavke

| Postavka | Vrijednost |
|---|---|
| Project name | `dimo-portfolio` |
| Production branch | `main` |
| Framework preset | None |
| Build command | *(prazno)* |
| Build output directory | `public` |
| Custom domain | `portfolio.ai-sol.me` |

Bez build koraka — Cloudflare samo servira fajlove iz `public/`.
Svaki push na `main` = novi deploy. Svaka druga grana = preview URL.

## Lokalni pregled

```bash
python3 -m http.server 8092 --directory public
# http://127.0.0.1:8092
```

## Dizajn

Dizajn sistem je naslijeđen sa AI Solutions portala (dark canvas `#010102`,
ljubičasto-plavi akcenat `#5e6ad2`, hairline ivice `#23252a`), da se odmah
vidi da je isti brend. Tokeni su na jednom mjestu, u `:root` u `static/css/site.css`.

Fontovi: **Inter** za tekst (Google Fonts), **Press Start 2P** samo za kratke
natpise (eyebrow, badge, sekcijske oznake) — nikad za duži tekst.

## Izmjene sadržaja

Sve je u dva HTML fajla (`public/index.html` i `public/en/index.html`) — nema
templatinga ni generatora. Izmjena teksta = izmjena HTML-a, commit, push.
Ako mijenjaš jedno jezičko izdanje, promijeni i drugo da ostanu usklađeni.

## Licenca

Kod i dizajn: Dimitrije Ačković. Font Press Start 2P je pod SIL OFL 1.1
(`public/static/fonts/OFL.txt`).
