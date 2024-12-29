import os
from itertools import permutations
from math import factorial
from multiprocessing import Pool

from p_tqdm import p_uimap
from tqdm import tqdm

rules = {}


def parse_input() -> tuple[dict[int, list[int]], list[list[int]]]:
    with open(f"{os.getcwd()}/src/2024/05/input.txt") as f:
        text = f.read()

    rules_str, pages_str = text.split("\n\n")
    pages = [[int(page) for page in line.split(",")] for line in pages_str.splitlines()]

    # parse rules
    rules: dict[int, list[int]] = {}
    for line in rules_str.splitlines():
        b, a = line.split("|")
        rules[int(a)] = rules.get(int(a), []) + [int(b)]

    return rules, pages


# dict is {after: before}


def isValid(pages: list[int]) -> bool:
    global rules
    pos_lookup = {num: i for i, num in enumerate(pages)}

    for after_num, before_nums in rules.items():
        after_pos = pos_lookup.get(after_num, -1)
        if after_pos == -1:  # if after_num isn't in the sequence, skip
            continue

        for before_num in before_nums:
            if before_num in pos_lookup and pos_lookup[before_num] >= after_pos:
                return False
    return True


def check_permutation(perm) -> tuple[bool, tuple]:
    """Helper function to check a single permutation"""
    if isValid(list(perm)):
        return True, perm
    return False, perm


def part11():
    rules, examples = parse_input()
    result = []
    print("Processing examples")

    for pages in tqdm(examples):
        # Process permutations in parallel
        for valid, perm in p_uimap(check_permutation, permutations(pages), total=factorial(len(pages)), leave=False):
            if valid:
                result.append(perm)
                break  # We only need the first valid permutation

    # add middle numbers
    total = 0
    for example in result:
        total += example[len(example) // 2]

    print(total)


def part1():
    rules, examples = parse_input()
    result = []
    print("Processing examples")

    # Create a process pool
    with Pool() as pool:
        print("Processing permutations")
        for pages in tqdm(examples):
            # Prepare arguments for each permutation
            perms = permutations(pages)
            args = [(rules, perm) for perm in perms]

            # Process permutations in parallel
            for valid, perm in pool.imap_unordered(check_permutation, args):
                if valid:
                    result.append(perm)
                    break  # We only need the first valid permutation

    # add middle numbers
    total = 0
    for example in result:
        total += example[len(example) // 2]

    print(total)


if __name__ == "__main__":
    from multiprocessing import freeze_support

    freeze_support()
    part11()
