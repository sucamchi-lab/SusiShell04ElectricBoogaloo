"""
py_sliding_window_maximium.py

Slide a window of size k across the list and collect the biggest value in
each position. Empty list or k <= 0 gives [].
"""


def sliding_window_maximium(nums: list[int], k: int) -> list[int]:
    if not nums or k <= 0:
        return []

    maximums = []
    for start in range(len(nums) - k + 1):
        maximums.append(max(nums[start:start + k]))
    return maximums


if __name__ == "__main__":
    tests = [
        (([1, 3, -1, -3, 5, 3, 6, 7], 3), [3, 3, 5, 5, 6, 7]),
        (([4, 2, 12, 11, -5], 2), [4, 12, 12, 11]),
        (([], 3), []),
        (([1, 2, 3], 1), [1, 2, 3]),
        (([1, 2, 3], 3), [3]),
        (([7, 7, 7], 2), [7, 7]),
        (([-1, -5, -3], 2), [-1, -3]),
        (([5, 4, 3, 2, 1], 2), [5, 4, 3, 2]),
        (([1, 2], 0), []),
    ]

    for (nums, k), expected in tests:
        result = sliding_window_maximium(nums, k)
        status = "OK" if result == expected else "FAIL"
        print(f"[{status}] sliding_window_maximium({nums!r}, {k}) "
              f"-> {result}")
