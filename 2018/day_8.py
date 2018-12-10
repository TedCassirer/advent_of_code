from utils import readData, timeIt

class Node:
    def __init__(self):
        self.metadata = []
        self.children = []

    def getMetadata(self):
        return self.metadata

    def getValue(self):
        return sum(self.metadata) + sum(map(Node.getValue, self.children))

    def getValue2(self):
        if self.children:
            res = 0
            for ci in self.metadata:
                if ci-1 < len(self.children):
                    res += self.children[ci-1].getValue2()
            return res
        else:
            return sum(self.metadata)
    def __repr__(self):
        return str(self.metadata) + ' | ' + str(self.children)

def parseNodes(numbers):
    node = Node()
    childrenCount = next(numbers)
    metadataCount = next(numbers)
    for _ in range(childrenCount):
        node.children.append(parseNodes(numbers))
    for _ in range(metadataCount):
        node.metadata.append(next(numbers))
    return node

@timeIt
def part1():
    numbers = (int(i) for i in next(readData('2018/data/day_8')).split(' '))
    root = parseNodes(numbers)
    return root.getValue()

@timeIt
def part2():
    numbers = (int(i) for i in next(readData('2018/data/day_8')).split(' '))
    root = parseNodes(numbers)
    return root.getValue2()


if __name__ == '__main__':
    print('Part 1:', part1())
    print('Part 2:', part2())
