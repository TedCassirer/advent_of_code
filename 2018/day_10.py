from utils import readData, timeIt
import re

class Point:

    def __init__(self, x, y, xv, yv):
        self.x = x
        self.y = y
        self.xv = xv
        self.yv = yv
    
    def getCoordinates(self):
        return self.x, self.y
    
    def step(self, n=1):
        self.x += self.xv*n
        self.y += self.yv*n

    def stepBackwards(self, n=1):
        self.x -= self.xv*n
        self.y -= self.yv*n

    def __repr__(self):
        return str((self.x, self.y, (self.xv, self.yv)))

def getPoints():
    regex = re.compile(r'^position\=<\s?(?P<x>-?\d+), \s?(?P<y>-?\d+)> velocity\=<\s?(?P<xv>-?\d+), \s?(?P<yv>-?\d+)>')
    for line in readData('2018/data/day_10'):
        yield Point(*map(int, regex.search(line).groups()))

def getWindowsize(points):
    x_min, x_max = min(points, key=lambda p: p.x), max(points, key=lambda p: p.x)
    y_min, y_max = min(points, key=lambda p: p.y), max(points, key=lambda p: p.y)
    return ((x_min.x, x_max.x+1), (y_min.y, y_max.y+1))

def getWindowArea(points):
    X, Y = getWindowsize(points)
    return (X[1]-X[0]) * (Y[1]-Y[0])

def printPoints(points):
    X, Y = getWindowsize(points)
    x_offset, y_offset = X[0], Y[0]
    matrix = []
    for _ in range(*Y):
        matrix.append(['.' for _ in range(*X)])
    
    for x, y in map(Point.getCoordinates, points):
        matrix[y-y_offset][x-x_offset] = '#'
    
    [print(''.join(row)) for row in matrix]




@timeIt
def part1():
    points = list(getPoints())
    prevWindowArea = 1 << 63
    windowArea = getWindowArea(points)
    while prevWindowArea > windowArea:
        #printPoints(points)
        [p.step(1000) for p in points]
        prevWindowArea = windowArea
        windowArea = getWindowArea(points)

    [p.stepBackwards(1000) for p in points]

    prevWindowArea = 1 << 63
    windowArea = getWindowArea(points)
    while prevWindowArea > windowArea:
        #printPoints(points)
        [p.step() for p in points]
        prevWindowArea = windowArea
        windowArea = getWindowArea(points)
    
    [p.stepBackwards() for p in points]
    printPoints(points)



@timeIt
def part2():
    time = 0
    points = list(getPoints())
    prevWindowArea = 1 << 63
    windowArea = getWindowArea(points)
    while prevWindowArea > windowArea:
        #printPoints(points)
        [p.step(1000) for p in points]
        prevWindowArea = windowArea
        windowArea = getWindowArea(points)
        time += 1000

    [p.stepBackwards(1000) for p in points]
    time -= 1000

    prevWindowArea = 1 << 63
    windowArea = getWindowArea(points)
    while prevWindowArea > windowArea:
        #printPoints(points)
        [p.step() for p in points]
        prevWindowArea = windowArea
        windowArea = getWindowArea(points)
        time += 1
    
    [p.stepBackwards() for p in points]
    time -= 1

    printPoints(points)
    return time

if __name__ == '__main__':
    print('Part 1:', part1())
    print('Part 2:', part2())
