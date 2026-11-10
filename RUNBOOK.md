# Daily Verse Parables: runbook for the daily run

Each run makes **two** new videos and stops there. Each video is 18 seconds, 1080x1920 and 30 fps, and loops seamlessly.
The look: a cream background, black silhouettes, three stacked panels, and one CPDV verse per panel.
Day 1 to day 7 (`episodes/ep001`–`ep007`) are the reference for quality and style. Read two of them before writing anything new.

## 0. Setup (fresh workspace)
```
./setup.sh            # installs pycairo/numpy, downloads data/CPDV.json, checks fonts
```

## 1. Pick the next two stories
- Take the first two items in `queue.json` → `queue`. Their refs and ideas are suggestions only.
- Numbering: the next day number is the last `done[].day` plus 1, then plus 2.
- Choose three verses that tell **one story in three outcomes**. Every panel starts the same way and then the outcomes split, as in the original sample, where three people shoot the same basketball.
  The best formats are: two who fail and one who perseveres, three different responses, or a contrast in what's chosen.
- Look up the exact text with `from engine import verse; verse("Luke", 15, 4)`.
  The JSON uses names like `I Samuel`, `I Kings` and `Revelation of John`. On screen, write `1 Samuel`, `1 Kings`, `Revelation`.
  Psalms use **Vulgate numbering**: Hebrew Psalm 23 is CPDV Psalm 22. Always check the text before you use a reference.
- If a queue idea can't be drawn simply and clearly with the props available (or a small new prop), skip to the next one. Note the skip in `queue.json`.

## 2. Write the episode
Copy the closest existing episode to `episodes/epNNN_<slug>.py` and set:
- `kicker`: "BOOK CH  •  TITLE" in capitals.
- `headline`: the hook. Two short lines joined with `\n`, under about 34 characters per line. It should be a contrast or a challenge, such as "Three people saw him.\nOnly one stopped."
- `captions`: three entries of `(cpdv(book, ch, vs, "exact excerpt"), "Book ch:vs", time_in_seconds)`.
  `cpdv()` checks the wording against the CPDV and fails on anything that isn't verbatim. Use `…` to trim text.
  Each excerpt should be at most about 20 words. Make each caption appear at the moment its panel's outcome happens.
- `cta`: rotate through `queue.json` → `apps_cta_rotation`, picking by day number modulo its length.
- `OUTPUT_NAME = "dayNNN_<slug>_<book><chapter>"`.
- `draw_panel(cr, i, t, y0, gy)`: put the choreography here.
  Helpers: `track()` for walking positions, `keyed()` for pose keyframes, `body()` to blend in a walk cycle, `draw_figure()` and `draw_rotated()` for people, and the props in `props.py` (house/door/light, coin, lamp, lampstand, basket, darkness, water, boat, wind, sun, bird, sprout, wheat).
  Add new props to `props.py`, never inline, so later days can reuse them.
- Rules: no faces and no text inside the art. Jesus is a robed silhouette only. Keep everything wordless except the captions.
  Hold the final state from about 15 to 17.2 seconds; the engine fades back to frame 0 so the video loops.
  For dark scenes, set `caption_bg = True`. For water scenes, set `ground = False`.

## 3. Check before rendering (required)
```
python3 make.py episodes/epNNN_x.py --preview 2 5 8 11 14 16.5
```
Open every PNG and look at it. Check that:
- each panel's outcome is clear without sound;
- no limbs are broken and no figure floats;
- captions don't collide with the art or the headline;
- nothing important is clipped at a panel edge.
Fix the problem and preview again.

## 4. Render
```
python3 make.py episodes/epNNN_x.py     # -> out/<name>.mp4 and prev/<name>_sheet.png
```
Open the contact sheet and confirm the whole story plays.

## 5. Deliver and record
- Add a block to `POSTS.md` with a hook caption, a pinned comment that matches the CTA app, and 5 to 7 hashtags.
- Move the two items from `queue` to `done` as `{day, title, refs}`. Keep the queue at 20 or more items by adding fresh triad stories (parables, miracles, Psalms, Proverbs, epistles, saints' favourite verses).
- Commit to the `daily-verse-parables` branch, never to `main`, and push. Don't commit the mp4 files.
- Send the two mp4s to the user, with their post captions, in a short message.
