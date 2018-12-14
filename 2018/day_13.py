from utils import timeIt
import re

def readData(path):
    with open(path) as data:
        yield from data
class Direction:
    UP = '^'
    RIGHT = '>'
    DOWN = 'v'
    LEFT = '<'

    TURN1 = '/'
    TURN2 = '\\'

    INTERSECTION = '+'

    MOVEMENT = {
        UP : (-1, 0),
        RIGHT : (0, 1),
        DOWN : (1, 0),
        LEFT : (0, -1)
    }
    
    TURNS = {
        TURN1: {
            UP : RIGHT,
            RIGHT : UP,
            DOWN : LEFT,
            LEFT : DOWN
        },
        TURN2: {
            UP : LEFT,
            RIGHT : DOWN,
            DOWN : RIGHT,
            LEFT : UP
        }
    }

    INTERSECTION_TURN = [
        {
            UP: LEFT,
            RIGHT: UP,
            DOWN: RIGHT,
            LEFT: DOWN            
        },
        {
            UP: UP,
            RIGHT: RIGHT,
            DOWN: DOWN,
            LEFT: LEFT
        },
        {
            UP: RIGHT,
            RIGHT: DOWN,
            DOWN: LEFT,
            LEFT: UP
        }
    ]

class Train:
    def __init__(self, pos, direction):
        self.pos = pos
        self.direction = direction
        self.intersectionCounter = 0

    def move(self):
        self.pos = tuple(map(int.__add__, self.pos, Direction.MOVEMENT[self.direction]))

    def setDirection(self, tile):
        if tile in Direction.TURNS:
            self.direction = Direction.TURNS[tile][self.direction]
        elif tile == Direction.INTERSECTION:
            self.direction = Direction.INTERSECTION_TURN[self.intersectionCounter%3][self.direction]
            self.intersectionCounter += 1

    def tick(self, graph):
        self.move()
        tile = graph[self.pos[0]][self.pos[1]]
        self.setDirection(tile)
        return self.pos

    def __repr__(self):
        return str(self.pos) + ', ' + self.direction

def buildGraph():
    data = readData('2018/data/day_13')
    graph = []
    trains = []
    trainFind = re.compile((r'v|\<|\^|\>'))
    for row, line in enumerate(data):
        for m in trainFind.finditer(line):
            direction = line[m.span()[0]]
            trains.append(Train((row, m.span()[0]), direction))
        graph.append(line)
    return graph, trains

@timeIt
def part1():
    graph, trains = buildGraph()
    taken = set(t.pos for t in trains)
    while True:
        for train in trains:
            taken.remove(train.pos)
            newPos = train.tick(graph)
            if newPos in taken:
                return tuple(reversed(newPos))
            taken.add(newPos)
        


@timeIt
def part2():
    graph, trains = buildGraph()
    taken = {t.pos: t for t in trains}
    while True:
        for train in trains[:]:
            if not train.pos in taken:
                continue
            taken.pop(train.pos)
            newPos = train.tick(graph)
            if newPos in taken:
                otherTrain = taken.pop(newPos)
                trains.remove(train)
                trains.remove(otherTrain)
                if len(trains) == 1:
                    return tuple(reversed(trains[0].pos))
            else:
                taken[newPos] = train
        

if __name__ == '__main__':
    print('Part 1:', part1())
    print('Part 2:', part2())
