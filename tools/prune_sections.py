#!/usr/bin/env python3
"""
Uklanja pet sekcija/stvari koje je Dimo odbacio (28.10.2026):
  1. "Problemi sa kojima mi ljudi dolaze"  (#problemi / #problems)
  2. proces u 5 koraka ("bez iznenađenja")  -> cetiri pravila OSTAJU
  3. "Dokazi"                               (#dokazi / #proof)
  4. "Pitanja" (FAQ)                        (#pitanja / #questions)
  5. ponavljanje "podaci ostaju kod tebe": .ishod redovi + "lokalno, bez clouda" nota

Plus: nav/footer linkovi, FAQPage JSON-LD, renumeracija sekcija.
"""
import re, pathlib, sys

BASE = pathlib.Path("/app/data/portfolio-site/public")
PAGES = {
    BASE / "index.html": "cnr",
    BASE / "en" / "index.html": "en",
}

DROPPED_SECTIONS = ["problemi", "problems", "dokazi", "proof", "pitanja", "questions"]

# stara oznaka -> nova oznaka (posle uklanjanja 01, 05, 06)
RENUM = {
    "cnr": [
        ("02 \u00b7 Usluge", "01 \u00b7 Usluge"),
        ("03 \u00b7 Odabrani radovi", "02 \u00b7 Odabrani radovi"),
        ("04 \u00b7 Kako te\u010de posao", "03 \u00b7 Kako radim"),
        ("07 \u00b7 Alati koje koristim", "04 \u00b7 Alati koje koristim"),
        ("08 \u00b7 O meni", "05 \u00b7 O meni"),
        ("09 \u00b7 Iskustvo", "06 \u00b7 Iskustvo"),
    ],
    "en": [
        ("02 \u00b7 Services", "01 \u00b7 Services"),
        ("03 \u00b7 Selected work", "02 \u00b7 Selected work"),
        ("04 \u00b7 How the work runs", "03 \u00b7 How I work"),
        ("07 \u00b7 Tools I use", "04 \u00b7 Tools I use"),
        ("08 \u00b7 About", "05 \u00b7 About"),
        ("09 \u00b7 Experience", "06 \u00b7 Experience"),
    ],
}

# proces: ukloniti uvodni sec-head sa "Pet koraka" i blok .steps, ostaviti pravila
PROCES_HEAD = {
    "cnr": (
        '    <div class="sec-head">\n'
        '      <h2>Pet koraka, bez iznena\u0111enja</h2>\n'
        '      <p>Isto radi i za popravku jednog ure\u0111aja i za postavljanje servera. '
        'Zna\u0161 u kojem smo koraku u svakom trenutku.</p>\n'
        '    </div>\n\n'
    ),
    "en": (
        '    <div class="sec-head">\n'
        '      <h2>Five steps, no surprises</h2>\n'
        '      <p>The same applies to repairing one device and to setting up a server. '
        'You know which step we are on at any point.</p>\n'
        '    </div>\n\n'
    ),
}

# nota koju treba skloniti ("lokalno, bez clouda" / "local, no cloud")
NOTE = {
    "cnr": '          <div class="card-foot"><span class="card-note">lokalno, bez clouda</span></div>\n',
    "en": '          <div class="card-foot"><span class="card-note">local, no cloud</span></div>\n',
}


def strip_section(html, sec_id):
    """Ukloni <section id="sec_id" ...> ... </section> (bez ugnijezdenih section)."""
    pat = re.compile(
        r'\n<section id="%s"[^>]*>.*?</section>\n' % re.escape(sec_id),
        re.DOTALL,
    )
    return pat.sub("\n", html, count=1), bool(pat.search(html))


def strip_steps(html):
    """Ukloni blok .steps iz sekcije proces."""
    return re.sub(r'    <div class="steps">.*?</div>\n\n', "", html, count=1, flags=re.DOTALL)


for path, lang in PAGES.items():
    src = path.read_text(encoding="utf-8")
    before = len(src)
    log = []

    # 1. sekcije
    for sid in DROPPED_SECTIONS:
        src, found = strip_section(src, sid)
        if found:
            log.append("sekcija #" + sid)

    # 2. proces: uvod + koraci
    if PROCES_HEAD[lang] in src:
        src = src.replace(PROCES_HEAD[lang], "", 1)
        log.append("uvod procesa")
    src2 = strip_steps(src)
    if src2 != src:
        log.append("5 koraka")
        src = src2

    # 3. .ishod redovi (svih 10)
    n_ishod = len(re.findall(r'\n *<p class="ishod">.*?</p>', src, re.DOTALL))
    src = re.sub(r'\n *<p class="ishod">.*?</p>', "", src, flags=re.DOTALL)
    if n_ishod:
        log.append("%d ishod redova" % n_ishod)

    # 4. nota "lokalno, bez clouda"
    if NOTE[lang] in src:
        src = src.replace(NOTE[lang], "", 1)
        log.append("nota bez clouda")

    # 5. nav + footer linkovi ka uklonjenim sekcijama
    for sid in DROPPED_SECTIONS:
        src = re.sub(r'\n *<a href="#%s">[^<]*</a>' % re.escape(sid), "", src)

    # 6. FAQPage iz JSON-LD
    n_faq = len(re.findall(r'\{"@type":"FAQPage".*?\}\n', src, re.DOTALL))
    # ukloni i zavrni zarez prethodnog bloka u @graph
    src = re.sub(r',\n\{"@type":"FAQPage".*?\}\]\}', "]}\n", src, flags=re.DOTALL)
    if n_faq:
        log.append("FAQPage JSON-LD")

    # 7. renumeracija
    for old, new in RENUM[lang]:
        if old in src:
            src = src.replace(old, new)
    log.append("renumerisano")

    # 8. pocisti prazne redove nastale brisanjem
    src = re.sub(r"\n{3,}", "\n\n", src)

    path.write_text(src, encoding="utf-8")
    print("%-34s %6d -> %6d  (-%d)  | %s" % (
        path.relative_to(BASE), before, len(src), before - len(src), ", ".join(log)))
