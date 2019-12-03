class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.__coord = (self.x, self.y)

    def __add__(self, other):
        return Coordinate(self.x + other.x, self.y + other.y)

    def __hash__(self):
        return hash(self.__coord)
    
    def __eq__(self, other):
        return self.__coord == other.__coord

directions = {
    'U': Coordinate(0, 1),
    'D': Coordinate(0, -1),
    'R': Coordinate(1, 0),
    'L': Coordinate(-1, 0),
}

def getInput(loop=False):
    with open('2019/input/day_3') as input:
        for line in input:
            yield [(c[0], int(c[1:])) for c in line.split(',')]

def get_line(movements):
    current = Coordinate(0, 0)
    for d, steps in movements:
        direction = directions[d]
        for _ in range(steps):
            current += direction
            yield current

def part1():
    lines = [set(get_line(movements)) for movements in getInput()]
    crossings = set.intersection(*lines)
    distance_from_start = map(lambda c: abs(c.x) + abs(c.y), crossings)
    return min(distance_from_start)

def part2():
    lines = [{coord : step+1 for step, coord in enumerate(get_line(movements))} for movements in getInput()]
    crossings = set.intersection(*(set(l.keys()) for l in lines))
    steps_to_crossing = (sum(l[c] for l in lines) for c in crossings)
    return min(steps_to_crossing)

if __name__ == '__main__':
    print('Part 1:', part1())
    print('Part 2:', part2())