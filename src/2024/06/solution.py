## advent of code 2024
## https://adventofcode.com/2024
## day 06

from itertools import cycle
from os.path import dirname
from time import sleep

from colorama import Fore, Style

guard_chars = [">", "<", "^", "v"]
directions = cycle(["up", "right", "down", "left"])
dir_map = {
    ">": "right",
    "<": "left",
    "^": "up",
    "v": "down",
}
guard_map = {
    "right": ">",
    "left": "<",
    "up": "^",
    "down": "v",
}


def turn_right(direction: str) -> str:
    match direction:
        case "right":
            return "down"
        case "down":
            return "left"
        case "left":
            return "up"
        case "up":
            return "right"
        case _:
            raise ValueError(f"Invalid direction: {direction}")


def next_pos(x: int, y: int, direction: str) -> tuple[int, int]:
    match direction:
        case "right":
            return x + 1, y
        case "left":
            return x - 1, y
        case "up":
            return x, y - 1
        case "down":
            return x, y + 1
        case _:
            raise ValueError(f"Invalid direction: {direction}")


def pos_in_bounds(x: int, y: int, data: list[list[str]]) -> bool:
    return 0 <= x < len(data) and 0 <= y < len(data[x])


def visualize_step(x: int, y: int, direction: str, data: list[list[str]], seen: set[tuple[int, int]]):
    for i, row in enumerate(data):
        for j, char in enumerate(row):
            if i == y and j == x:
                print(Fore.RED + guard_map[direction] + Style.RESET_ALL, end="")
            elif (j, i) in seen:
                print("X", end="")
            else:
                print(char, end="")
        print()
    print()
    print(f"Count: {len(seen)}")
    sleep(0.2)


def step(x: int, y: int, direction: str, data: list[list[str]]) -> list[tuple[int, int]]:
    seen = []
    while True:
        seen.append((x, y))
        # visualize_step(x, y, direction, data, seen)
        new_x, new_y = next_pos(x, y, direction)
        if not pos_in_bounds(new_x, new_y, data):
            return seen
        if data[new_y][new_x] == "#":
            direction = turn_right(direction)
        else:
            x, y = new_x, new_y


def get_start_pos(data: list[list[str]]) -> tuple[int, int]:
    y = next(y for y in range(0, len(data)) if any(c in guard_chars for c in data[y]))
    x = next(x for x in range(0, len(data[y])) if data[y][x] in guard_chars)
    return x, y


def parse_input(lst: list[str] = open(f"{dirname(__file__)}/input.txt").readlines()) -> list[list[str]]:
    return [list(l.strip()) for l in lst]


def part1(data: list[list[str]]):
    x, y = get_start_pos(data)
    direction = dir_map[data[y][x]]
    print(len(set(step(x, y, direction, data))))


def part2(data):
    x, y = get_start_pos(data)
    direction = dir_map[data[y][x]]
    seen = step(x, y, direction, data)
    print(seen)


# def find_loops(seen: list[tuple[int, int]]) -> int:
#     for i in range(len(seen)):
#         while True:
#             if seen[i]


if __name__ == "__main__":
    lines = open(f"{dirname(__file__)}/input.txt").readlines()
    part1(parse_input(lines))
