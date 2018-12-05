from utils import time_it, read_data
import re
from datetime import datetime

parser = re.compile(r'\[(?P<timestamp>.*)\]\s{1}(?P<action>.*)')
timeFormat = 'Y-m-d H:M'


def parseText(text):
    timestamp, action = parser.search(text).groups()
    timestamp = datetime.strptime(timeFormat, timestamp)
    return timestamp, action

def getGuardId(action):
    return re.search(r'Guard \#(\d+) begins', action).group(1)

@time_it
def part1():
    for row in read_data('2018/data/day_4'):
        print(parseText(row))


@time_it
def part2():
    pass
            

if __name__ == '__main__':
    print('Part 1:', part1())
    print('Part 2:', part2())