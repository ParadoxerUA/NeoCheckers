from checker import *


colors = ['white', 'black']
points = {'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7}

class Desk():
    def __init__(self):
        self.board = list()
        for row in range(8):
            for coll in range(8):
                if (row+coll)%2 == 0 and coll not in [3,4]:
                    side = colors[0] if row<3 else colors[1]
                    self.board[row][coll] = Checker(x, y, side=side)


        dc = lambda x,y: Checker(x, y) if (x + y) % 2 == 0 and y not in [3, 4] else BlankSpace(x, y)
        self.board = [[dc(row, coll) for row in range(8)] for coll in range(8)]
        self.whites = list()
        self.blacks = list()
        for row in range(8):
            for coll in range(row%2, 8 , 2):
                 self.whites.append(self.board[row][coll])
                 self.blacks.append(self.board[7-row][7-coll])
    def turnToCode(self, point):
        return self.board[points[point[0]]][int(point[1])]

    def codeToturn(self, x, y):
        return str(list(points.keys())[list(points.values()).index(y)]) + str(x)

    def possibleMoves(self, side, posFrom, beatOnlyMode=False):
        moves = {}
        mul = 1 if side == colors[0] else -1
        for direction in [(x*mul, y*mul) for x,y in [(1,1), (-1,1)]]:
            moves[direction] = self.findMovesInDirection(side, posFrom, direction, beatOnlyMode)
        for direction in [(x*mul, y*mul) for x,y in [(-1,-1), (1,-1)]]:
            moves[direction] = self.findMovesInDirection(side, posFrom, direction, beatOnlyMode=True)
        return moves

    def findMovesInDirection(self, side, posFrom, direction, beatOnlyMode=False):
        checker = self.turnToCode(posFrom)
        moves = list()
        enemy_count = 0
        n = checker.area_of_affect + 1
        for el in range(1, n):

            x = checker.x + direction[0]
            y = checker.y + direction[1]
            if 0 <= x and x < 8 and 0 <= y and y < 8:
                if not isinstance(self.board[x][y], Checker):
                    moves.append((x, y))
                else:
                    if (self.board[x][y]).color != side:
                        enemy_count += 1
                        enemy_x = x
                        enemy_y = y
                        n = checker.area_of_affect + 2
                    if enemy_count > 1:
                        break
        if beatOnlyMode and len(moves)>0:
            if enemy_count == 0:
                moves.clear()
            elif enemy_x*direction[0] > moves[-1][0]*direction[1] \
                or enemy_y*direction[1] > moves[-1][0]*direction[1]:
                moves.clear()
        return {'moves':moves, 'enemyies':(enemy_x, enemy_y)}




    def checkTurn(self, side, posFrom, posTo, beatOnlyMode):
        departure = self.turnToCode(posFrom)
        destination = self.turnToCode(posTo)
        direction = zip((destination.x - departure.x)/abs(destination.x - departure.y),
                        (destination.y - departure.y)/abs(destination.y - departure.y))
        if isinstance(departure, Checker) and departure.color == side:
            if (departure.x, departure.y) in self.possibleMoves(side, posFrom, beatOnlyMode=beatOnlyMode)[direction]['moves']:
                    return True
        return False

    def rearrange(self, posFrom, posTo):
        previousPos = self.turnToCode(posFrom)
        nextPos = self.turnToCode(posTo)
        tempX, tempY = previousPos.x, previousPos.y
        previousPos.x = nextPos.x
        previousPos.y = nextPos.y
        self.board[nextPos.x][nextPos.y] = previousPos
        self.board[tempX][tempY] = BlankSpace(tempX, tempY)

    def turn(self, side):
        while True:
            posFrom, posTo =  input("Input your turn").split('-')
            if self.checkTurn(side, posFrom, posTo):
                break
            else:
                print(r'You\'ve entered wrong move, try again')
        self.rearrange(posFrom, posTo)
        temp = self.possibleMoves(side, posFrom, beatOnlyMode=True)
        while True:
            for direaction in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                if len(temp[direaction]['moves'])>0:
                    posFrom = posTo
                    while True:
                        posTo = input("Beat enemy checker")
                        if self.checkTurn(side, posFrom, posTo, beatOnlyMode=True):
                            break
                        else:
                            print(r'You\'ve entered wrong move, try again')
                    self.rearrenge(posFrom, posTo)
                    break
            else:
                break


if __name__ == '__main__':
    bord = Desk()
    print(bord.possibleMoves('white', 'C2'))