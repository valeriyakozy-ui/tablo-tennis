# ATP & WTA Board

A small installable web app for following the 2026 tennis season: the ATP and WTA calendars, tournament draws, the order of play in your own time zone, and live rankings.

**Open the app:** https://valeriyakozy-ui.github.io/tablo-tennis/

## What it does

- **Now** — tournaments that are on right now, your followed players and their next matches, and the order of play for the coming days. Match times are converted to the viewer's local time, and “not before” slots are marked.
- **Calendar** — every ATP and WTA event of the season, filterable by category (Grand Slams, 1000, 500, 250, Finals, team events), with champions and final scores for finished events.
- **Draws** — full brackets for current tournaments. Finished rounds collapse automatically so the players still in the draw stay in view, and large draws can be viewed by quarter.
- **Rankings** — live ATP and WTA top 100 with movement against the latest official ranking. Tap a player to see their 2026 season: titles, finals and how far they went at each tournament, colour-coded by category.
- **My players** — tap ☆ next to any player to follow them. Followed players are highlighted in draws and the order of play and listed at the top of **Now**. The list is stored on the device.
- **ATP / WTA switch** — show one tour or both.
- Works offline with the last loaded data, in light and dark mode.

## Install

The app is a progressive web app, so it installs straight from the browser:

- **iPhone / iPad (Safari):** open the link, tap **Share**, then **Add to Home Screen**.
- **Android (Chrome):** open the link and tap **Install app** in the header, or use the browser menu.
- **Desktop (Chrome or Edge):** click **Install app** in the header or the install icon in the address bar.

## How the data is updated

The data lives in `data/tablo.json`. A scheduled Claude task runs three times a day (09:00, 15:00 and 21:00 Moscow time). It collects fresh results, draws, the order of play and live rankings from public sources, rebuilds `data/tablo.json` with `tools/build_bundle.py` and commits it here. The app picks up the new file the next time it is opened, and every 15 minutes while it is open.

## Project structure

| Path | What it is |
|---|---|
| `index.html` | The whole app: markup, styles and script in one file |
| `data/tablo.json` | Calendars, draws and rankings |
| `manifest.webmanifest`, `sw.js`, `icons/` | Installation and offline support |
| `tools/build_bundle.py` | Rebuilds `data/tablo.json` from exported data documents |

### Data format (short version)

- `seasons.atp` / `seasons.wta` — `{tournaments: [{id, name, city, country, cat, surf, start, end, champ, runner, score, sf, qf, note, draw}]}`
- `draws.<tournament id>` — `{type: "knockout" | "list", rounds: [{name, matches: [{a, b, w, sc, st, t, nb, d}]}]}`, rounds named `R64`, `R32`, `R16`, `QF`, `SF`, `Final`
- `rankings.atp` / `rankings.wta` — live top 100 `{list: [{r, n, p, d, dp}], official: [...], officialDate}`

All times in the data are UTC; the app converts them for display.

## Sources

ATP Tour, WTA, ITF, official tournament websites, Wikipedia, TennisDB, ESPN and rank.tennis. This is an unofficial fan project and is not affiliated with the ATP, the WTA or any tournament.
