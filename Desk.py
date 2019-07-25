from checker import *


colors = ['white', 'black']
points = {'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7}

class Desk():
    def __init__(self):
        self.board = [[BlankSpace(row, coll) for coll in range(8)] for row in range(8)]
        for row in range(8):

            for coll in range(8):
                if (row+coll)%2 == 0 and row not in [3,4]:
                    side = colors[0] if row<3 else colors[1]
                    self.board[row][coll] = Checker(row, coll, side=side)


        self.checkersCount = {}
        self.checkersCount[colors[0]] = 12
        self.checkersCount[colors[1]] = 12

    def turnToCode(self, point):
        return self.board[points[point[0]]][int(point[1])-1]

    def codeToturn(self, x, y):
        return str(list(points.keys())[list(points.values()).index(y)]) + str(x)

    def possibleMoves(self, side, posFrom, beatOnlyMode=False):
        moves = {}
        mul = 1 if side == colors[0] else -1
        for direction in [(x*mul, y*mul) for x,y in [(1,1), (1,-1)]]:
            moves[direction] = self.findMovesInDirection(side, posFrom, direction, beatOnlyMode)
        for direction in [(x*mul, y*mul) for x,y in [(-1,-1), (-1,1)]]:
            moves[direction] = self.findMovesInDirection(side, posFrom, direction, beatOnlyMode=True)
        return moves

    def findMovesInDirection(self, side, posFrom, direction, beatOnlyMode=False):
        checker = self.turnToCode(posFrom)
        moves = list()
        enemy_count = 0
        enemy_x = None
        enemy_y = None
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
        return {'moves': moves, 'enemies': (enemy_x, enemy_y)}




    def makeMove(self, side, posFrom, posTo, beatOnlyMode):     #not the best solution, mb change later
        departure = self.turnToCode(posFrom)
        destination = self.turnToCode(posTo)
        direction = zip((destination.x - departure.x)/abs(destination.x - departure.y),
                        (destination.y - departure.y)/abs(destination.y - departure.y))
        if isinstance(departure, Checker) and departure.color == side:
            moveData = self.possibleMoves(side, posFrom, beatOnlyMode=beatOnlyMode)
            if not (departure.x, departure.y) in moveData[direction]['moves']:
                return False

        tempX, tempY = departure.x, departure.y
        departure.x = destination.x
        departure.y = destination.y
        self.board[destination.x][destination.y] = departure
        self.board[tempX][tempY] = BlankSpace(tempX, tempY)
        en_x, en_y = moveData[direction]['enemies']
        if en_x:
            self.board[en_x][en_y] = BlankSpace(en_x, en_y)
            self.checkersCount[abs(colors.index(side)-1)] -= 1
        return True




    def turn(self, side):
        while True:
            posFrom, posTo =  input("Input your turn").split('-')

            if self.makeMove(side, posFrom, posTo):
                break
            else:
                print(r'You\'ve entered wrong move, try again')
        temp = self.possibleMoves(side, posFrom, beatOnlyMode=True)
        while True:
            for direaction in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                if len(temp[direaction]['moves'])>0:
                    posFrom = posTo
                    while True:
                        posTo = input("Beat enemy checker")
                        if self.makeMove(side, posFrom, posTo, beatOnlyMode=True):
                            break
                        else:
                            print(r'You\'ve entered wrong move, try again')
                    break
            else:
                break


if __name__ == '__main__':
    bord = Desk()
    a = bord.board[2][1]
    b = bord.turnToCode('C2')
    if (a.x, a.y) != (b.x, b.y):
        print('Bug #1')
    a = bord.possibleMoves(colors[0], 'C3')
    print(a)
