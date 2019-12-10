from collections import defaultdict
from math import gcd, atan2, pi

class Asteroid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    

def get_asteroids():
    with open('2019/input/day_10') as input:
        for y, row in enumerate(input):
            for x, val in enumerate(row):
                if val == '#':
                    yield (x, y)


def get_angle(p1, p2):
    v = (p2[0] - p1[0], p2[1] - p1[1])
    d = gcd(*v)
    return (v[0]//d, v[1]//d)

def radians(dx, dy):
    return atan2(dy, dx)

def distance(p1, p2):
    return abs(p2[0]-p1[0]) + abs(p2[1]-p1[1])

def get_visible_asteroids(asteroids):
    all_visible = defaultdict(dict)
    for a1 in asteroids:
        visible = all_visible[a1]
        for a2 in asteroids - {a1}:
            angle = get_angle(a1, a2)
            already_visible_asteroid = visible.get(angle)
            if already_visible_asteroid:
                visible[angle] = min(already_visible_asteroid, a2, key=lambda a: distance(a1, a))
            else:
                visible[angle] = a2
    return all_visible


def part1():
    asteroids = set(get_asteroids())
    visible_asteroids = get_visible_asteroids(asteroids)
    return max(map(len, visible_asteroids.values()))



def part2():
    def transform(dx, dy):
        return ((radians(dx, dy) + pi/2) % (2*pi))

    asteroids = set(get_asteroids())
    all_visible = get_visible_asteroids(asteroids)
    visible = max(all_visible.values(), key=len)
    asteroid_destroy_order = sorted(visible.items(), key=lambda kv: transform(*kv[0]))
    x, y = asteroid_destroy_order[199][1]
    return x*100 + y


if __name__ == '__main__':
    print('Part 1:', part1())
    print('Part 2:', part2())
