from IntCodeComputer import IntCodeComputerVM, generator_of

def read_file():
    with open('2019/input/day_19') as input:
        return [int(n) for n in input.readline().split(',')]

def scanCoord(y, x, program=read_file()):
    tractorBeam = IntCodeComputerVM(program)
    tractorBeam.input_provided_from(generator_of(x, y))
    return next(tractorBeam.run())

def part1():
    X, Y = 50, 50
    return sum(scanCoord(y, x) for y in range(Y) for x in range(X))

def part2():
    size = 100-1
    x, y = 0, 0
    
    topRight = scanCoord(y, x+size)
    bottomLeft = scanCoord(y+size, x)

    while not (topRight and bottomLeft):
        while not topRight:
            y += 1
            topRight = scanCoord(y, x+size)
        bottomLeft = scanCoord(y+size, x)
        while not bottomLeft:
            x += 1
            bottomLeft = scanCoord(y+size, x)
        topRight = scanCoord(y, x+size)
    assert(scanCoord(y, x))
    assert(scanCoord(y+size, x+size))
    
    return x*10000 + y

if __name__ == '__main__':
    print('Part1:', part1())
    print('Part2:', part2())