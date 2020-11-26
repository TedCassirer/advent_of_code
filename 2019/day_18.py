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
def getPath(key1, key2):
    visited = set()
    toVisit = deque([(keyLocations[key1], frozenset(), frozenset(), 0)])
    while toVisit:
        curr, freeKeys, requiredKeys, steps = toVisit.pop()
        tile = maze[curr[0]][curr[1]]
        if curr in visited or tile == '#':
            continue
        if tile == key2:
            return (steps, freeKeys|{key2} , requiredKeys - freeKeys)
        if tile.isalpha():
            if tile.isupper():
                requiredKeys |= {tile.lower()}
            else:
                freeKeys |= {tile}
        for nextStep in ((curr[0]+1, curr[1]), (curr[0]-1, curr[1]), (curr[0], curr[1]+1), (curr[0], curr[1]-1)):
            toVisit.append((nextStep, freeKeys, requiredKeys, steps+1))
        visited.add(curr)

seen = dict()
def simpleSearch(current, owned, toFind, currentSteps=0, shortest=1<<32):
    fp = (current, owned)
    if fp in seen and seen[fp] <= currentSteps:
        return shortest
    seen[fp] = currentSteps

    if currentSteps >= shortest:
        return shortest
    if not toFind:
        print(currentSteps)
        return currentSteps
    for path, k2 in sorted((getPath(current, k2), k2) for k2 in toFind):
        steps, freeKeys, requiredKeys = path 
        keys = owned|freeKeys
        if keys.issuperset(requiredKeys):
            tmp = simpleSearch(k2, keys, toFind-freeKeys, currentSteps+steps, shortest)
            shortest = min(shortest, tmp)
    return shortest

    
@timeIt
def part1():
    return simpleSearch('@', frozenset('@'), frozenset(keyLocations.keys()) - {'@'}, 0)

def part2():
    pass

if __name__ == '__main__':
    print('Part 1:', part1())
    print('Part 2:', part2())