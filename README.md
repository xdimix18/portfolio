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
├── make_qr.py              # generise QR vizit kartu (85x55 mm, PNG + PDF)
├── out/                    # izlaz make_qr.py (nije u gitu)
└── fonts/                  # TTF verzije istih fontova, samo za generisanje slika
```

## Dizajn

Tema **"Gold Blue Sleek Corporate"** (po Canva dizajnu, `canva.link/eyn7mznfnefinla`):
duboko mornarsko plava `#1f2147` i toplo zlato `#cfae7b` na papirnoj podlozi
`#f5f2ee`. **Bez sjenki** — dubina se dobija samo bojom i linijom od 1 px.

Ivice: trake, paneli i dugmad ostaju oštri (radius 0), a **kartice sa sadržajem
su blago zaobljene (14px) i razdvojene razmakom od 18px, bez spojenih tabelarnih
ivica** — `.svc-card` (usluge), `.card` (radovi), `.skill-col` (vještine) i
`.facts` (podaci u sekciji O meni, kao mreža zaobljenih polja 2x3, na mobitelu 1
kolona). Tamna tema je podržana preko `prefers-color-scheme` (nije potreban
prekidač ni JavaScript).

Tipografija: **Libre Baskerville** za naslove (visokokontrastni serif),
**Instrument Sans** za tekst. Oba fonta su lokalna (`static/fonts/*.woff2`),
tako da sajt ne zavisi od tuđih servera i nema nijedan eksterni zahtjev.

Svi tokeni (boje, radijusi, sjenke, fontovi) su na jednom mjestu, u `:root`
u `static/css/site.css`. Dugme u primarnoj boji koristi `--accent-ink`, koji se
mijenja uz temu, da kontrast ostane iznad 5:1 i u svijetloj i u tamnoj varijanti.

## Sekcije

1. Hero: obećanje sa posljedicom za klijenta („rade bez tuđeg clouda"), ne lista usluga
2. Traka sa četiri broja
3. **Usluge** u dvije grupe: **Ono po čemu me zovu** (servis, elektronika, serveri, AI) i
   podređena grupa **Takođe radim** (3D dizajn, grafički dizajn)
4. **Odabrani radovi** — deset kartica; tri projekta imaju `Za tebe:` liniju sa onim što klijent dobija
5. **Kako radim** — četiri pravila koja se ne mijenjaju
6. **Alati koje koristim** — tri kolone bez izmišljenih nivoa
7. O meni
8. Iskustvo, vremenska linija
9. Kontakt, tamni blok sa emailom i GitHub-om; muzika je sitnim tekstom u uglu

Privatnost podataka se pominje **jednom**, u heroju („bez tuđeg clouda"). Ranije se
ponavljala na svakoj kartici radova, u servisnoj kartici i u pravilima; to je uklonjeno
28.10.2026. Iz istog prolaza su izbačene i sekcije „Zvuči poznato?", proces u pet
koraka, „Dokazi" i FAQ.

### Napomena o emailu

Na sajtu je **`dimitrije.ackovic18@gmail.com`**, namjerno. Provjereno je da
`dimitrije@ai-sol.me` **ne dostavlja** poruke: test poslan sa eksternog
(univerzitetskog) naloga nije stigao ni u INBOX, ni u Spam, ni u All Mail, dok isti
nalog inače uredno komunicira sa Gmail-om. Domen ima MX (Cloudflare routing) i SPF,
ali odredište nije verifikovano, a API token nema pravo na `email_routing`.

Kad se to provjeri u dashboardu (Email → Email Routing → Destination addresses), na
sajtu se adresa mijenja u dva fajla, na tri mjesta (`mailto:` u navigaciji, herou i
kontaktu) plus u `application/ld+json`.

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

QR vizit karta za terenske izlaske (85x55 mm, 300 dpi, PNG + PDF, u `tools/out/`):

```bash
python3 tools/make_qr.py     # vizit-karta-mne i vizit-karta-en
```

## Licenca

Kod i dizajn: Dimitrije Ačković.
Fontovi Instrument Serif i Instrument Sans su pod SIL OFL 1.1
(`public/static/fonts/OFL-InstrumentSans.txt`).
