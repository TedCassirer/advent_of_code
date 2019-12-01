def getData(loop=False):
    with open('2019/data/day_1') as data:
        yield from data

def fuelbois(n):
    return ((n//3)-2)

def part1():
    return sum((fuelbois(n)) for n in map(int, getData()))

def part2():
    numbers = map(int, getData())
    return sum(map(doTheThing, numbers))

def doTheThing(n):
    s = fuelbois(n)
    if s <= 0:
        return 0
    return s + doTheThing(s)
 
if __name__ == '__main__':
    print('Part 1:', part1())
    print('Part 2:', part2())