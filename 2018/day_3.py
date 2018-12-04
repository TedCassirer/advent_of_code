def read_data(path):
    with open(path) as data:
        yield from data


class Rectangle:
    def __init__(self, x1, x2, y1, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    
    def overlaps(self, other):
        return self.x2 > other.x1  and self.y2 > other.y1

    def getOverlap(self, other):
        return Rectangle(max(self.x1, other.x1), min(self.x2, other.x2), max(self.y1, other.y1), min(self.y2, other.y2))

    def getArea(self):
        return (self.x2-self.x1) * (self.y2-self.y1)

    def __lt__(self, other):
        return (self.x1, self.y1) < (other.x1, other.y1)

    def __str__(self):
        return str((self.x1, self.y1, self.x2, self.y2))

def getRectangles():
    for line in read_data('2018/data/day_3'):
        id, _, corner, size = line.split()

        x1, y1 = map(int, corner[:-1].split(','))
        xd, yd = map(int, size.split('x'))
        x2, y2 = x1+xd, y1+yd
        yield Rectangle(x1, x2, y1, y2)
        
def getOverlaps(rectangles):
    for i1, r1 in enumerate(rectangles):
        for r2 in rectangles[i1+1:]:
            if r1.x2 < r2.x1 or r1.y2 < r2.y1:
                break
            if r1.overlaps(r2):
                yield r1.getOverlap(r2)

def part1():
    rectangles = sorted(getRectangles())
    overlaps = list(getOverlaps(rectangles))
    overOverlaps = list(getOverlaps(sorted(overlaps)))
    print([str(r) for r in overlaps])
    print([str(r) for r in overOverlaps])
    print(sum(map(Rectangle.getArea, overlaps)),  sum(map(Rectangle.getArea, overOverlaps)))
    return sum(map(Rectangle.getArea, overlaps)) - sum(map(Rectangle.getArea, overOverlaps))



    
if __name__ == '__main__':
    print('Part 1:', part1())