def get_input():
    with open('2019/input/day_1') as input:
        yield from (int(i) for i in input)

def fuelbois(n):
    return ((n//3)-2)

def part1():
    return sum(map(fuelbois, get_input()))

def part2():
    return sum(map(doTheThing, get_input()))

def doTheThing(n):
    s = fuelbois(n)
    if s <= 0:
        return 0
    return s + doTheThing(s)
 
if __name__ == '__main__':
    print('Part 1:', part1())
    print('Part 2:', part2())