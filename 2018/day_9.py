from utils import readData, timeIt

class LinkedNode:

    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None
    
    def remove(self):
        prev = self.prev
        self.prev.next = self.next
        self.next.prev = prev
    
    def insertAfter(self, node):
        node.prev = self
        node.next = self.next
        self.next.prev = node
        self.next = node

    def __repr__(self):
        return str(self.value)


class GameBoard:

    def __init__(self):
        self.currentMarble = LinkedNode(0)
        self.currentMarble.next = self.currentMarble
        self.currentMarble.prev = self.currentMarble
        self.head = self.currentMarble
        
    def placeMarble(self, value):
        if value % 23 == 0:
            for _ in range(6):
                self.currentMarble = self.currentMarble.prev
            score = value + self.currentMarble.prev.value
            self.currentMarble.prev.remove()
        else:
            newMarble = LinkedNode(value)
            self.currentMarble.next.insertAfter(newMarble)
            self.currentMarble = newMarble
            score = 0
        return score

    def __repr__(self):
        current = self.head
        res = []
        while current.next != self.head:
            res.append(current.value)
            current = current.next
        res.append(current.value)
        return str(self.currentMarble.value) + ' | ' + str(res)


@timeIt
def part1():
    line = next(readData('2018/data/day_9')).split(' ')
    playerCount, lastMarble = int(line[0]), int(line[-2])
    players = [0]*playerCount
    currentMarble = 1
    board = GameBoard()
    while currentMarble <= lastMarble:
        for pi in range(playerCount):
            players[pi] += board.placeMarble(currentMarble)
            currentMarble += 1
            if currentMarble > lastMarble:
                break
    return max(players)


@timeIt
def part2():
    line = next(readData('2018/data/day_9')).split(' ')
    playerCount, lastMarble = int(line[0]), int(line[-2])
    lastMarble *= 100
    players = [0]*playerCount
    currentMarble = 1
    board = GameBoard()
    while currentMarble <= lastMarble:
        for pi in range(playerCount):
            players[pi] += board.placeMarble(currentMarble)
            currentMarble += 1
            if currentMarble > lastMarble:
                break
    return max(players)


if __name__ == '__main__':
    print('Part 1:', part1())
    print('Part 2:', part2())
