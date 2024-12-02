def getReports() -> list[list[int]]:
    with open("/Users/olivia/projects/advent/src/2/input.txt") as f:
        lines = f.readlines()
        print("-" in f.read())

    return [[int(n) for n in line.split()] for line in lines]


def main():
    reps = getReports()
    listsWithNeg = [rep for rep in reps if any(n < 0 for n in rep)]

    print(listsWithNeg)


main()
