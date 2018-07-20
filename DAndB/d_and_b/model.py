# -*- coding: UTF-8 -*-
from enum import Enum
from datetime import datetime


RED = 1
BLUE = -1


class DBException(Exception):
    def __init__(self, *args, **kwargs):
        super(DBException, self).__init__(args, kwargs)
        if (len(args[0]) > 0):
            self.info = args[0][0]

# 棋盘类
class Board:
    def __init__(self):
                       #  0   1   2   3   4   5   6   7   8   9  10
        self._pieces = [[-1,  0, -1,  0, -1,  0, -1,  0, -1,  0, -1],  # 0
                        [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],  # 1
                        [-1,  0, -1,  0, -1,  0, -1,  0, -1,  0, -1],  # 2
                        [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],  # 3
                        [-1,  0, -1,  0, -1,  0, -1,  0, -1,  0, -1],  # 4
                        [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],  # 5
                        [-1,  0, -1,  0, -1,  0, -1,  0, -1,  0, -1],  # 6
                        [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],  # 7
                        [-1,  0, -1,  0, -1,  0, -1,  0, -1,  0, -1],  # 8
                        [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],  # 9
                        [-1,  0, -1,  0, -1,  0, -1,  0, -1,  0, -1]]  #10

    @property
    def pieces(self):
        return self._pieces.copy()

    def set_piece(self, x, y):
        if (self._pieces[x][y] != 0):  # 如果已有棋子则抛出异常
            raise BoardError("Cannot set piece")

        self._pieces[x][y] = 1

    def set_box(self, coordinate):
        x = coordinate[0]
        y = coordinate[1]

        if (self._pieces[x][y] != 0):  # 如果格子已被占领则抛出异常
            raise BoardError("Cannot set box")

        self._pieces[x][y] = 2

    def unset_piece(self, x, y):
        if (self._pieces[x][y] == 0):  # 如果没有棋子则抛出异常
            raise BoardError("Cannot unset piece")

        self._pieces[x][y] = 0

    def unset_box(self, coordinate):
        x = coordinate[0]
        y = coordinate[1]

        if (self._pieces[x][y] == 0):  # 如果格子未被占领则抛出异常
            raise BoardError("Cannot unset box")

        self._pieces[x][y] = 0

    #根据当前棋谱获得可下坐标
    def get_moves(self):
        lis = []
        for i in range(len(self.pieces)):
            if i % 2 == 0:
                for j in (1, 3, 5, 7, 9):
                    if self.pieces[i][j] == 0:
                        x = 'abcdef'[int((j - 1) / 2)]
                        y = int(6 - i / 2)
                        str1 = x + str(y) + 'h'
                        lis.append(str1)
            else:
                for j in (0, 2, 4, 6, 8, 10):
                    if self.pieces[i][j] == 0:
                        x = 'abcdef'[int(j / 2)]
                        y = int(6 - (i + 1) / 2)
                        str1 = x + str(y) + 'v'
                        lis.append(str1)
        return lis




class BoardError(DBException):
    def __init__(self, *args, **kwargs):
        super(BoardError, self).__init__(args, kwargs)


class PieceHistory():
    def __init__(self):
        self._list = []

    @property
    def list(self):
        return self._list.copy()

    @property
    def len(self):
        return len(self._list)

    def add(self, coordinate, color):
        self._list.append([coordinate, color])

    def delete(self):
        return self._list.pop()

