from functools import lru_cache
from utils import timeIt
import heapq
from dataclasses import dataclass
from typing import Set, Tuple, Any
from collections import defaultdict, deque


def getMaze(filePath):
    maze = []
    with open(filePath) as file:
        for line in file:
            maze.append(line.strip())
        return Maze(maze)


def manhattanDistance(p1, p2):
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])


@lru_cache(None)
def getDist(key1, key2):
    p2 = keyLocations[key2]
    visited = set()
    toVisit = [(0, keyLocations[key1], frozenset(), frozenset(), 0)]
    while toVisit:
        _, curr, freeKeys, requiredKeys, steps = heapq.heappop(toVisit)
        for nextStep in getNeighbours(curr):
            if nextStep in visited:
                continue
            visited.add(nextStep)

            if nextStep == p2:
                return (steps+1, freeKeys | {key2}, requiredKeys - freeKeys)

            tile = maze[nextStep[0]][nextStep[1]]
            if tile.isalpha():
                if tile.isupper():
                    requiredKeys |= {tile.lower()}
                else:
                    freeKeys |= {tile}
            heapq.heappush(toVisit, ((manhattanDistance(nextStep, p2), nextStep, freeKeys, requiredKeys, steps+1)))
    raise Exception("Uh, this shouldn't happen")


def estimateCost(k1, remaining):
    if not remaining:
        return 0
    pos = keyLocations[k1]
    if len(remaining) == 1:
        return manhattanDistance(pos, keyLocations[next(iter(remaining))])
    left, right = min(map(keyLocations.get, remaining)), max(map(keyLocations.get, remaining))
    firstRoute = min(manhattanDistance(pos, left), manhattanDistance(pos, right))
    secondRoute = manhattanDistance(left, right)
    return firstRoute + secondRoute       


def aStar(maze, start):
    stuff = [(0, 0, start, frozenset(), allKeys)]
    seen = dict()
    while stuff:
        _, steps, k1, keys, notVisited = heapq.heappop(stuff)
        for k2 in notVisited:
            stepsToKey, newKeys, requiredKeys = getDist(k1, k2)
            if not keys.issuperset(requiredKeys):
                continue
            currentCost = steps + stepsToKey

            toVisit = notVisited - newKeys
            if not toVisit:
                return currentCost

            fp = (k2, toVisit)
            if fp in seen and seen[fp] <= currentCost:
                continue
            seen[fp] = currentCost

            newKeys |= keys
            estimatedCost = estimateCost(k2, newKeys)
            heapq.heappush(stuff, (currentCost + estimatedCost, currentCost, k2, newKeys, toVisit))

class Maze:
    def __init__(self, maze):
        self.__maze = maze
        self.keyLocations = self.__getKeyLocations()
        self.startPositions = self.__getStartPositions()
        self.allKeys = frozenset(sorted(self.keyLocations.keys()))
        
    @lru_cache(None)
    def getCost(self, p1, p2):
        if p2 < p1:
            return self.getCost(p2, p1)
        k1 = self.__maze[p1[0]][p1[1]]
        k2 = self.__maze[p2[0]][p2[1]]
        toVisit = [(0, 0, p1, frozenset(), frozenset({p1}))]
        woh = defaultdict(dict)
        while toVisit:
            _, steps, curr, r, v = heapq.heappop(toVisit)
            for nextStep in self.getConnected(curr):
                visited = v
                requiredKeys = r
                if woh[nextStep].get(requiredKeys, 1<<32) <= steps:
                    continue
                woh[nextStep][requiredKeys] = steps+1
                if nextStep in visited:
                    continue
                visited |= {nextStep}

                if nextStep == p2:
                    return (steps+1, requiredKeys)

                tile = self.getTile(nextStep)
                if tile.isalpha():
                    requiredKeys |= {tile.lower()}

                heapq.heappush(toVisit, ((steps+1+manhattanDistance(nextStep, p2), steps+1, nextStep, requiredKeys, visited)))
        raise Exception("This shouldn't happen")

    def getTile(self, pos):
        return self.__maze[pos[0]][pos[1]]

    def getConnected(self, pos):
        for p in ((pos[0]+1, pos[1]), (pos[0]-1, pos[1]), (pos[0], pos[1]+1), (pos[0], pos[1]-1)):
            if self.getTile(p) != '#':
                yield p

    def __getKeyLocations(self):
        return {c : (y, x) for y, row in enumerate(self.__maze) for x, c in enumerate(row) if c.islower()}

    def __getStartPositions(self):
        return [(y, x) for y, row in enumerate(self.__maze) for x, c in enumerate(row) if c == '@']


@dataclass(frozen=True, eq=True, repr=True, order=True)
class AStarNode1:
    pos: Tuple[int]
    remaining: Set[str]
    
    def goalReached(self):
        return not self.remaining

    def getNeighbours(self, maze):
        for k2 in sorted(self.remaining):
            p2 = maze.keyLocations[k2]
            toVisit = self.remaining - {k2}
            stepsToKey, requiredKeys = maze.getCost(self.pos, p2)
            if not self.remaining.isdisjoint(requiredKeys):
                continue
            yield stepsToKey, AStarNode1(p2, toVisit)
    
    def estimateCost(self, maze):
        if not self.remaining:
                return 0
        if len(self.remaining) == 1:
            return manhattanDistance(self.pos, maze.keyLocations[next(iter(self.remaining))])
        left, right = min(map(maze.keyLocations.get, self.remaining)), max(map(maze.keyLocations.get, self.remaining))
        firstRoute = min(manhattanDistance(self.pos, left), manhattanDistance(self.pos, right))
        secondRoute = manhattanDistance(left, right)
        return firstRoute + secondRoute


def aStarSolve(maze, start):
    stuff = [(0, 0, start)]
    seen = dict()
    while stuff:
        _, cost, n1 = heapq.heappop(stuff)
        for costToMove, n2 in n1.getNeighbours(maze):
            totalCost = cost + costToMove
            if n2.goalReached():
                return totalCost
            if n2 in seen and seen[n2] <= totalCost:
                continue
            seen[n2] = totalCost
            estimatedCost = n2.estimateCost(maze)
            heapq.heappush(stuff, (totalCost + estimatedCost, totalCost, n2))


@timeIt
def part1():
    maze = getMaze('2019/input/day_18')
    assert len(maze.startPositions) == 1
    startPos = maze.startPositions[0]
    node = AStarNode1(pos=startPos, remaining=maze.allKeys)
    return aStarSolve(maze, node)
    
def part2():
    pass


if __name__ == '__main__':
    print('Part 1:', part1())
    print('Part 2:', part2())
