from shutil import move
from tabnanny import check
from functools import reduce
from copy import deepcopy

def copy(board):
    cp = Board(board.get_N())
    cp.board = deepcopy(board.board)
    return cp

class Board:
    def __init__(self, n):
        self.n = n
        self.board = [[0 for _ in range(n)] for _ in range(n)]
        self.winner = 0

    def __str__(self):
        n = self.get_N()
        output = self.line(n) + "\n"
        rows = ""
        cell = ""
        for i in range(0, n):
            rows = "|"
            for j in range(0, n):
                match self.get_Value(i,j):
                    case 1:
                        cell = " X "
                    case -1:
                        cell = " O "
                    case _:
                        cell = "   "

                rows += cell + "|"
            rows += "\n" + self.line(n) + "\n"
            output += rows
        
        output += "\n"

        return output


    def line(self, n):
        return ('-' * ((4*n) + 1))

    def get_N(self):
        return self.n

    def get_Winner(self):
        return self.winner

    def get_Value(self, row, col):
        return self.board[row][col]

    def set_Value(self, row, col, player):
        self.board[row][col] = player
        return self

    def is_Empty(self, row, col):
        if(self.get_Value(row, col) == 0):
            return True
        return False

    def moves(self):
        n = self.get_N()
        move_list = []
        for i in range(0, n):
            for j in range(0, n):
                if(self.board[i][j] == 0):
                    move_list.append((i,j))
        
        return move_list

    def check_Horz(self):
        check = 0
        n = self.get_N()
        for i in range (0, n):
            check = 0
            for j in range(0, n):
                check += self.get_Value(i, j)
            
            if(check == n or check == (-1) * n):
                self.winner = check/n
                return True
         
        return False
        
    def check_Vert(self):
        check = 0
        n = self.get_N()
        for i in range (0, n):
            check = 0
            for j in range(0, n):
                check += self.get_Value(j, i)
            
            if(check == n or check == (-1) * n):
                self.winner = check/n
                return True
         
        return False

    def check_Diag(self, reverse):
        check = 0
        n = self.get_N()

        if(reverse):
            for i,j in enumerate(range(n)):
                check += self.get_Value(i,j)
        else:
            for i,j in enumerate(range(n-1, -1, -1)):
                check += self.get_Value(i,j)

        if(check == n or check == (-1) * n):
                self.winner = check/n
                return True

            
        return False

    def check_Tie(self):
        n = self.get_N()
        for i in range(0, n):
            for j in range(0, n):
                if(self.get_Value(i,j) == 0):
                    return False
        return True
    
    def check_Win(self):
        if(self.check_Horz() or self.check_Vert() or self.check_Diag(True) or self.check_Diag(False) or self.check_Tie()):
            return True
        else:
            return False

class Tree:
    def __init__(self, board, player):
        self.board = board
        self.nodes = reduce(lambda x, move: x.append(copy(board).set_Value(move[0], move[1],player)), board.moves(), [])
        map(lambda x: Tree)

    