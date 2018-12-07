from itertools import chain, product
from utils import readData, timeIt
from itertools import chain, product


class Rectangle:
    def __init__(self, x1, x2, y1, y2, id=''):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.id = id

    def overlaps(self, other):
        return other.x1 < self.x2 and (
        other.y1 <= self.y1 <= other.y2 or self.y1 <= other.y1 <= self.y2)

    def getOverlap(self, other):
        return Rectangle(max(self.x1, other.x1), min(self.x2, other.x2),
                         max(self.y1, other.y1), min(self.y2, other.y2))

    def breakDown(self):
        yield from product(range(self.x1, self.x2), range(self.y1, self.y2))

    def __lt__(self, other):
        return (self.x1, self.y1) < (other.x1, other.y1)

    def __repr__(self):
        return self.id


def getRectangles():
    for line in readData('2018/data/day_3'):
        id, _, corner, size = line.split()
        x1, y1 = map(int, corner[:-1].split(','))
        xd, yd = map(int, size.split('x'))
        x2, y2 = x1 + xd, y1 + yd
        yield Rectangle(x1, x2, y1, y2, id)


def getOverlappingRectangles(rectangles):
    rectangles = sorted(rectangles)
    for i1, r1 in enumerate(rectangles):
        for r2 in rectangles[i1 + 1:]:
            if r1.x2 < r2.x1:
                break
            if r1.overlaps(r2):
                yield r1, r2


def getOverlaps(rectangles):
    for r1, r2 in getOverlappingRectangles(rectangles):
        yield r1.getOverlap(r2)


@timeIt
def part1():
    rectangles = getRectangles()
    overlaps = getOverlaps(rectangles)
    tiles = set(chain(*map(Rectangle.breakDown, overlaps)))
    return len(tiles)


@timeIt
def part2():
    rectangles = set(getRectangles())
    overlapping = set(s for rects in getOverlappingRectangles(rectangles) for s in rects)
    return rectangles - overlapping


if __name__ == '__main__':
    print('Part 1:', part1())
    print('Part 2:', part2())
