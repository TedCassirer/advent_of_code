from functools import lru_cache
from utils import timeIt
import heapq


def getMaze():
    maze = []
    with open('2019/input/day_18') as file:
        for line in file:
            maze.append(line.strip())
        return maze


def getKeyLocations(maze):
    keys = {}
    for y, row in enumerate(maze):
        for x, c in enumerate(row):
            if c == '@' or (c.isalpha() and c.islower()):
                keys[c] = (y, x)
    return keys


maze = getMaze()
keyLocations = getKeyLocations(maze)
allKeys = frozenset(keyLocations.keys()) - {'@'}


def manhattanDistance(p1, p2):
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])


def getNeighbours(p1):
    for p in ((p1[0]+1, p1[1]), (p1[0]-1, p1[1]), (p1[0], p1[1]+1), (p1[0], p1[1]-1)):
        if maze[p[0]][p[1]] != '#':
            yield p


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


@timeIt
def part1():
    return aStar(maze, '@')


def part2():
    pass


if __name__ == '__main__':
    print('Part 1:', part1())
    print('Part 2:', part2())
