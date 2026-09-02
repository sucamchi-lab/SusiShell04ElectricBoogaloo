"""
py_merge_sorted_list.py

Merge already-sorted sublists into one ascending list, keeping duplicates.
Done by hand: repeatedly take the smallest value still at the front of any
sublist.
"""

FORBIDDEN = ["sorted", "sort", "heapq"]


def merge_sorted_list(lists: list[list[int]]) -> list[int]:
    positions = [0] * len(lists)     # how far we have read into each sublist
    merged: list[int] = []

    while True:
        best = None
        smallest = None
        for i, sublist in enumerate(lists):
            if positions[i] == len(sublist):
                continue                  # this sublist is used up
            value = sublist[positions[i]]
            if smallest is None or value < smallest:
                best = i
                smallest = value

        if best is None:
            return merged             # every sublist is used up

        merged.append(lists[best][positions[best]])
        positions[best] += 1


if __name__ == "__main__":
    tests: list[tuple[list[list[int]], list[int]]] = [
        ([[1, 4, 5], [1, 3, 4], [2, 6]], [1, 1, 2, 3, 4, 4, 5, 6]),
        ([[1, 2, 3], [], [0, 4]], [0, 1, 2, 3, 4]),
        ([], []),
        ([[], []], []),
        ([[5]], [5]),
        ([[2, 2, 2], [2, 2]], [2, 2, 2, 2, 2]),
        ([[-5, -1], [-3, 0]], [-5, -3, -1, 0]),
        ([[10, 20, 30]], [10, 20, 30]),
        ([[1], [2], [3], [0]], [0, 1, 2, 3]),
    ]

    for lists, expected in tests:
        result = merge_sorted_list(lists)
        status = "OK" if result == expected else "FAIL"
        print(f"[{status}] merge_sorted_list({lists!r}) -> {result}")
