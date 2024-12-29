## advent of code 2024
## https://adventofcode.com/2024
## day 05


class List(list[int]):
    def __init__(self, *args):
        self.rules, _ = parse_input()
        super().__init__(args)

    def move(self, i: int, to: int):
        additional_moves = len(self._check_rule(i))
        self.insert(to, self.pop(i))
        for add_move in range(additional_moves):
            self.move(add_move, to)

    def _check_rule(self, i: int) -> list[int]:
        return self.rules[i]


def parse_input() -> tuple[dict[int, list[int]], list[List]]:
    with open("input.txt") as f:
        text = f.read()

    rules_str, pages_str = text.split("\n\n")
    pages = [List([int(page) for page in line.split(",")]) for line in pages_str.splitlines()]

    # parse rules
    rules: dict[int, list[int]] = {}
    for line in rules_str.splitlines():
        b, a = line.split("|")
        rules[int(a)] = rules.get(int(a), []) + [int(b)]

    return rules, pages


def part1():
    rules, examples = parse_input()
    for pages in examples:
        for i in range(len(pages)):
            if any(page in pages._check_rule(i) for page in pages[i:]):
                pages.move(i, i - 1)
        print(pages)


def part2(data):
    pass
