# vercel_shared_bible

Static multi-page site (no build step, no server). Deployed as the Vercel project
`commentary` -> https://commentary-rust.vercel.app

| Page | URL | What it is |
| --- | --- | --- |
| `index.html` | `/` | Landing menu. Opens nothing by itself - you pick a page. |
| `commentary.html` | `/commentary` | Two panes: Berean Standard Bible beside commentary (John Gill for the OT, Matthew Henry for the NT), both fetched live from the HelloAO API (https://bible.helloao.org). |
| `chinese.html` | `/chinese` | Genesis in Chinese as tappable word chips - dwell 700 ms or tap for pinyin + gloss, with a WEB English reveal. Reads `chinese_breakdown.json` and `genesis_web.json` from this folder. |

In `commentary.html`, pane 2 can switch between commentary and the book introductions
in `bible_intro/`. Intro mode also shows the generated chapter summaries from
`summaries/`, with clickable verse ranges. Run `python3 generate_bible_intro.py` after
editing an introduction to rebuild the static `bible_intro.json` bundle.

`cleanUrls` in `vercel.json` is what serves `/commentary` and `/chinese` without the
`.html`; the old `/commentary.html` style URLs still work and redirect to the short form.

## Adding a page

1. Drop `page2.html` in this folder (plain HTML - include `<!DOCTYPE html>`, charset and
   viewport yourself; each page is standalone).
2. Add one line to the `PAGES` list near the bottom of `index.html`:

   ```js
   { href: 'page2.html', name: 'Page 2', tint: '#4f46e5', blurb: 'What it does.' }
   ```

3. Give the page an `<a class="home" href="/">` link so there is a way back.
