"""
py_list_intersection_finder.py

Return the values present in every input list, sorted and without
duplicates. If there are no lists, or any list is empty, the result is [].
"""


def list_intersection_finder(lists: list[list[int]]) -> list[int]:
    if not lists:
        return []

    common = set(lists[0])
    for sublist in lists[1:]:
        common = common & set(sublist)

    return sorted(common)


if __name__ == "__main__":
    tests = [
        ([[1, 2, 3], [2, 3, 4], [2, 3, 5]], [2, 3]),
        ([[1, 2, 3, 4], [2, 4, 6, 8], [4, 8, 12]], [4]),
        ([[1, 1, 2, 3], [1, 2, 2, 3], [1, 2, 3, 3]], [1, 2, 3]),
        ([[1, 2, 3], [4, 5, 6]], []),
        ([], []),
        ([[1, 2, 3], []], []),
        ([[5]], [5]),
        ([[3, 1, 2], [2, 1, 3]], [1, 2, 3]),
        ([[-2, 0, 7], [-2, 7, 9], [-2, 7]], [-2, 7]),
    ]

    for lists, expected in tests:
        result = list_intersection_finder(lists)
        status = "OK" if result == expected else "FAIL"
        print(f"[{status}] list_intersection_finder({lists!r}) -> {result}")
