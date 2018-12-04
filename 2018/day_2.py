from collections import Counter
from functools import reduce

def getData():
    with open('2018/data/day2') as data:
        yield from data

def part1():
    letterCounts = map(Counter, getData())
    letterCounts = map(lambda count: set(count.values()), letterCounts)

    threeLetters = 0
    twoLetters = 0

    for letterCount in letterCounts:
        threeLetters += 3 in letterCount
        twoLetters += 2 in letterCount

    return threeLetters * twoLetters

def part2():
    def maskLetter(word, i):
        return word[:i] + word[i+1:]

    words = list(getData())
    N = len(words[0])
    for i in range(N):
        seen = set()
        for word in words:
            maskedWord = maskLetter(word, i)
            if maskedWord in seen:
                return maskedWord
            else:
                seen.add(maskedWord)
            

if __name__ == '__main__':
    print('Part 1:', part1())
    print('Part 2:', part2())