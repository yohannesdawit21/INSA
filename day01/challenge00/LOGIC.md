# Challenge 00 — Code Logic (Josephus Circle)

This document explains **how the code works**, end to end: the algorithm, the
Django backend that serves it, and the JavaScript that animates it.

> High-level overview lives in [README.md](README.md).
> The plain-English story of the puzzle is in [challenge-oo.md](challenge-oo.md).

---

## 1. The algorithm — `visualizer/josephus.py`

The whole challenge is one function: `josephus_sequence(n, k)`.

```python
def josephus_sequence(n, k):
    people = list(range(1, n + 1))   # [1, 2, ..., n]
    index = 0
    order = []

    while len(people) > 1:
        index = (index + k - 1) % len(people)   # count k-1 steps, wrap around
        order.append(people.pop(index))         # remove the counted person
        if index >= len(people):
            index = 0

    return {"order": order, "survivor": people[0]}
```

### The core idea

People are a **list**, and `index` is where we are standing in that list.

- **`(index + k - 1) % len(people)`** — this single line replaces the original
  script's inner `for` loop. We move `k - 1` steps because the person we *land
  on* is the one eliminated (counting includes the current position). The `%`
  (modulo) makes the count **wrap around** the circle — stepping past the end
  brings you back to the start.
- **`people.pop(index)`** removes that person and returns them, so we append
  them to `order`.
- After a `pop`, every later element shifts down by one — which means `index`
  **already points at the next person**, so the next count continues naturally.
  The `if index >= len(people)` guard only matters when we removed the very last
  element, resetting us to the front.

### What changed from the original `challenge-00.py`

The original only returned the survivor. Here we also record `order` — the full
list of who is eliminated and in what sequence. **That list is what the frontend
replays as an animation.** Same logic, richer output.

```
josephus_sequence(5, 2) -> {"order": [2, 4, 1, 5], "survivor": 3}
```

---

## 2. The backend — `visualizer/views.py`

Two views, wired up in `visualizer/urls.py`:

| URL | View | Returns |
|-----|------|---------|
| `/` | `index` | the HTML page |
| `/api/solve?n=&k=` | `solve` | JSON: `{n, k, order, survivor}` |

`solve` is a thin, defensive wrapper around the algorithm:

```python
n = int(request.GET.get("n", ""))      # read query params
k = int(request.GET.get("k", ""))
# ... validate ...
result = josephus_sequence(n, k)
return JsonResponse({"n": n, "k": k, **result})
```

Validation rules (each returns HTTP 400 with an `error` message):
- `n` and `k` must be whole numbers,
- both must be `>= 1`,
- `n` must be `<= MAX_PEOPLE` (200) so the animation stays readable.

The backend holds **no state** — every request recomputes from scratch, so there
is no database (`DATABASES = {}` in settings).

---

## 3. The animation — `templates/visualizer/index.html`

All the motion is client-side JavaScript. The page never reloads; it just calls
the API and animates the result. The script is wrapped in `{% verbatim %}` so
Django leaves the JS braces alone.

### State

```js
let nodes = [];     // the person <div>s, nodes[0] == person 1
let order = [];     // elimination order from the API
let stepIdx = 0;    // how many eliminations have played so far
let playing = false;
```

### Placing people on a circle — `layout()`

People are positioned with trigonometry around a ring:

```js
const ang = (-90 + (360 * i) / total) * (Math.PI / 180);
el.style.left = (cx + R * Math.cos(ang)) + "px";
el.style.top  = (cy + R * Math.sin(ang)) + "px";
```

For person `i` of `total`, the angle is evenly spaced around 360°, starting at
the top (`-90°`). `cos`/`sin` turn that angle into x/y on a circle of radius `R`.
It re-runs on window resize so the layout stays responsive.

### The flow

1. **`build()`** — reads `n`/`k`, calls `GET /api/solve`, stores `order` and
   `survivor`, then creates one `.person` div per number and lays them out.
2. **`step()`** — plays **one** elimination:
   - point the rotating pointer at the victim (`pointAt`),
   - flash them red (CSS `pop` animation), log it, then fade them out
     (`.eliminated`),
   - increment `stepIdx`. When `stepIdx` reaches the end, the survivor gets the
     golden glow (`.survivor`).
3. **`play()`** — calls `step()` on a timer; the gap is `720 / speedFactor()` ms,
   so the speed slider directly scales the delay. Clicking again pauses.
4. **`step` button / `reset`** — step plays one frame manually; reset rebuilds.

### Where the CSS does the work

The JS only **adds/removes classes**; the visual motion is CSS transitions and
`@keyframes`:
- `.person` has a `transition`, so any change (scale, color, opacity) animates.
- `.person.flash` runs the red `pop` keyframe, `.survivor` runs the looping
  `glow` keyframe, and `:hover` scales a dot up and snaps the pointer to it.

---

## 4. Putting it together

```
Browser ── GET /api/solve?n=7&k=3 ──▶ Django (views.solve)
                                         │ josephus_sequence(7, 3)
Browser ◀── {order:[3,6,2,7,5,1],     ──┘
             survivor:4} ── JSON
   │
   └─ JS replays `order` one dot at a time, then crowns `survivor`.
```

The Python decides **what happens**; the JavaScript decides **how it looks**.
