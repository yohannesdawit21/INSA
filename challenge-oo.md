# Challenge 00 — The Josephus Problem

A small Python program ([challenge-00.py](challenge-00.py)) that solves the classic
**Josephus problem**: people stand in a circle and are eliminated one by one at a
fixed counting interval until a single survivor remains.

---

## The story behind it

Imagine `n` people standing in a circle, numbered `1` to `n`.

Starting from the first person, you count `k` people around the circle. The
`k`-th person is eliminated. You then start counting again from the *next*
person, and repeat. The circle keeps shrinking until only **one person is left** —
that person is the survivor.

The program asks for `n` and `k`, runs the elimination, and prints who survives.

---

## How to run it

```bash
python3 challenge-00.py
```

Example session:

```
Enter number of people: 5
Enter elimination index: 2
Person 2 is eliminated
Person 4 is eliminated
Person 1 is eliminated
Person 5 is eliminated
Last surviving person is: 3
```

- **Number of people** → `n`, how many people start in the circle.
- **Elimination index** → `k`, every `k`-th person is removed.

---

## How the code works

The logic lives in the `josephus(n, k)` function.

### 1. Build the circle

```python
people = []
for i in range(1, n + 1):
    people.append(i)
```

A list `people = [1, 2, 3, ..., n]` represents everyone standing in the circle.

### 2. Count around and eliminate

```python
index = 0
while len(people) > 1:
    for j in range(k - 1):
        index = index + 1
        if index >= len(people):
            index = 0          # wrap around to the start
    eliminated = people.pop(index)
    print("Person", eliminated, "is eliminated")
    if index >= len(people):
        index = 0
```

- `index` tracks the current position in the list.
- The inner loop steps forward `k - 1` times. (We only move `k - 1` steps because
  the person we land *on* is the one eliminated — counting starts at the current
  position.)
- `if index >= len(people): index = 0` makes the counting **wrap around** the
  circle, so the end connects back to the beginning.
- `people.pop(index)` removes the counted person from the circle.
- After removing someone, if `index` now points past the end of the list, it is
  reset to `0` so the next count continues correctly.

### 3. Return the survivor

```python
return people[0]
```

Once only one person remains, the loop stops and that last person is returned.

---

## Key idea

The trick is that after each removal, the **next count automatically starts from
the person right after the eliminated one** — because `pop(index)` shifts every
later element down by one, so `index` already points at the next person without
extra work.

---

## Inputs at a glance

| Input | Meaning | Example |
|-------|---------|---------|
| `n`   | Number of people in the circle | `5` |
| `k`   | Count interval (every k-th person is out) | `2` |

## Output

The program prints each elimination in order and finally announces the last
surviving person.
