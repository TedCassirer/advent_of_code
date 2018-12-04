
def getData(loop=False):
    while True:
        with open('2018/data/day1') as data:
            yield from data
        if not loop:
            break

def part1():
    return sum(map(int, getData()))

def part2():
    seen = {0}
    currentFrequency = 0
    for frequency in map(int, getData(True)):
        currentFrequency += frequency
        if currentFrequency in seen:
            return currentFrequency
        else:
            seen.add(currentFrequency)
            
if __name__ == '__main__':
    print('Part 1:', part1())
    print('Part 2:', part2())