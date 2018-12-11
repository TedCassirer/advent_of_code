from utils import readData, timeIt
from collections import defaultdict
import heapq

class Node:
    def __init__(self, id):
        self.id = id
        self.before = set()
        self.after = set()
        self.time = self.getTime()

    def remove(self):
        for n in self.after:
            n.before.remove(self)

    def getTime(self):
        return ord(self.id) - ord('A')+61

    def __lt__(self, other):
        return self.time < other.time

    def __repr__(self):
        return str((self.id, self.time))

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
    nodes = getOrders()
    workers = 5
    work = []
    currentTime = 0
    ready = []
    while nodes:
        for n in list(nodes):
            if len(n.before) == 0:
                ready.append(n)
                nodes.remove(n)
        while ready and workers:
            task = ready.pop()
            task.time += currentTime
            heapq.heappush(work, task)
            workers -= 1
        completedWork = heapq.heappop(work)
        currentTime = completedWork.time
        workers += 1 
        for aw in completedWork.after:
            aw.before.remove(completedWork)
    return currentTime

if __name__ == '__main__':
    print('Part 1:', part1())
    print('Part 2:', part2())
