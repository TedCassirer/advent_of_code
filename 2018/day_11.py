from utils import readData, timeIt

class FuelGrid:
    def __init__(self, serialId, rows, columns):
        self.serialId = serialId
        self.rows = rows
        self.columns = columns
        self.fuelCells = self._generateFuelCells()

    def _generateFuelCells(self):
        fuelCells = []
        for y in range(1, self.rows+1):
            row = []
            for x in range(1, self.columns+1):
                rackId = x + 10
                powerLevel = y * rackId
                powerLevel += self.serialId
                powerLevel *= rackId
                powerLevel %= 1000
                powerLevel //= 100
                powerLevel -= 5
                row.append(powerLevel)
            fuelCells.append(row)
        return fuelCells

    def getMaxSquare(self, size):
        best = (-1<<63, None, None, None)
        reduced = []
        for row in self.fuelCells:
            windowSum = sum(row[:size])
            reducedRow = [windowSum]
            for i in range(1, self.columns-size):
                windowSum += row[i+size-1] - row[i-1]
                reducedRow.append(windowSum)
            reduced.append(reducedRow)
        for ci in range(self.columns-size):
            windowSum = sum(reduced[i][ci] for i in range(size))
            best = max(best, (windowSum, ci+1, 1, size))
            for ri in range(1, self.rows-size):
                windowSum += reduced[ri+size-1][ci] - reduced[ri-1][ci]
                best = max(best, (windowSum, ci+1, ri+1, size))

        return best
            


@timeIt
def part1():
    serialId = int(next(readData('2018/data/day_11')))
    grid = FuelGrid(serialId, 300, 300)
    #[print(row) for row in grid.fuelCells]
    return grid.getMaxSquare(3)

@timeIt
def part2():
    serialId = int(next(readData('2018/data/day_11')))
    grid = FuelGrid(serialId, 300, 300)
    #[print(row) for row in grid.fuelCells]
    best = (0,0,0)
    for size in range(1, 301):
        best = max(best, grid.getMaxSquare(size))
    return best

if __name__ == '__main__':
    print('Part 1:', part1())
    print('Part 2:', part2())
