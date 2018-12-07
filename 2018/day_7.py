from utils import readData, timeIt
from collections import defaultdict, deque
class Node:
    def __init__(self, id):
        self.id = id
        self.before = set()
        self.after = set()

    def remove(self):
        for n in self.after:
            n.before.remove(self)

    def getTime(self):
        return ord(self.id) - ord('A')+1

    def __lt__(self, other):
        return self.id < other.id

    def __repr__(self):
        return self.id

def getOrders():
    nodes = dict()
    for row in readData('2018/data/day_7'):
        items = row.split(' ')
        bef, aft = items[1], items[-3]
        if bef not in nodes:
            nodes[bef] = Node(bef)
        if aft not in nodes:
            nodes[aft] = Node(aft)
        before, after = nodes[bef], nodes[aft]
        before.after.add(after)
        after.before.add(before)
    return set(nodes.values())

def doWork(nodes, workers=2):
    currentTime = 0
    nodes = sorted(nodes, key=Node.getTime, reverse=True)
    processing = deque(map(Node.getTime, nodes[-workers:]))
    while processing:
        deltaTime = processing.pop()
        for i in range(len(processing)):
            processing[i] -= deltaTime
            assert processing[i] >= 0
        if nodes:
            processing.appendleft(nodes.pop().getTime())
        currentTime += deltaTime
        
    return currentTime

@timeIt
def part1():
    result = []
    nodes = getOrders()
    # Get first node
    while nodes:
        ready = min(filter(lambda n: len(n.before) == 0, nodes))
        result.append(ready.id)
        for work in ready.after:
            work.before.remove(ready)
        nodes.remove(ready)
        
    return ''.join(result)


@timeIt
def part2():
    totalTime = 0
    nodes = getOrders()
    while nodes:
        ready = list(filter(lambda n: len(n.before) == 0, nodes))
        totalTime += doWork(ready)
        for completedWork in ready:
            for work in completedWork.after:
                work.before.remove(completedWork)
            nodes.remove(completedWork)
    return totalTime

if __name__ == '__main__':
    print('Part 1:', part1())
    print('Part 2:', part2())
