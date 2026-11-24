# fieldareameasure.com (EN/ES/FR/DE/PT)

Website for **Field Area Measure** (iOS id6740893569, Android com.asilarslan.fieldarea). GitHub Pages, repo root, `main` = live.
fieldareameasure.com (international) and arazi.app (Turkish) share the same `build.py`, CSS and JS; only `content/` differs. Keep them in sync.

```bash
python3 build.py         # regenerate pages
python3 build.py --ping  # after a deploy: submit URLs to IndexNow
NODE_PATH=<playwright> PW_CHANNEL=chrome node tools/og.js   # share images from content/og.json
```

- `content/site.py`: home page copy, languages, sister site. `content/pages.py`: converter, extra tools, guides.
- App screens in `assets/img/screen-<lang>-<key>.webp` are real captures of the Android app (debug build, `--ez demo true`).
- Don't claim CSV export, offline mode or GPS walk tracking; the app doesn't have them. Site Analysis is Android-only for now.
