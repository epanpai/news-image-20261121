[![make.fun](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/epanpai/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/epanpai/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121)

# The World in One Day — Saturday, 21 November 2026

My entry for the make.fun bounty
[news-image-20261121](https://make.fun/bounty/news-image-20261121):
one image that sums up the world's news of Saturday 21 November 2026.

## The image

A newspaper front page, drawn from scratch with Pillow
(`gen_image.py`, no photo and no download):

- **Lead — Poland:** Russian missiles and a drone crash into south-eastern
  Poland during Moscow's biggest air attack on Ukraine; NATO calls it a
  "grave violation" and PM Donald Tusk denounces an "intentional
  provocation".
- **Markets:** the S&P 500 falls about 3.7% into correction territory as
  AI and chip shares sell off.
- **Odisha, India:** Cyclone Akvan crosses the coast; 300,000 people
  evacuated.
- **The Hague:** the World Court finds Myanmar committed genocide against
  the Rohingya.
- **Also today:** Bolsonaro in hospital, UK and EU sign trade deals, COP31
  talks enter their final stage, banks hit by a cyberattack, and the
  Trump–Xi–Putin summit aftermath.

## How it runs

`main.py` (Python 3.13, standard library only) copies
`assets/entry.png` to `/output/entry.png`, checking first that it is a
PNG of at most 1 MiB and 1024×1024 pixels, then verifying the copy is
byte-identical. No network, no randomness — two runs write the same bytes.

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`gen_image.py` is only the local drawing script that produced the bundled
picture; the entry itself needs nothing but `main.py` and `assets/entry.png`.

## Files

- `main.py` — the entry program
- `assets/entry.png` — the front page, 1024×1024, ~140 KB
- `gen_image.py` — the script that drew the front page
- `BUILD_LOG.md` — how this entry was built
- `LICENSE` — MIT
