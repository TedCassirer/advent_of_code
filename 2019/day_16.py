from itertools import cycle
from functools import lru_cache
from collections import Counter


def FFT(signal, start, end, N):
    cache = {}
    def inner(phase, level):
        if level == 0:
            return signal[(phase%len(signal))-1]
        
        key = (phase, level)
        if key in cache:
            return cache[key]
        val = 0
        for p in range(phase-1, len(signal), 4*phase):
            for i in range(p, min(len(signal), p+phase)):
                val += inner(i+1, level-1)
        for p in range(phase*3-1, len(signal), 4*phase):
            for i in range(p, min(len(signal), p+phase)):
                val -= inner(i+1, level-1)
        res = abs(val) % 10
        cache[key] = res
        return res


    return [inner(p+1, N) for p in range(start, end)]        
    
def get_input_signal():
    with open('2019/input/day_16') as file:
        return [int(n) for n in file.readline()]

def part1():
    signal = get_input_signal()
    return ''.join(map(str, FFT(signal, 0, 8, 100)))

def part2():
    signal = get_input_signal()
    offset = int(''.join(str(n) for n in signal)[:7]) % len(signal)
    return ''.join(map(str, FFT(signal, offset, offset+8, 100)))



if __name__ == '__main__':
    print('Part 1:', part1())
    print('Part 2:', part2())
