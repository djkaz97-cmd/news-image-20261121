# Task: news-image-20261121 entry — make.fun bounty ($100, closes 2026-11-23T00:00:00 UTC)

Build this entry in this session (make.fun BUNDLE mode — parent bundles + submits after). Write every source file yourself. Never ask questions. Do NOT submit, do NOT pay, never print API keys.

REPO: C:/Users/Kaz/makefun-bounties/entries/news-image-20261121 — completely empty. Create everything from scratch.
Kit: C:/Users/Kaz/makefun-bounties/news-image-20261121-kit/news-image-20261121-kit — read RULES.txt fully first.

THE TASK
Write one image that sums up world news of Saturday 21 November 2026 to /output/entry.png.
- PNG or JPEG, named entry.png, at most 1 MiB (1048576 bytes), at most 1024x1024 px.
- The judge (z-ai/glm-5.3-flash via OpenRouter) has no news feed; it compares images. It looks for: names the day (21 Nov 2026), specific recognisable events of that day, breadth across regions/fields, reads clearly at ~300px, faithful without hype, clean composition with legible text.
- No network at runtime: the entry is just the image + a one-line program that copies it.
- Prior entry (news-image-20261120) scored ~94% win rate against house images — reuse that proven style: newspaper front page, masthead with date, lead story + story cards, ticker, illustration.

RESOURCES
- gh: C:/Users/Kaz/AppData/Local/Programs/gh/bin/gh.exe
- Python+Pillow: C:/Users/Kaz/AppData/Local/hermes/tools/youtube-venv/Scripts/python.exe
- Node on PATH
- Keypair: C:/Users/Kaz/makefun-bounties/makefun-keypair.json (wallet 5bUR9FL3rTeevwqZC97oH7agHyQqJD9H6C2jW4DGcLUk)

STEPS
1. cd C:/Users/Kaz/makefun-bounties/entries/news-image-20261121
2. Inspect C:/Users/Kaz/makefun-bounties/news-image-20261121-kit/news-image-20261121-kit/starter/main.ts — the proven pattern: reads entry.png beside itself, checks PNG magic + <=1048576 bytes, mkdir + write to MAKEFUN_OUTPUT_DIR ?? /output, log bytes.
3. Render entry.png at build time with Pillow: a newspaper front page dated Saturday 21 November 2026. CONTENT SAFETY (critical): the model provider's safety filter rejects graphic violence, war attacks/casualties, genocide, or protest-violence text — keep EVERY headline/deck neutral and non-graphic or the build dies. Use these safe, specific, recognisable angles for breadth: GTA VI launch (gaming/entertainment), BepiColombo enters Mercury orbit (science/ESA-JAXA), Alcaraz unbeaten at ATP Finals Turin (sports/Europe), COP31 climate summit overtime in Antalya (climate/global), UK-EU post-Brexit agreements signed in Brussels (politics/Europe), AI chip selloff / S&P 500 correction (markets/tech), India vs NZ cricket test (sports/Asia), F1 Las Vegas GP (sport). Phrase diplomacy/economy neutrally; NO war-attack, genocide or casualty detail. 1024x1024, deep teal/orange palette, masthead with the date, lead story image, 4-6 story cards, ticker. Use Windows fonts (C:/Windows/Fonts/: georgia.ttf, georgiab.ttf, arialbd.ttf, impact.ttf) at build time only — repo ships just the PNG.
4. Verify entry.png: <=1 MiB, exactly 1024x1024, valid PNG (Pillow).
5. Write main.ts at root (copy starter pattern, your own code).
6. LICENSE: MIT text WITH `SPDX-License-Identifier: MIT`.
7. .makefun/owner.json: {"wallet": "5bUR9FL3rTeevwqZC97oH7agHyQqJD9H6C2jW4DGcLUk"}
8. .gitignore: out/, __pycache__/
9. Test: mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts; verify out/entry.png byte-identical to entry.png.
10. Git init -b main, add all, commit, push to GitHub.
11. Create PUBLIC GitHub repo djkaz97-cmd/news-image-20261121 if not exists: gh repo create --public --source C:/Users/Kaz/makefun-bounties/entries/news-image-20261121 --push --homepage https://make.fun/bounty/news-image-20261121 (or git push origin main if exists).
12. gh repo edit --add-topic makefun,ai-agents,bounties,growth.
13. README.md: title + 3 live make.fun badges for news-image-20261121 (owner djkaz97-cmd, repo news-image-20261121):
    [![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
    [![rank](https://make.fun/badge/news-image-20261121/djkaz97-cmd/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
    [![reward](https://make.fun/badge/news-image-20261121/djkaz97-cmd/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
14. AGENTS.md: rewrite this file in your own words.
15. Do NOT submit — parent handles it.

FINAL REPORT: commit sha, repo URL, entry.png bytes/dimensions, check results if you run it, blockers. Do NOT submit.
