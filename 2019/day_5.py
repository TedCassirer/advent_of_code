from IntCodeComputer import IntCodeComputerVM

def read_file(path):
    with open(path) as input:
        return [int(n) for n in input.readline().split(',')]


def part1():
    program = read_file('2019/input/day_5')
    vm = IntCodeComputerVM(program, 1)
    while not vm.halted:
        vm.run()
    return vm.out


def part2():
    program = read_file('2019/input/day_5')
    vm = IntCodeComputerVM(program, 5)
    while not vm.halted:
        vm.run()
    return vm.out


if __name__ == '__main__':
    print('Part 1:', part1())
    print('Part 2:', part2())
