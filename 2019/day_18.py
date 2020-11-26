from functools import lru_cache
from collections import deque
from utils import timeIt

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

@lru_cache(None)
def findPath(key1, key2):
    visited = set()
    toVisit = deque([(keyLocations[key1], frozenset(), frozenset(), 0)])
    paths = []
    while toVisit:
        curr, freeKeys, requiredKeys, steps = toVisit.pop()
        tile = maze[curr[0]][curr[1]]
        if curr in visited or tile == '#':
            continue
        if tile == key2:
            paths.append((steps, freeKeys, requiredKeys))
            continue
        if tile.isalpha():
            if tile.islower():
                freeKeys |= {tile}
            elif not tile.lower() in freeKeys:
                requiredKeys |= {tile.lower()}
        for nextStep in ((curr[0]+1, curr[1]), (curr[0]-1, curr[1]), (curr[0], curr[1]+1), (curr[0], curr[1]-1)):
            toVisit.append((nextStep, freeKeys, requiredKeys, steps+1))
        visited.add(curr)
    
    return paths

def findBestPath():
    seen = dict()
    def inner(startKey, keys, stepsTaken, shortest):
        fingerPrint = (startKey, keys)
        if fingerPrint in seen and seen[fingerPrint] <= stepsTaken:
            return shortest
        else:
            seen[fingerPrint] = stepsTaken

        if len(keys) == len(keyLocations):
            assert stepsTaken < shortest
            return stepsTaken

        toCheck = []
        for key in keyLocations.keys() - keys:
            paths = [(s, f, r) for s, f, r in findPath(startKey, key) if keys.issuperset((r | f))]
            if not paths:
                continue
            stepsToKey, freeKeys, requiredKeys = min(paths)
            toCheck.append((stepsToKey, key, freeKeys | keys | {key}))
        toCheck.sort()

        for stepsToKey, key, ownedKeys in toCheck:
            if stepsToKey + stepsTaken < shortest:
                shortest = min(shortest, inner(key, ownedKeys, stepsTaken+stepsToKey, shortest))
        return shortest

    return inner('@', frozenset({'@'}), 0, 1<<32)

@timeIt
def part1():
    return findBestPath()

def part2():
    pass

if __name__ == '__main__':
    print('Part 1:', part1())
    print('Part 2:', part2())