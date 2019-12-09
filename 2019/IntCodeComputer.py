from itertools import chain

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


def manual_input():
    while True:
        yield int(input("Input: "))

def generator_of(*args):
    for a in args:
        yield a

class IntCodeComputerVM:
    def __init__(self, program, phase_setting):
        self.__mem = program[:]
        self.__ptr = 0
        self.out = None
        self.phase_setting = phase_setting
        self.__input = generator_of(phase_setting)
        self.halted = False

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
    
    def __repr__(self):
        return str(self.phase_setting)

    def connect_with(self, int_supplier):
        if type(int_supplier) == IntCodeComputerVM:
            def get_output():
                while not int_supplier.halted:
                    yield int_supplier.run()
            self.__input = chain(self.__input, get_output())
        else:
            self.__input = chain(self.__input, int_supplier)

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

    def __ADD(self, p1, p2, p3):
        self.__mem[p3] = p1 + p2

    def __MULTIPLY(self, p1, p2, p3):
        self.__mem[p3] = p1 * p2

    def __INPUT(self, p1, p2, p3):
        self.__mem[p1] = next(self.__input)

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
        self.__mem[p3] = 1 if p1 < p2 else 0

    def __EQUALS(self, p1, p2, p3):
        self.__mem[p3] = 1 if p1 == p2 else 0

    def __HALT(self, p1, p2, p3):
        return self.out

    def run(self):
        while not self.halted:
            modes, op = self.__read_instruction()
            args = self.__get_args(modes, op)
            self.__OP[op](*args)
            if op == HALT:
                self.halted = True
                return self.out
            if op == OUT:
                return self.out
