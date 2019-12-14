
import re
class Moon:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.vx = 0
        self.vy = 0
        self.vz = 0

    def apply_gravity_from(self, other):
        if self.x < other.x:
            self.vx += 1
        elif self.x > other.x:
            self.vx -= 1

        if self.y < other.y:
            self.vy += 1
        elif self.y > other.y:
            self.vy -= 1

        if self.z < other.z:
            self.vz += 1
        elif self.z > other.z:
            self.vz -= 1
    
    def tick(self):
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz
    
    def __kinetic_energy(self):
        return abs(self.vx) + abs(self.vy) + abs(self.vz)
    
    def __potential_energy(self):
        return abs(self.x) + abs(self.y) + abs(self.z)
    
    def energy(self):
        return self.__kinetic_energy() * self.__potential_energy()
    
    def __hash__(self):
        return hash((self.x, self.y, self.z, self.vx, self.vy, self.vz))

    def x_hash(self):
        return hash((self.x, self.vx))
        
    def y_hash(self):
        return hash((self.y, self.vy))
    
    def z_hash(self):
        return hash((self.z, self.vz))

def get_moons():
    regex = re.compile(r'=(-?\d+)')
    with open('2019/input/day_12') as file:
        moons = {Moon(*map(int, regex.findall(line))) for line in file}
        return moons


def part1():
    moons = get_moons()
    for tick in range(1000):
        for m1 in moons:
            for m2 in moons:
                m1.apply_gravity_from(m2)
        
        for moon in moons:
            moon.tick()
    return sum(moon.energy() for moon in moons)

def part2():
    periods = []
    for hash_fun in [Moon.x_hash, Moon.y_hash, Moon.z_hash]:
        moons = get_moons()
        states = {}
        for tick in range(10000000000):
            for m1 in moons:
                for m2 in moons:
                    m1.apply_gravity_from(m2)
            state = tuple(hash_fun(m) for m in moons)
            if state in states:
                periods.append((tick, tick - states[state]))
                break
            states[state] = tick
            for moon in moons:
                moon.tick()
    
    print(periods)
    x_period_data, y_period_data, z_period_data = periods

    x_tick, x_period = x_period_data
    y_tick, y_period = y_period_data
    z_tick, z_period = z_period_data

    search_to = 100
    while True:
        print(search_to)
        x_ticks = {x for x in range(x_tick, search_to, x_period)}
        x_tick += x_period * len(x_ticks)

        y_ticks = {y for y in range(y_tick, search_to, y_period)}
        y_tick += y_period * len(y_ticks)

        z_ticks = {z for z in range(z_tick, search_to, z_period)}
        z_tick += z_period * len(z_ticks)

        intersection = set.intersection(x_ticks, y_ticks, z_ticks)
        print(intersection)
        if intersection:
            return min(intersection)

        search_to += search_to


if __name__ == '__main__':
    # print('Part 1:', part1())
    print('Part 2:', part2())
