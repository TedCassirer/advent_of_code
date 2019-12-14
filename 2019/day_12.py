
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
    pass

if __name__ == '__main__':
    print('Part 1:', part1())
    print('Part 2:', part2())
