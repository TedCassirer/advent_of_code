def get_input():
    with open('2019/input/day_5') as input:
        return [int(n) for n in input.readline().split(',')]

def get_value(parameter, mode, memory):
    assert mode == 0 or mode == 1
    if mode == 1:
        return parameter
    else:
        return memory[parameter]

def parse_instructions(instruction):
    rest, op_code = divmod(instruction, 100)
    rest, pm1 = divmod(rest, 10)
    rest, pm2 = divmod(rest, 10)
    rest, pm3 = divmod(rest, 10)
    return (op_code, pm1, pm2, pm3)

def process_program(memory, input_value):
    output = 0
    i = 0
    op_code, *parameter_modes = parse_instructions(memory[i])
    while op_code != 99:
        if op_code == 1:
            n1 = get_value(memory[i+1], parameter_modes[0], memory)
            n2 = get_value(memory[i+2], parameter_modes[1], memory)
            write_loc = memory[i+3]
            memory[write_loc] = n1 + n2
            i += 4
        elif op_code == 2:
            n1 = get_value(memory[i+1], parameter_modes[0], memory)
            n2 = get_value(memory[i+2], parameter_modes[1], memory)
            write_loc = memory[i+3]
            memory[write_loc] = n1 * n2
            i += 4
        elif op_code == 3:
            write_loc = memory[i+1]
            memory[write_loc] = input_value
            i += 2
        elif op_code == 4:
            output = get_value(memory[i+1], parameter_modes[0], memory)
            if output != 0:
                return output
            i += 2
        elif op_code == 5:
            n1 = get_value(memory[i+1], parameter_modes[0], memory)
            n2 = get_value(memory[i+2], parameter_modes[1], memory)
            if n1 != 0:
                i = n2
            else:
                i += 3
        elif op_code == 6:
            n1 = get_value(memory[i+1], parameter_modes[0], memory)
            n2 = get_value(memory[i+2], parameter_modes[1], memory)
            if n1 == 0:
                i = n2
            else:
                i += 3
        elif op_code == 7:
            n1 = get_value(memory[i+1], parameter_modes[0], memory)
            n2 = get_value(memory[i+2], parameter_modes[1], memory)
            write_loc = memory[i+3]
            memory[write_loc] = n1 < n2
            i += 4
        elif op_code == 8:
            n1 = get_value(memory[i+1], parameter_modes[0], memory)
            n2 = get_value(memory[i+2], parameter_modes[1], memory)
            write_loc = memory[i+3]
            memory[write_loc] = n1 == n2
            i += 4
        else:
            raise Exception(f"Invalid op_code: {op_code}")
        op_code, *parameter_modes = parse_instructions(memory[i])      
    assert(op_code == 0)
    return op_code

def part1():
    memory = get_input()
    return process_program(memory, input_value=1)
    
def part2():
    memory = get_input()
    return process_program(memory, input_value=5)

if __name__ == '__main__':
    print('Part 1:', part1())
    print('Part 2:', part2())