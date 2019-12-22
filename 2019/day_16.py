from itertools import cycle

PATTERN = [0, 1, 0, -1]

def flatten(nested_list):
    for inner in nested_list:
        for n in inner:
            yield n

def pattern_factors(phase, pattern=PATTERN):
    multi_pattern = cycle(flatten(zip(*(PATTERN for _ in range(phase)))))
    next(multi_pattern)
    yield from multi_pattern

def transform_number(pos, signal):
    factors = pattern_factors(pos)
    # num = 0
    # s = []
    # for n, fac in zip(signal, factors):
    #     num += n * fac
    #     s.append(f'{n}*{fac}')
    # print(' + '.join(s) + ' = ' + str(abs(num) % 10))
    # return abs(num) % 10
    return abs(sum(n * next(factors) for n in signal)) % 10

def FFT(signal):
    return [transform_number(i+1, signal) for i in range(len(signal))]

def get_input_signal():
    with open('2019/input/day_16') as file:
        return [int(n) for n in file.readline()]

def part1():
    signal = get_input_signal()
    for _ in range(100):
        signal = FFT(signal)
    return ''.join(str(n) for n in signal[:8])

def part2():
    signal = get_input_signal() * 100
    offset = int(''.join(str(n) for n in signal)[:7])
    for _ in range(100):
        print(_)
        print(''.join(str(n) for n in signal[:]))
        signal = FFT(signal)
    signal = signal * 5
    return signal[offset:offset+8]


if __name__ == '__main__':
    print('Part 1:', part1())
    print('Part 2:', part2())
