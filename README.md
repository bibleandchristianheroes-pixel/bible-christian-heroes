# Daily Verse Parables

Wordless three-panel silhouette videos. Each panel shows one CPDV verse, and the video is an 18-second loop at 1080x1920.
They promote Scroll the Catholic Bible, Ave – Catholic Prayer Lock and Ave Missal.

- `./setup.sh` sets things up, then `python3 make.py episodes/ep001_sower.py` renders `out/day001_sower_matthew13.mp4`
- `RUNBOOK.md` has the step-by-step instructions the daily run follows (two videos per day)
- `queue.json` lists the upcoming stories plus the record of what's done; `POSTS.md` has the social captions
- The music is original, synthesised in `engine.make_music`. The CPDV text is public domain and fetched by `setup.sh`.
