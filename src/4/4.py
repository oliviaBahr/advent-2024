import os
import time
from typing import Iterator

import numpy as np
import pytest
from colorama import Fore
from more_itertools import sliding_window
from numpy.typing import NDArray


class Grid:
    def __init__(self, arr: list[str]):
        self.arr = arr

    def __getitem__(self, key: tuple[int, int], default: str = "") -> str:
        try:
            return self.arr[key[0]][key[1]]
        except IndexError:
            return default

    def __len__(self) -> int:
        return len(self.arr)

    def __iter__(self):
        return self.arr

    @property
    def n_rows(self) -> int:
        return len(self.arr)

    @property
    def n_cols(self) -> int:
        return len(self.arr[0])


def get_input_text() -> list[str]:
    with open("src/4/input.txt", "r") as f:
        return f.read().splitlines()


def count_xmas(arr: list[str]) -> int:
    n_rows = len(arr)
    n_cols = len(arr[0]) if n_rows > 0 else 0
    total = 0

    def diag_coords(n_rows: int, n_cols: int) -> list[list[tuple[int, int]]]:
        result = []

        # Down right
        for d in range(n_rows + n_cols - 1):
            diagonal = []
            for x in range(max(0, d - n_cols + 1), min(d + 1, n_rows)):
                y = d - x
                diagonal.append((x, y))
            result.append(diagonal)

        # Down left
        for d in range(n_rows + n_cols - 1):
            diagonal = []
            for x in range(max(0, d - n_cols + 1), min(d + 1, n_rows)):
                y = n_cols - 1 - (d - x)
                if 0 <= y < n_cols:
                    diagonal.append((x, y))
            result.append(diagonal)

        return [r for r in result if len(r) >= 4]

    def hor_coords(n_rows: int, n_cols: int) -> list[list[tuple[int, int]]]:
        result = []
        for y in range(n_cols):
            row = []
            for x in range(n_rows):
                row.append((x, y))
            result.append(row)
        return result

    def ver_coords(n_rows: int, n_cols: int) -> list[list[tuple[int, int]]]:
        result = []
        for x in range(n_rows):
            row = []
            for y in range(n_cols):
                row.append((x, y))
            result.append(row)
        return result

    def _count_xmas(coords: list[list[tuple[int, int]]]) -> int:
        total = 0
        for line in coords:
            for word_coords in sliding_window(line, 4):
                word = "".join(arr[x][y] for x, y in word_coords)
                if word in ["XMAS", "SAMX"]:
                    total += 1
        return total

    total += _count_xmas(hor_coords(n_rows, n_cols))
    total += _count_xmas(ver_coords(n_rows, n_cols))
    total += _count_xmas(diag_coords(n_rows, n_cols))
    return total


def count_x_mas(arr: list[str], visualize: bool = False) -> int:
    total = 0
    grid = Grid(arr)
    v = Vis(grid, silent=not visualize)
    up = lambda x, y: (x - 1, y)
    down = lambda x, y: (x + 1, y)
    left = lambda x, y: (x, y - 1)
    right = lambda x, y: (x, y + 1)
    for i in range(grid.n_rows):
        for j in range(grid.n_cols):
            if grid[i, j] == "A":
                v.update([(i, j)], total=total)

                lmas_coords = [down(*left(i, j)), (i, j), up(*right(i, j))]
                left_mas = "".join(grid[c] for c in lmas_coords)
                r_mas_valid = left_mas in ["MAS", "SAM"]
                v.update(lmas_coords, correct=r_mas_valid, total=total)

                rmas_coords = [down(*right(i, j)), (i, j), up(*left(i, j))]
                right_mas = "".join(grid[c] for c in rmas_coords)
                l_mas_valid = right_mas in ["MAS", "SAM"]
                v.update(rmas_coords, correct=l_mas_valid, total=total)

                if r_mas_valid and l_mas_valid:
                    total += 1

                v.update(lmas_coords + rmas_coords, correct=r_mas_valid and l_mas_valid, total=total)
    return total


class Vis:
    def __init__(self, grid: Grid, silent: bool = False):
        self.grid = grid
        self.silent = silent
        self.update([])

    def update(self, highlight: list[tuple[int, int]], correct: bool | None = None, total: int = 0) -> None:
        if self.silent:
            return
        os.system("clear")
        highlight_color = Fore.GREEN if correct else Fore.RED if correct is False else Fore.LIGHTBLACK_EX
        default_color = Fore.RESET

        print("\n\n")
        for i in range(self.grid.n_rows):
            for j in range(self.grid.n_cols):
                if (i, j) in highlight:
                    print(highlight_color + self.grid[i, j], end="")
                else:
                    print(default_color + self.grid[i, j], end="")
            print()
        print(f"Total: {total}")

        time.sleep(0.5)


test_cases = [
    ("XMAS", 1, "horizontal"),
    ("SAMX", 1, "horizontal reversed"),
    ("X...\n.M..\n..A.\n...S", 1, "vertical"),
    ("S...\n.A..\n..M.\n...X", 1, "vertical reversed"),
    ("X...\n.M..\n..A.\n...S", 1, "diagonal"),
    ("S...\n.A..\n..M.\n...X", 1, "diagonal reversed"),
]


@pytest.mark.parametrize("text_input,expected,description", test_cases)
def test_xmas_patterns(text_input, expected, description):
    result = count_xmas(text_input)
    assert result == expected, f"Failed for {description} text_input"


def main():
    inp = get_input_text()
    print(count_xmas(inp))
    print(count_x_mas(inp))


def test_xmas_patterns_visual():
    test_str = """.M.S......
..A..MSMS.
.M.S.MAA..
..A.ASMSM.
.M.S.M....
..........
S.S.S.S.S.
.A.A.A.A..
M.M.M.M.M.
.........."""
    expected = 9
    result = count_x_mas(test_str.splitlines(), True)
    if result == expected:
        print(Fore.GREEN + "Correct")
    else:
        print(Fore.RED + f"Expected {expected}")


if __name__ == "__main__":
    main()
    # test_xmas_patterns_visual()
