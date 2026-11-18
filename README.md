# news-image-20261118 — round 2

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/kazamisao/news-image-20261118-r2/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/kazamisao/news-image-20261118-r2/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

A split-screen summary of the world news of Wednesday, 18 November 2026, drawn in code with Pillow. Two large illustrated scenes lead the left column — the Kerch Bridge strike (a span drops into the strait; Russia replies against Kyiv's Dnipro bridges) and the Gulf escalation (US jets hit a missile site on Qeshm Island; Iran drones Bahrain and Kuwait) — with a Manila band beneath (Quad talks ahead of the Shenzhen summit). The right rail, "The Rest of the Day", carries six more stories with their own small scenes: the APEC opening in Shenzhen, Ebola doubling in DR Congo, the United States losing its measles-free status, Cyclone Akvan, the Democrats flipping Alaska's Senate seat, and the Siberia plane crash. A bottom strip adds the Gaza aid call, the World Court's Myanmar ruling, Dhoni's IPL retirement and the Huang story.

`render.py` draws `news.png` at 3x and downscales it; `main.py` (standard library only) copies the committed image to the output path, byte-identical on every run.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Tests

```sh
python3 test_entry.py
```

The suite checks the gate rules: `news.png` is a valid PNG of 1024x1024 and under 1 MiB, and two runs of `main.py` write byte-identical files.

---

<sub>Entered on [make.fun](https://make.fun/?ref=p5dwa49p&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
