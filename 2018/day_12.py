from utils import readData, timeIt

def buildPropagationSet(padding):
    data = readData('2018/data/day_12')
    initialState = padding*'.' + next(data).split(' ')[2] + padding*'.'
    next(data)
    stateEmission = map(lambda s: s.split(' '), data)
    propagation = {state: emission for state, _, emission in stateEmission}
    return initialState, propagation

def getStateContexts(state, size=2):
    for i in range(size):
        yield '.'*(size-i) + state[:i+size+1]
    for i in range(size, len(state)-size):
        yield state[i-size:i+size+1]
    for i in range(size, 0, -1):
        yield state[-i-size:] + '.'*(size-i+1)

def propagate(state, propagation):
    return ''.join(map(lambda s: propagation.get(s, '.'), getStateContexts(state)))



@timeIt
def part1():
    padding = 25
    state, propagationSet = buildPropagationSet(padding)
    print(0, state)
    for i in range(1, 21):
        state = propagate(state, propagationSet)
        print(i, state)
    return sum(i-padding for i, flower in enumerate(state) if flower=='#')
@timeIt
def part2():
    padding = 2000
    state, propagationSet = buildPropagationSet(padding)
    print(0, state)
    for i in range(1, 50000000000):
        state = propagate(state, propagationSet)
        if i % 1000 == 0:
            print(sum(i-padding for i, flower in enumerate(state) if flower=='#'))
    print(state)
    return sum(i-padding for i, flower in enumerate(state) if flower=='#')

if __name__ == '__main__':
    print('Part 1:', part1())
    print('Part 2:', part2())
