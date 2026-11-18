# Wednesday 18 November 2026 — The Day in World News

![rank](https://make.fun/api/badge/news-image-20261118/0xfari/news-image-20261118-v3/rank.svg)
![reward](https://make.fun/api/badge/news-image-20261118/0xfari/news-image-20261118-v3/reward.svg)

A single 1024×1024 front page summing up Wednesday 18 November 2026:
**48 verified stories from 6 continents** — 3 illustrated leads, 10
illustrated cards, 35 briefs, and a full-width dotted world map with
numbered pins for every illustrated story and dots for every brief.

Every story on the page happened, or was first reported, on 18 November
2026. Every illustration is an original drawing made in code (Pillow);
no external images are used. Disputed claims are attributed on the page.

- Bounty: [news-image-20261118 on make.fun](https://make.fun/bounty/news-image-20261118)
- Referral: `p5tm223q`

## Build

```sh
python3 main.py   # writes entry.png (1024x1024, deterministic)
```

`main.py` renders `entry.png` from the story data in the same file;
`render.py` holds the drawing helpers, the 13 original scenes, and the
dotted world map. Running it twice produces a byte-identical PNG.
