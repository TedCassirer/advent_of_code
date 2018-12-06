from utils import readData, timeIt
from functools import reduce

class NodeGroup:
    nextNeighbors = dict()
    taken = set()
    groups = dict()
    X = 0
    Y = 0

    def __init__(self, id, start):
        self.id = id
        self.connected = {start}
        self.outer = {start}
        self.outside = False
        NodeGroup.groups[id] = self

    @staticmethod
    def reserveNext():
        toRemove = set()
        for node in list(NodeGroup.groups.values()):
            if not node.outer:
                if not node.outside:
                    print(len(node.connected))
                NodeGroup.groups.pop(node.id)
                continue
            for edge in node.outer:
                x, y = edge
                if x == -1 or x == NodeGroup.X+1 or y == -1 or y == NodeGroup.Y+1:
                    node.outside = True
                    continue
                for connection in node.getConnections(*edge):
                    if connection in NodeGroup.nextNeighbors and NodeGroup.nextNeighbors[connection] != node.id:
                        toRemove.add(connection)
                    else:
                        NodeGroup.nextNeighbors[connection] = node.id
            node.outer = set()
        for connection in toRemove:
            NodeGroup.taken.add(connection)
            NodeGroup.nextNeighbors.pop(connection)
    

    def getConnections(self, x, y):
        if (x-1, y) not in self.connected and (x-1, y) not in NodeGroup.taken:
            yield (x-1, y)
        if (x+1, y) not in self.connected and (x+1, y) not in NodeGroup.taken:
            yield (x+1, y)
        if (x, y-1) not in self.connected and (x, y-1) not in NodeGroup.taken:
            yield (x, y-1)
        if (x, y+1) not in self.connected and (x, y+1) not in NodeGroup.taken:
            yield (x, y+1)

    @staticmethod
    def advance():
        for coord, id in NodeGroup.nextNeighbors.items():
            node = NodeGroup.groups[id]
            node.connected.add(coord)
            node.outer.add(coord)
            NodeGroup.taken.add(coord)
        NodeGroup.nextNeighbors = dict()
            
    def __repr__(self):
        return '(%s, %s)' % (self.id, self.connected)

@timeIt
def part1():
    data = readData('2018/data/day_6')
    X, Y = 0, 0
    for id, row in enumerate(data):
        x, y = map(int, row.split(', '))
        X = max(X, x)
        Y = max(Y, y)
        NodeGroup(id, (x, y))
    NodeGroup.X = X+1
    NodeGroup.Y = Y+1
    mahGroups = NodeGroup.groups
    while NodeGroup.groups:
        NodeGroup.reserveNext()
        NodeGroup.advance()
    


def getDistance(coord, nodes):
    distance = 0
    for n in nodes:
        distance += abs(coord[0]-n[0]) + abs(coord[1]-n[1])
    return distance

def getConnections(coord):
    x, y = coord
    yield (x-1, y)
    yield (x+1, y)
    yield (x, y-1)
    yield (x, y+1)

def bfs(start, nodes, maxRadius):
    seen = set()
    stack = [start]
    while stack:
        node = stack.pop()
        if node in seen or getDistance(node, nodes) >= maxRadius:
            continue
        seen.add(node)
        stack.extend(getConnections(node))
    return seen

@timeIt
def part2():
    RADIUS = 10000
    data = readData('2018/data/day_6')
    nodes = []
    for id, row in enumerate(data):
        x, y = map(int, row.split(', '))
        nodes.append((x, y))
    N = len(nodes)
    ax, ay = reduce(lambda a, b: (a[0]+b[0], a[1]+b[1]), nodes)
    ax //= N
    ay //= N
    return len(bfs((ax, ay), nodes, RADIUS))

if __name__ == '__main__':
    #print('Part 1:', part1())
    print('Part 2:', part2())
