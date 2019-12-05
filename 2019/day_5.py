POSITION=0
IMMEDIATE=1

READ = 0
WRITE = 1

ADD=1 
MUL=2 
INP=3 
OUT=4 
JPT=5 
JPF=6 
LST=7 
EQL=8 
HLT=99

ACTIONS = {
    ADD : (READ, READ, WRITE),
    MUL : (READ, READ, WRITE),
    INP : (WRITE,),
    OUT : (READ,),
    JPT : (READ, READ),
    JPF : (READ, READ),
    LST : (READ, READ, WRITE),
    EQL : (READ, READ, WRITE),
    HLT : (),
}
class IntCodeComputerVM:
    def __init__(self, program):
        self.mem = program
        self.pointer = 0

    # Increments pointer
    def __read_instruction(self):
        types_and_code = self.mem[self.pointer]
        types, op_code = divmod(types_and_code, 100)
        self.pointer += 1
        return types, op_code

    # Increments pointer
    def __read_val(self, type, action):
        val = self.mem[self.pointer]
        self.pointer += 1
        if action == READ:
            if type == POSITION:
                val = self.mem[val]
        elif action == WRITE:
            assert type == POSITION
        else:
            raise Exception(f"Invalid action {action}")
        return val

    def __get_args(self, types, op):
        args = [None] * 4
        actions = ACTIONS[op]
        for i, action in enumerate(actions):
            types, type = divmod(types, 10)
            args[i] = self.__read_val(type, action)
        return args

    def run(self, input_param):
        out = 0
        while True:
            types, op = self.__read_instruction()
            p1, p2, p3, p4 = self.__get_args(types, op)
            if op == ADD:
                self.mem[p3] = p1 + p2
            elif op == MUL:
                self.mem[p3] = p1 * p2
            elif op == INP:
                self.mem[p1] = input_param
            elif op == OUT:
                out = p1
                if out != 0:
                    return out
            elif op == JPT:
                if p1 != 0:
                    self.pointer = p2
            elif op == JPF:
                if p1 == 0:
                    self.pointer = p2
            elif op == LST:
                self.mem[p3] = int(p1 < p2)
            elif op == EQL:
                self.mem[p3] = int(p1 == p2)
            elif op == HLT:
                return out
            else:
                raise Exception(f"Invalid OP {op}")

def get_input():
    with open('2019/input/day_5') as input:
        return [int(n) for n in input.readline().split(',')]

def part1():
    program = get_input()
    vm = IntCodeComputerVM(program)
    return vm.run(1)
    
def part2():
    program = get_input()
    vm = IntCodeComputerVM(program)
    return vm.run(5)

if __name__ == '__main__':
    print('Part 1:', part1())
    print('Part 2:', part2())