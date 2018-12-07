from utils import timeIt, readData
import re
from datetime import datetime
from collections import defaultdict

parser = re.compile(r'\[(?P<timestamp>.*)\] (?P<event>.*)')
timeFormat = '%Y-%m-%d %H:%M'


def parseText(text):
    timestamp, event = parser.search(text).groups()
    timestamp = datetime.strptime(timestamp, timeFormat)
    return timestamp, event

def getGuardId(event):
    return int(re.search(r'Guard \#(\d+) begins', event).group(1))

def getSleepEvents():
	currentGuard = None
	sleepStart = None
	for ts, event in sorted(map(parseText, readData('2018/data/day_4'))):
		if event == 'wakes up':
			yield currentGuard, sleepStart, ts
			sleepStart = None
		elif event == 'falls asleep':
			assert sleepStart == None
			sleepStart = ts
		else:
			currentGuard = getGuardId(event)

def getSleepSchedule():
	sleepSchedule = defaultdict(lambda: [0]*60)
	for guard, sleepStart, sleepEnd in getSleepEvents():
		sleep = sleepSchedule[guard]
		for minute in range(sleepStart.minute, sleepEnd.minute):
			sleep[minute] += 1
	return sleepSchedule

@timeIt
def part1():
	sleepSchedule = getSleepSchedule()
	mostSleepyGuard, timesAsleep = max(sleepSchedule.items(), key=lambda sleep: sum(sleep[1]))
	sleepyMinute = timesAsleep.index(max(timesAsleep))
	return mostSleepyGuard * sleepyMinute

@timeIt
def part2():
	sleepSchedule = getSleepSchedule()
	mostSleepyGuard, timesAsleep = max(sleepSchedule.items(), key=lambda sleep: max(sleep[1]))
	sleepyMinute = timesAsleep.index(max(timesAsleep))
	return mostSleepyGuard * sleepyMinute


if __name__ == '__main__':
    print('Part 1:', part1())
    print('Part 2:', part2())