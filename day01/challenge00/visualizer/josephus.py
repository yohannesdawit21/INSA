"""
The Josephus problem — same idea as the original challenge-00.py script,
but instead of only returning the survivor it records the FULL order in
which people are eliminated. The frontend replays that order as an
animation.

n people stand in a circle numbered 1..n. Counting starts at person 1;
every k-th person is removed until a single survivor remains.
"""


def josephus_sequence(n, k):
    """Return the elimination order and the final survivor.

    Args:
        n: number of people in the circle (>= 1).
        k: count interval — every k-th person is eliminated (>= 1).

    Returns:
        dict with:
            "order"    -> list of person numbers in the order eliminated
            "survivor" -> the last remaining person
    """
    people = list(range(1, n + 1))
    index = 0
    order = []

    while len(people) > 1:
        # Move k-1 steps forward, wrapping around the circle.
        index = (index + k - 1) % len(people)
        order.append(people.pop(index))
        # After popping, `index` already points at the next person.
        if index >= len(people):
            index = 0

    return {"order": order, "survivor": people[0]}
