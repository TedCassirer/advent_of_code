import time
class Grid:
    def __init__(self, board):
        self.board = board

    def tick(self):
        newBoard = []

        for y in range(len(self.board)):
            row = ''
            for x in range(len(self.board[y])):
                score = sum(self.get(ay, ax)=='#' for ay, ax in self.adjacent(y, x))
                if self.get(y, x) == '#':
                    row += '#' if int(score == 1) else '.'
                else:
                    row += '#' if int(1 <= score <= 2) else '.'

            newBoard.append(row)
        return Grid(newBoard)

    def get(self, y, x):
        return self.board[y][x]

    def adjacent(self, y, x):
        if y > 0:
            yield (y-1, x)
        if y < len(self.board)-1:
            yield (y+1, x)
        if x > 0:
            yield (y, x-1)
        if x < len(self.board[y])-1:
            yield (y, x+1)

    def biodiversity(self):
        points = 0
        index = 0
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.get(y, x) == '#':
                    points += 2**index
                index += 1
                
        return points

    def __repr__(self):
        return '\n'.join(map(str, self.board)) + '\n' + str(self.biodiversity()) + '\n'

def parse(input):
    board = []
    for line in input.strip().split('\n'):
        board.append(line)
    return Grid(board)

input = '''
.###.
..#.#
...##
#.###
..#..
'''
grid = parse(input)
seen = {grid.biodiversity()}
for _ in range(100):
    grid = grid.tick()
    points = grid.biodiversity()
    if points in seen:
        print(_)
        print(points)
        break
    seen.add(points)


