"""
py_palindrome_partitioner.py

Fewest cuts that split a string into palindromes only.

Two passes of dynamic programming: first mark every palindromic substring,
then walk left to right keeping the best answer for each prefix.
"""


def palindrome_partitioner(s: str) -> int:
    n = len(s)
    if n <= 1:
        return 0

    # is_pal[i][j] is True when s[i:j + 1] reads the same both ways
    is_pal = []
    for _ in range(n):
        is_pal.append([False] * n)

    # go right to left so the shorter inner substring is already known
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            if s[i] == s[j] and (j - i < 2 or is_pal[i + 1][j - 1]):
                is_pal[i][j] = True

    cuts = [0] * n                   # cuts[j] = best answer for s[:j + 1]
    for j in range(n):
        if is_pal[0][j]:
            continue                 # whole prefix is a palindrome already
        best = j                     # worst case: cut before every character
        for i in range(1, j + 1):
            if is_pal[i][j] and cuts[i - 1] + 1 < best:
                best = cuts[i - 1] + 1
        cuts[j] = best

    return cuts[n - 1]


if __name__ == "__main__":
    tests = [
        ("aab", 1),
        ("aba", 0),
        ("abc", 2),
        ("", 0),
        ("a", 0),
        ("aa", 0),
        ("ab", 1),
        ("racecar", 0),
        ("abccba", 0),
        ("noonabbad", 2),
        ("abcde", 4),
    ]

    for value, expected in tests:
        result = palindrome_partitioner(value)
        status = "OK" if result == expected else "FAIL"
        print(f"[{status}] palindrome_partitioner({value!r}) -> {result}")
