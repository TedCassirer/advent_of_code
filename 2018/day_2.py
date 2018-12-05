from collections import Counter
from utils import time_it, read_data

@time_it
def part1():
    letterCounts = map(dict.values, map(Counter, read_data('2018/data/day_2')))

    threeLetters = 0
    twoLetters = 0

    for letterCount in letterCounts:
        threeLetters += 3 in letterCount
        twoLetters += 2 in letterCount

    return threeLetters * twoLetters

@time_it
def part2():
    def maskLetter(word, i):
        return word[:i] + word[i+1:]

    words = list(read_data('2018/data/day_2'))
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