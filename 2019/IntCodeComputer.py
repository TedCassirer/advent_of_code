from itertools import chain

POSITION = 0
IMMEDIATE = 1
RELATIVE = 2

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
SET_RELATIVE_BASE = 9
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
    SET_RELATIVE_BASE: (READ,),
    HALT: (),
}


def manual_input():
    while True:
        yield int(input("Input: "))


def generator_of(*args):
    for a in args:
        yield a

def empty():
    return
    yield 

class IntCodeComputerVM:
    def __init__(self, program, phase_setting=None):
        self.__mem = program[:]
        self.__ptr = 0
        self.out = None
        self.phase_setting = phase_setting
        self.__input = generator_of(phase_setting) if phase_setting else empty()
        self.halted = False
        self.__relative_base = 0

        self.__OP = {
            ADD: self.__ADD,
            MULTIPLY: self.__MULTIPLY,
            INPUT: self.__INPUT,
            OUT: self.__OUT,
            JUMP_IF_TRUE: self.__JUMP_IF_TRUE,
            JUMP_IF_FALSE: self.__JUMP_IF_FALSE,
            LESS_THAN: self.__LESS_THAN,
            EQUALS: self.__EQUALS,
            SET_RELATIVE_BASE: self.__SET_RELATIVE_BASE,
            HALT: self.__HALT
        }

    def __getitem__(self, i):
        assert i >= 0
        try:
            return self.__mem[i]
        except IndexError:
            self.__mem += [0]*(len(self.__mem))
            return self.__mem[i]

    def __setitem__(self, i, val):
        assert i >= 0
        try:
            self.__mem[i] = val
        except IndexError:
            self.__mem += [0]*(len(self.__mem))
            self.__mem[i] = val

    def __repr__(self):
        return str(self.phase_setting)

    def input_provided_from(self, int_supplier):
        self.__input = chain(self.__input, int_supplier)

    # Increments pointer
    def __read_instruction(self):
        modes_and_code = self[self.__ptr]
        modes, op_code = divmod(modes_and_code, 100)
        self.__ptr += 1
        return modes, op_code

    # Increments pointer
    def __read_val(self, mode, action):
        val = self[self.__ptr]
        self.__ptr += 1
        if action == READ:
            if mode == POSITION:
                val = self[val]
            elif mode == RELATIVE:
                val = self[val + self.__relative_base]
        elif action == WRITE_TO:
            assert mode != IMMEDIATE
            if mode == RELATIVE:
                val += self.__relative_base
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

    def __ADD(self, p1, p2, p3):
        self[p3] = p1 + p2

    def __MULTIPLY(self, p1, p2, p3):
        self[p3] = p1 * p2

    def __INPUT(self, p1, p2, p3):
        self[p1] = next(self.__input)

    def __OUT(self, p1, p2, p3):
        self.out = p1
        return self.out

    def __JUMP_IF_TRUE(self, p1, p2, p3):
        if p1 != 0:
            self.__ptr = p2

    def __JUMP_IF_FALSE(self, p1, p2, p3):
        if p1 == 0:
            self.__ptr = p2

    def __LESS_THAN(self, p1, p2, p3):
        self[p3] = 1 if p1 < p2 else 0

    def __EQUALS(self, p1, p2, p3):
        self[p3] = 1 if p1 == p2 else 0

    def __SET_RELATIVE_BASE(self, p1, p2, p3):
        self.__relative_base += p1

    def __HALT(self, p1, p2, p3):
        return self.out

    def run(self):
        while not self.halted:
            modes, op = self.__read_instruction()
            args = self.__get_args(modes, op)
            self.__OP[op](*args)
            if op == HALT:
                self.halted = True
            elif op == OUT:
                yield self.out
