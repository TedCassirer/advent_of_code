def getInput(loop=False):
    with open('2019/input/day_2') as input:
        return list(map(int, next(input).split(',')))

OP_CODES = {
    1 : int.__add__,
    2 : int.__mul__
}

def do_the_thing(numbers):
    for i in range(0, len(numbers), 4):
        code = numbers[i]
        if code == 99:
            return numbers
        else:
            n1, n2, p = numbers[i+1: i+4]
            numbers[p] = OP_CODES[code](numbers[n1], numbers[n2])
    raise Exception()

def part1():
    numbers = getInput()
    numbers[1] = 12
    numbers[2] = 2
    return do_the_thing(numbers)[0]

def part2():
    target = 19690720
    numbers = getInput()
    for n1 in range(0, 100):
        for n2 in range(0, 100):
            numbers_copy = numbers[:]
            numbers_copy[1], numbers_copy[2] = n1, n2
            result = do_the_thing(numbers_copy)
            if result[0] == target:
                return 100*n1 + n2

if __name__ == '__main__':
    print('Part 1:', part1())
    print('Part 2:', part2())