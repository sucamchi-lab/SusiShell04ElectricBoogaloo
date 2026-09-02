"""
py_array_rotation_detector.py

Check whether arr2 is a circular rotation of arr1, in either direction.
Lists of different lengths are never rotations of each other.
"""

FORBIDDEN = ["rotate"]


def array_rotation_detector(arr1: list, arr2: list) -> bool:
    if len(arr1) != len(arr2):
        return False

    for offset in range(len(arr1)):
        if arr1[offset:] + arr1[:offset] == arr2:
            return True

    # no offset matched, which for two empty lists means the loop never ran
    return len(arr1) == 0


if __name__ == "__main__":
    tests = [
        (([1, 2, 3, 4, 5], [4, 5, 1, 2, 3]), True),
        (([1, 2, 3, 4, 5], [5, 1, 2, 3, 4]), True),
        (([1, 2, 3], [3, 2, 1]), False),
        (([1, 2], [1, 2, 3]), False),
        (([], []), True),
        (([1, 2, 3], [1, 2, 3]), True),
        (([1, 2, 3], []), False),
        (([1, 1, 2], [1, 2, 1]), True),
        (([1, 2, 3], [1, 3, 2]), False),
    ]

    for (arr1, arr2), expected in tests:
        result = array_rotation_detector(arr1, arr2)
        status = "OK" if result == expected else "FAIL"
        print(f"[{status}] array_rotation_detector({arr1!r}, {arr2!r}) "
              f"-> {result}")
