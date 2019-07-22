from checker import *


colors = ['black', 'white']
points = {'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7}

class Desk():
    def __init__(self):
        dc = lambda x,y: Checker(x, y) if (x + y) % 2 == 0 and y not in [3, 4] else None
        self.board = [[dc(row, coll) for row in range(8)] for coll in range(8)]
        self.whites = list()
        self.blacks = list()
       # for row in range(8):
           # for coll in range(row%2, 8 , 2):
                # self.whites.append(self.board[row][coll])
                # self.blacks.append(self.board[7-row][7-coll])
    def turnToCode(self, point):
        return self.board[points[point[0]]][int(point[1])]

    def codeToturn(self, x, y):
        return str(list(points.keys())[list(points.values()).index(y)]) + str(x)

    def possibleMoves(self, side, pos):
        moves = [[]]
        checker = self.turnToCode(pos)
        for direction in [(1, 1), (1, -1), (-1, -1), (-1, 1)]:
            temp = list()
            enemy_count = 0
            n = checker.area_of_affect+1
            for el in range(1, n):

                x = checker.x+direction[0]
                y = checker.y+direction[1]
                if 0<=x and x<8 and 0<=y and y<8:
                    if not isinstance(self.board[x][y], Checker):
                        temp.append((x, y))
                    else:
                        if (self.board[x][y]).colour != side:
                            enemy_count += 1
                            n = checker.area_of_affect+2
                        if enemy_count > 1:
                            break

            moves[0].append(enemy_count)
            moves.append(temp)

        for i in range(2,3):
            if moves[0][i] == 0:
                moves.pop(i+1)
            else:
                flag = False
                f = lambda t: t/abs(t)
                xs = moves[i+1][-1][0]
                y = moves[i+1][-1][1]
                for x in range(checker.x, xs, f(xs)):
                    if isinstance(self.board[x][y], Checker) and self.board[x][y].colour != side:
                        flag = True
                    y += f(y)
                if not flag:
                    moves.pop(i+1)
        moves.pop(0)
        return moves




    def checkTurn(self, side, posFrom, posTo):
        departure = self.turnToCode(posFrom)
        destination = self.turnToCode(posTo)
        if isinstance(departure, Checker) and departure.colour == side:
            for diagonal in self.possibleMoves(side, posFrom):
                if (points[posTo[0]], int(posTo[1])) in diagonal:
                    return True
            return False


    def turn(self, side):
        while True:
            posFrom, posTo =  input("Input your turn").split('-')
            if self.checkTurn(side, posFrom, posTo):
                break
            else:
                print(r'You\'ve entered wrong move, try again')


if __name__ == '__main__':
    bord = Desk()
    print(bord.possibleMoves('white', 'C2'))