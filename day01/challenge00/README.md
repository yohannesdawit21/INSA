# Josephus Circle — Interactive Django Visualizer

An animated web app that brings the **Josephus problem** (see
[challenge-oo.md](challenge-oo.md)) to life: `n` people stand in a circle and
every `k`-th person is eliminated until one survivor remains. Press play and
watch the circle decide, with a rotating counter, fading eliminations, and a
glowing survivor.

## Features

- 🎯 People arranged on an animated ring, eliminated one-by-one
- 🎞️ Play / Pause / Step / Reset controls + adjustable speed
- ✨ Motion & hover effects, glassmorphism UI, animated gradient background
- 📜 Live elimination log + alive/eliminated/survivor stats
- 🔌 Tiny JSON API (`/api/solve?n=&k=`) powered by the original algorithm

## Run it

```bash
# from this folder (INSA/)
python3 manage.py runserver
```

Then open **http://127.0.0.1:8000/** in your browser.

> Requires Django (`pip install Django`). Already installed in this env.

## Project layout

```
INSA/
├── manage.py                     # Django entry point
├── josephus_site/                # project config (settings, urls, wsgi)
└── visualizer/                   # the app
    ├── josephus.py               # the algorithm (returns full elimination order)
    ├── views.py                  # page view + JSON API
    ├── urls.py
    └── templates/visualizer/
        └── index.html            # the entire animated UI (HTML/CSS/JS)
```

## How it fits together

1. The browser loads `index.html` and calls `GET /api/solve?n=7&k=3`.
2. `views.solve` validates the input and runs `josephus_sequence(n, k)`.
3. The API returns the elimination `order` and the `survivor`.
4. The frontend replays that order as an animation around the circle.

The core algorithm is the same logic as the original `challenge-00.py`, only
extended to record *every* elimination instead of just the final survivor.
