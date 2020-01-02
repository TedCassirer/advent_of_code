from IntCodeComputer import IntCodeComputerVM, manual_input, read_program

def ascii_input():
    while True:
        yield from (ord(i) for i in input('Input: '))
        yield ord('\n')

def part1():
    program = read_program('2019/input/day_17')
    vm = IntCodeComputerVM(program)
    s = []
    row = []
    for r in vm.run():
        char = chr(r)
        if char == '\n':
            s.append(row)
            row = []
        else:
            row.append(char)

    scaffold_coords = set()
    for y, row in enumerate(s):
        for x, char in enumerate(row):
            if char == '#':
                scaffold_coords.add((y, x))

    intersections = set()
    for y, x in scaffold_coords:
        if (y-1, x) in scaffold_coords \
                and (y+1, x) in scaffold_coords \
                and (y, x-1) in scaffold_coords \
                and (y, x+1) in scaffold_coords:
            s[y][x] = 'O'
            intersections.add((y, x))

    for row in s:
        print(''.join(row))

    return sum(y*x for y, x in intersections)


def part2():
    program = read_program('2019/input/day_17')
    program[0] = 2
    vm = IntCodeComputerVM(program)
    vm.input_provided_from(ascii_input())
    s = []
    row = []
    for r in vm.run():
        char = chr(r)
        if char == '\n':
            s.append(row)
            print(''.join(row))
            row = []
        else:
            row.append(char)


if __name__ == '__main__':
    #print('Part 1:', part1())
    print('Part 2:', part2())
