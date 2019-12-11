from IntCodeComputer import IntCodeComputerVM
from collections import defaultdict

BLACK = 0
WHITE = 1

LEFT = 0
RIGHT = 1

class RoboWife:
    def __init__(self):
        self.dir = (-1, 0)
        self.pos = (0, 0)
    
    def move(self, direction):
        if direction == LEFT:
            self.dir = (-self.dir[1], self.dir[0])
        elif direction == RIGHT:
            self.dir = (self.dir[1], -self.dir[0])
        else:
            raise Exception(f"Unknown direction, {direction}")
        
        self.pos = (self.pos[0] + self.dir[0], self.pos[1] + self.dir[1])

        return self.pos

def read_program():
    with open('2019/input/day_11') as input:
        return [int(n) for n in input.readline().split(',')]

def print_grid(grid):
    NOT_PAINTED = 2
    x_min = min(x for y, x in grid.keys())
    y_min = min(y for y, x in grid.keys())
    
    x_max = max(x for y, x in grid.keys())
    y_max = max(y for y, x in grid.keys())

    offset_grid = {(k[0] - y_min, k[1] - x_min): v for k, v in grid.items()}
    canvas = [[offset_grid.get((y, x), NOT_PAINTED) for x in range(-1, x_max - x_min+2)] for y in range(-1, y_max - y_min+2)]
    def to_printable_image(image):
        symbols = {
            BLACK: '░',
            WHITE: '▓',
            NOT_PAINTED: 'X'
        }
        decoded_image = []
        for row in image:
            decoded_image.append(''.join([symbols[s] for s in row]))
        return '\n' + '\n'.join(decoded_image)
    canvas
    return to_printable_image(canvas)
def part1():
    grid = defaultdict(lambda: BLACK)
    robo = RoboWife()
    robo_brain = IntCodeComputerVM(read_program())
    def robo_input(robo, grid):
        while True:
            if robo.pos in grid:
                print('Yeet')
            yield grid[robo.pos]
    robo_brain.input_provided_from(robo_input(robo, grid))
    runner = robo_brain.run()
    for painted_color in runner:
        turn = next(runner)
        grid[robo.pos] = painted_color
        robo.move(turn)
        print(print_grid(grid))
    print(len(grid))
    return print_grid(grid)

def part2():
    pass

if __name__ == '__main__':
    print('Part 1:', part1())
    print('Part 2:', part2())
