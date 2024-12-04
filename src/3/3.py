import re


def get_input():
    with open("/Users/olivia/projects/advent/src/3/input.txt", "r") as file:
        return file.read()


def main():
    corrupted = get_input()
    res = 0
    do = True

    muls = r"mul\([0-9]+,[0-9]+\)"
    dos = r"do\(\)"
    donts = r"don't\(\)"
    pattern = re.compile(r"|".join([muls, dos, donts]))
    matches = pattern.findall(corrupted)

    for s in matches:
        match s:
            case s if "mul" in s:
                if do:
                    numbers = re.findall(r"\d+", s)
                    res += int(numbers[0]) * int(numbers[1])
            case "don't()":
                do = False
            case "do()":
                do = True

    print(res)


main()
