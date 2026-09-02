"""
py_constellation_mapper.py

Draw a size * size grid of "." with a "*" at every star coordinate.
Coordinates outside the grid are ignored, duplicates change nothing.
"""


def constellation_mapper(stars: list[tuple[int, int]],
                         size: int) -> list[str]:
    grid = []
    for _ in range(size):
        grid.append(["."] * size)

    for row, col in stars:
        if 0 <= row < size and 0 <= col < size:
            grid[row][col] = "*"

    lines = []
    for cells in grid:
        lines.append("".join(cells))
    return lines


if __name__ == "__main__":
    tests = [
        (([(0, 0), (1, 1), (2, 2)], 3), ["*..", ".*.", "..*"]),
        (([(0, 0), (0, 1), (0, 2), (1, 1), (2, 2)], 3),
         ["***", ".*.", "..*"]),
        (([(0, 0), (5, 5), (2, 2)], 3), ["*..", "...", "..*"]),
        (([(0, 0), (5, 5)], 2), ["*.", ".."]),
        (([], 3), ["...", "...", "..."]),
        (([(1, 1), (1, 1), (1, 1)], 2), ["..", ".*"]),
        (([(-1, 0), (0, -1)], 2), ["..", ".."]),
        (([(0, 2), (2, 0)], 3), ["..*", "...", "*.."]),
        (([(0, 0)], 1), ["*"]),
    ]

    for (stars, size), expected in tests:
        result = constellation_mapper(stars, size)
        status = "OK" if result == expected else "FAIL"
        print(f"[{status}] constellation_mapper({stars!r}, {size}) "
              f"-> {result}")
