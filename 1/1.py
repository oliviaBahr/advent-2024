def get_lists() -> tuple[list[int], list[int]]:
    with open("./input.txt", "r") as file:
        lines = file.readlines()

    l1, l2 = zip(*[tuple(int(i) for i in line.split()) for line in lines])
    return sorted(l1), sorted(l2)


def part_1() -> int:
    l1, l2 = get_lists()
    zipped = zip(l1, l2)
    return sum(abs(a - b) for a, b in zipped)


def part_2() -> int:
    l1, l2 = get_lists()
    return sum(Litm * l2.count(Litm) for Litm in l1)


def main():
    print(part_1())
    print(part_2())


if __name__ == "__main__":
    main()
