POSITION = 0
IMMEDIATE = 1

READ = 0
WRITE_TO = 1

ADD = 1
MULTIPLY = 2
INPUT = 3
OUT = 4
JUMP_IF_TRUE = 5
JUMP_IF_FALSE = 6
LESS_THAN = 7
EQUALS = 8
HALT = 99

ACTIONS = {
    ADD: (READ, READ, WRITE_TO),
    MULTIPLY: (READ, READ, WRITE_TO),
    INPUT: (WRITE_TO,),
    OUT: (READ,),
    JUMP_IF_TRUE: (READ, READ),
    JUMP_IF_FALSE: (READ, READ),
    LESS_THAN: (READ, READ, WRITE_TO),
    EQUALS: (READ, READ, WRITE_TO),
    HALT: (),
}


class IntCodeComputerVM:
    def __init__(self, program):
        self.__mem = program
        self.__ptr = 0
        self.__out = 0
        self.__input = self.__get_input()

        self.__OP = {
            ADD: self.__ADD,
            MULTIPLY: self.__MULTIPLY,
            INPUT: self.__INPUT,
            OUT: self.__OUT,
            JUMP_IF_TRUE: self.__JUMP_IF_TRUE,
            JUMP_IF_FALSE: self.__JUMP_IF_FALSE,
            LESS_THAN: self.__LESS_THAN,
            EQUALS: self.__EQUALS,
            HALT: self.__HALT
        }

    # Increments pointer
    def __read_instruction(self):
        modes_and_code = self.__mem[self.__ptr]
        modes, op_code = divmod(modes_and_code, 100)
        self.__ptr += 1
        return modes, op_code

    # Increments pointer
    def __read_val(self, mode, action):
        val = self.__mem[self.__ptr]
        self.__ptr += 1
        if action == READ:
            if mode == POSITION:
                val = self.__mem[val]
        elif action == WRITE_TO:
            assert mode == POSITION
        else:
            raise Exception(f"Invalid action {action}")
        return val

    def __get_args(self, modes, op):
        args = [None] * 3
        actions = ACTIONS[op]
        for i, action in enumerate(actions):
            modes, mode = divmod(modes, 10)
            args[i] = self.__read_val(mode, action)
        return args

    def __get_input(self):
        while True:
            yield int(input("Input: "))

    def __ADD(self, p1, p2, p3):
        self.__mem[p3] = p1 + p2

    def __MULTIPLY(self, p1, p2, p3):
        self.__mem[p3] = p1 * p2

    def __INPUT(self, p1, p2, p3):
        self.__mem[p1] = next(self.__input)

    def __OUT(self, p1, p2, p3):
        self.__out = p1
        return self.__out

    def __JUMP_IF_TRUE(self, p1, p2, p3):
        if p1 != 0:
            self.__ptr = p2

    def __JUMP_IF_FALSE(self, p1, p2, p3):
        if p1 == 0:
            self.__ptr = p2

    def __LESS_THAN(self, p1, p2, p3):
        self.__mem[p3] = 1 if p1 < p2 else 0

    def __EQUALS(self, p1, p2, p3):
        self.__mem[p3] = 1 if p1 == p2 else 0

    def __HALT(self, p1, p2, p3):
        return 1

    def run(self, *input_params):
        if input_params:
            self.__input = (n for n in input_params)
        while True:
            modes, op = self.__read_instruction()
            args = self.__get_args(modes, op)
            if self.__OP[op](*args):
                return self.__out


def read_file(path):
    with open(path) as input:
        return [int(n) for n in input.readline().split(',')]


def part1():
    program = read_file('2019/input/day_5')
    vm = IntCodeComputerVM(program)
    return vm.run(1)


def part2():
    program = read_file('2019/input/day_5')
    vm = IntCodeComputerVM(program)
    return vm.run(5)


if __name__ == '__main__':
    print('Part 1:', part1())
    print('Part 2:', part2())
