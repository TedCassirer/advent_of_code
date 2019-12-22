from IntCodeComputer import IntCodeComputerVM, generator_of
from itertools import permutations

def read_file(path):
    with open(path) as input:
        return [int(n) for n in input.readline().split(',')]

def part1():
    program = read_file('2019/input/day_7')
    phase_setting_sequences = permutations((0,1,2,3,4))
    highest_output = 0
    for phase_settings in phase_setting_sequences:
        vms = []
        vms = [IntCodeComputerVM(program, phase) for phase in phase_settings]
        vms[0].input_provided_from(generator_of(0))
        for i in range(1, len(vms)):
            vms[i].input_provided_from(vms[i-1].run())
        highest_output = max(highest_output, next(vms[-1].run()))
    return highest_output

def part2():
    program = read_file('2019/input/day_7')
    phase_setting_sequences = permutations((5,6,7,8,9))
    highest_output = (0, None)
    for phase_settings in phase_setting_sequences:
        prev_vm = None
        vms = [IntCodeComputerVM(program, phase) for phase in phase_settings]
        for i in range(len(vms)):
            vms[i].input_provided_from(vms[i-1].run())
        
        list(vms[-1].run())
        highest_output = max(highest_output, (vms[-1].out, phase_settings))
    return highest_output[0]

if __name__ == '__main__':
    #print('Part 1:', part1())
    print('Part 2:', part2())