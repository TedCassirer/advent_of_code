def get_input():
    return (138307, 654504)

def get_numbers(start, end):
    for n in range(start, end):
        yield [int(c) for c in str(n)]

def is_double_number(numbers):
    return any(c1 == c2 for c1, c2 in zip(numbers[:-1], numbers[1:]))

def is_sorted(numbers):
    return numbers == sorted(numbers)

def double_number_not_part_of_group(numbers):
    padded_numbers = [None, None] + numbers + [None, None]
    return any(c1 != c2 and c2 == c3 and c3 != c4 for c1, c2, c3, c4 in zip(padded_numbers[:-3], padded_numbers[1:-2], padded_numbers[2:-1], padded_numbers[3:]))

def get_numbers_matching_predicates(*predicates):
    numbers = get_numbers(*get_input())
    matching_numbers = filter(lambda n: all(p(n) for p in predicates), numbers)
    return list(matching_numbers)

def part1():
    matching_numbers = get_numbers_matching_predicates(
        is_sorted,
        is_double_number,
    )
    return len(matching_numbers)

def part2():
    matching_numbers = get_numbers_matching_predicates(
        is_sorted,
        double_number_not_part_of_group,
    )
    return len(matching_numbers)

if __name__ == '__main__':
    print('Part 1:', part1())
    print('Part 2:', part2())