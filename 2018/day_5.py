from itertools import chain, product
from utils import readData, timeIt

def doesReact(c1, c2):
    return c1.swapcase() == c2

def reactPolymer(polymer):
    i = 0
    while i < len(polymer)-1:
        c1, c2 = polymer[i], polymer[i+1]
        if doesReact(c1, c2):
            polymer = polymer[:i] + polymer[i+2:]
            i -= 1 if i > 0 else 0
        else:
            i += 1    
    return polymer

def getPolymerPairs(polymer):
    chars = set(p for p in polymer if p.islower())
    yield from ((p, p.upper()) for p in chars)

@timeIt
def part1():
    polymer = str(next(readData('2018/data/day_5')))
    return len(reactPolymer(polymer))        

@timeIt
def part2():
    polymer = str(next(readData('2018/data/day_5')))
    polymerPairs = getPolymerPairs(polymer)
    reducedForms = map(lambda p: polymer.replace(p[0], '').replace(p[1], ''), polymerPairs)
    reactedPolymers = map(reactPolymer, reducedForms)
    return min(map(len, reactedPolymers))

if __name__ == '__main__':
    print('Part 1:', part1())
    print('Part 2:', part2())
