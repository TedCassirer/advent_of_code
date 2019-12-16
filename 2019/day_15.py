from IntCodeComputer import IntCodeComputerVM, manual_input
from queue import deque
from time import sleep

class Directions:
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4

    OPPOSITE = {
        NORTH: SOUTH,
        SOUTH: NORTH,
        EAST: WEST,
        WEST: EAST
    }

MOVE = {
    Directions.NORTH: lambda p: (p[0]-1, p[1]),
    Directions.SOUTH: lambda p: (p[0]+1, p[1]),
    Directions.WEST: lambda p: (p[0], p[1]-1),
    Directions.EAST: lambda p: (p[0], p[1]+1),
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
        WALL: '░',
        EMPTY: '▓',
        OXYGEN_TANK: 'O',
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
                
    def __str__(self):
        return TileType.TILE_STRING[self.type]
    
    def __repr__(self):
        return TileType.TILE_STRING[self.type]

class RoboBoy:
    def __init__(self, robo):
        self.robo = robo
        self.robo.input_provided_from(self.choose_direction())
        self.pos = (0, 0)
        self.grid = {self.pos: Tile(self.pos, TileType.EMPTY)}
        self.oxygen_pos = None
        self.last_dir = None

    
    def print_grid(self, delay=0.005):
        sleep(delay)
        min_x = min(x for y, x in self.grid.keys())
        min_y = min(y for y, x in self.grid.keys())
        max_x = max(x for y, x in self.grid.keys())
        max_y = max(y for y, x in self.grid.keys())

        string_grid = [[' '] * (max_x - min_x+1) for _ in range(max_y - min_y+1)]

        for pos, tile in self.grid.items():
            y = pos[0] - min_y
            x = pos[1] - min_x
            string_grid[y][x] = str(tile)
        
        ry, rx = self.pos[0] - min_y, self.pos[1] - min_x
        sy, sx = 0 - min_y, 0 - min_x
        string_grid[ry][rx] = '@'
        string_grid[sy][sx] = 'X'
        
        rows = []
        for row in string_grid:
            rows.append(''.join(row))
        
        rows.append(('\n'*(40 - (max_y - min_y))))
        rows.append(('\n\n------\n\n'))

        print('\n'.join(rows))

    
    def bff_search_for_tile(self, start, tile_matcher):
        queue = deque(((self.grid[start], []),))
        visited = set()
        while queue:
            tile, path = queue.popleft()
            visited.add(tile)
            if tile_matcher(tile):
                return path
            if tile.type == TileType.WALL:
                continue
            for dir, tile_connection in tile.connections.items():
                if tile_connection in visited:
                    continue
                queue.append((tile_connection, path + [dir]))
        print(len(path))
    
    def spread_oxygen(self, tiles, minutes=0):
        if not tiles:
            return minutes - 1
        next_tiles = set()
        for tile in tiles:
            for dir, tile_connection in tile.connections.items():
                if tile_connection.type == TileType.WALL or tile_connection.type == TileType.OXYGEN_TANK:
                    continue
                tile_connection.type = TileType.OXYGEN_TANK
                next_tiles.add(tile_connection)
        self.print_grid(0.05)
        return self.spread_oxygen(next_tiles, minutes+1)
        

    def choose_direction(self):
        while True:
            path = self.bff_search_for_tile(self.pos, lambda tile: tile == None)
            if not path:
                return
            for d in path:
                self.last_dir = d
                yield d

    def gogo_robo_boy(self):
        for status_code in self.robo.run():
            position_moved_to = MOVE[self.last_dir](self.pos)
            current_tile = self.grid[self.pos]
            if status_code == StatusCode.WALL:
                wall_tile = self.grid.get(position_moved_to)
                if not wall_tile:
                    wall_tile = Tile(position_moved_to, TileType.WALL)
                    self.grid[position_moved_to] = wall_tile
                current_tile.connections[self.last_dir] = wall_tile
            elif status_code == StatusCode.MOVED:
                self.pos = position_moved_to
                next_tile = self.grid.get(position_moved_to)
                if not next_tile:
                    next_tile = Tile(position_moved_to, TileType.EMPTY)
                    self.grid[position_moved_to] = next_tile
                current_tile.connections[self.last_dir] = next_tile
                next_tile.connections[Directions.OPPOSITE[self.last_dir]] = current_tile
            elif status_code == StatusCode.OXYGEN_TANK:
                self.oxygen_pos = position_moved_to
                self.pos = position_moved_to
                next_tile = self.grid.get(position_moved_to)
                if not next_tile:
                    next_tile = Tile(position_moved_to, TileType.OXYGEN_TANK)
                    self.grid[position_moved_to] = next_tile
                current_tile.connections[self.last_dir] = next_tile
                next_tile.connections[Directions.OPPOSITE[self.last_dir]] = current_tile
            self.print_grid()

    
def read_file():
    with open('2019/input/day_15') as input:
        return [int(n) for n in input.readline().split(',')]
        
def part1():
    robo = IntCodeComputerVM(read_file())
    boy = RoboBoy(robo)
    boy.gogo_robo_boy()
    return len(boy.bff_search_for_tile((0, 0), lambda tile: tile.type == TileType.OXYGEN_TANK))

def part2():
    robo = IntCodeComputerVM(read_file())
    boy = RoboBoy(robo)
    boy.gogo_robo_boy()


    return boy.spread_oxygen({boy.grid[boy.oxygen_pos]})

if __name__ == '__main__':
    #print('Part 1:', part1())
    print('Part 2:', part2())
