# Brend assets (generisano)

Ne mijenjati rucno — generisano skriptom:

```
python3 tools/build_brand_assets.py --src <folder sa Asset 3.svg>
```

| fajl | namjena |
|---|---|
| `mark.svg` | kvadratni znak, `currentColor` (nav, footer, ikonice) |
| `wordmark.svg` | puni znak, `currentColor` (krupna dekoracija) |
| `favicon.svg`, `favicon-*.png` | ikonica sajta u tabu |
| `apple-touch-icon.png` | ikonica na iOS pocetnom ekranu |
| `og.png` | pregled linka na drustvenim mrezama (1200x630) |

Izvor: `Asset 3.svg` (sha256:9588baccd597b0f5...), rotiran iz izvora 90 stepeni u smjeru
kazaljke (izvor je bio CCW) i preveden u `currentColor`.
