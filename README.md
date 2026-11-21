# news-image-20261121

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/djkaz97-cmd/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/djkaz97-cmd/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

**The World Ledger — Saturday, 21 November 2026.** One 1024×1024 PNG that sums
up the day's world news as a newspaper front page: masthead and dateline naming
the day, a lead story with an illustrated panorama, six story cards across
regions and beats, and a news ticker.

The day on the page:

- **Lead — GTA VI launches worldwide** (entertainment/gaming), with a Vice City dusk panorama
- **BepiColombo enters Mercury orbit** (science, ESA–JAXA)
- **Alcaraz unbeaten at the ATP Finals in Turin** (tennis)
- **COP31 goes to overtime in Antalya** (climate)
- **UK–EU sign new post-Brexit agreements in Brussels** (diplomacy)
- **AI chip selloff pulls the S&P 500 into correction** (markets)
- **India–NZ cricket test goes to the wire** (sport, Asia)
- Ticker: **F1 Las Vegas Grand Prix** under the lights

The image is rendered once at build time (`build/render.py`, Pillow + system
fonts) and shipped as `entry.png`. At runtime the entry is just `main.ts`,
which validates the PNG (magic bytes, 1 MiB cap, 1024×1024 dimensions) and
copies it to the output directory — no network, no randomness, so both grader
runs write identical bytes.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

In make.fun's sandbox the program writes `/output/entry.png`.

## Regenerate the image (optional, build-time only)

```sh
python build/render.py   # needs Pillow and Windows fonts (Georgia, Arial Bold, Impact)
```

## License

MIT — see [LICENSE](LICENSE).

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
