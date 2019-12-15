from IntCodeComputer import IntCodeComputerVM, manual_input

class Directions:
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4

    OPPOSITE_DIRECTION = {
        NORTH: SOUTH,
        SOUTH: NORTH,
        WEST: EAST,
        EAST: WEST,
    }

    MOVE = {
        NORTH: lambda p: (p[0]-1, p[1]),
        SOUTH: lambda p: (p[0]+1, p[1]),
        WEST: lambda p: (p[0], p[1]-1),
        EAST: lambda p: (p[0], p[1]+1),
    }

class StatusCode:
    WALL = 0
    MOVED = 1
    OXYGEN_TANK = 2

class TileType:
    WALL = 0
    EMPTY = 1
    OXYGEN_TANK = 2

    TILE_STRING = {
        WALL: '#',
        EMPTY: '.',
        OXYGEN_TANK: 'O'
    }

class Tile:
    def __init__(self, coord, type):
        self.connections = {
            Directions.NORTH: None,
            Directions.SOUTH: None,
            Directions.WEST: None,
            Directions.EAST: None
        }
        self.coord = coord
        self.type = type

    def get_direction(self):
        if not None in self.connections:
            return -1
        return self.connections.index(None) + 1
    
    def __str__(self):
        return TileType.TILE_STRING[self.type]

class RoboBoy:
    def __init__(self, robo):
        self.robo = robo
        self.robo.input_provided_from(self.choose_direction())
        self.start_tile = Tile()
        self.last_move = None
        self.oxygen_tile = None
        self.pos = (0, 0)
    
    def choose_direction(self):
        while True:
            self.last_move = self.current_tile.get_direction()
            yield self.last_move

    def gogo_robo_boy(self):
        for status_code in self.robo.run():
            


def read_file():
    with open('2019/input/day_15') as input:
        return [int(n) for n in input.readline().split(',')]

def traverse(robo):
    start_tile = Tile()
    current_tile = start_tile

def part1():
    robo = IntCodeComputerVM(read_file())
    boy = RoboBoy(robo)
    return boy.gogo_robo_boy()

def part2():
    pass

if __name__ == '__main__':
    print('Part 1:', part1())
    print('Part 2:', part2())
