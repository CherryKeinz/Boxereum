# -*- coding: UTF-8 -*-
import copy

from .model import *


class Game:
    def __init__(self, red_player, blue_player):
        if (not (red_player.color == Color.red and blue_player.color == Color.blue)):
            raise GameError("Invalid players", red_player, blue_player)

        self._red_player = red_player
        self._red_player._start_new_game()
        self._blue_player = blue_player
        self._blue_player._start_new_game()
        self._current_player = self._red_player
        self._piece_history = PieceHistory()
        self._board = Board()
        self._datetime = datetime.now()

    @property
    def board(self):
        return copy.deepcopy(self._board)

    @property
    def score(self):
        return (self._red_player.score, self._blue_player.score)

    @property
    def red_player(self):
        return self._red_player

    @property
    def blue_player(self):
        return self._blue_player

    @property
    def history(self):
        return self._piece_history.list

    @property
    def current_player_color(self):
        return self._current_player.color

    @property
    def is_end(self):
        if (self._red_player.score + self._blue_player.score == 25):
            return True
        else:
            return False

    @property
    def winner(self):
        if (self.is_end):
            if (self._red_player.score > self._blue_player.score):
                return Color.red
            else:
                return Color.blue
        else:
            return None

    @property
    def datetime(self):
        return self._datetime

    def copy(self):
        res = copy.deepcopy(self)
        return res

    #根据当前棋谱获得可下坐标
    def get_moves(self):
        lis = []
        for i in range(len(self.board.pieces)):
            if i % 2 == 0:
                for j in (1, 3, 5, 7, 9):
                    if self.board.pieces[i][j] == 0:
                        x = 'abcdef'[int((j - 1) / 2)]
                        y = int(6 - i / 2)
                        str1 = x + str(y) + 'h'
                        lis.append(str1)
            else:
                for j in (0, 2, 4, 6, 8, 10):
                    if self.board.pieces[i][j] == 0:
                        x = 'abcdef'[int(j / 2)]
                        y = int(6 - (i + 1) / 2)
                        str1 = x + str(y) + 'v'
                        lis.append(str1)
        return lis


    def move(self, piece):
        if (self.is_end):
            raise MoveError("Game is over")

        # if (piece.color != self.current_player_color):
        #     raise MoveError("Player color is wrong")

        self._board.set_piece(piece)

        x = piece.coordinate[0]
        y = piece.coordinate[1]
        score = 0  # 本次得分，用于记录这次落子得分数量
        if self._check_box((x, y-1)):  # 判断格坐标合法性的逻辑在_check_box()函数中
            score = score + 1
            self._board.set_box((x, y-1), (self._current_player.color, self._current_player.score + score))
        if self._check_box((x, y+1)):
            score = score + 1
            self._board.set_box((x, y+1), (self._current_player.color, self._current_player.score + score))
        if self._check_box((x-1, y)):
            score = score + 1
            self._board.set_box((x-1, y), (self._current_player.color, self._current_player.score + score))
        if self._check_box((x+1, y)):
            score = score + 1
            self._board.set_box((x+1, y), (self._current_player.color, self._current_player.score + score))
        if (score == 0):  # 如果没得分，就换玩家
            self._current_player = self._blue_player if (self._current_player.color == Color.red) else self._red_player
        else:
            self._current_player._score = self._current_player.score + score

        self._piece_history.add(piece)

    def transform_player(self):
        self._current_player = self._blue_player if (self._current_player.color == Color.red) else self._red_player

    def back(self):
        if (self._piece_history.len == 0):
            raise BackError()

        piece = self._piece_history.delete()

        x = piece.coordinate[0]
        y = piece.coordinate[1]
        score = 0  # 本次得分，用于记录这次落子得分数量
        if self._check_box((x, y-1)):  # 判断格坐标合法性的逻辑在_check_box()函数中
            self._board.unset_box((x, y-1))
            score = score + 1
        if self._check_box((x, y+1)):
            self._board.unset_box((x, y+1))
            score = score + 1
        if self._check_box((x-1, y)):
            self._board.unset_box((x-1, y))
            score = score + 1
        if self._check_box((x+1, y)):
            self._board.unset_box((x+1, y))
            score = score + 1
        if (score == 0):  # 如果没得分，就换玩家
            self._current_player = self._blue_player if (self._current_player.color == Color.red) else self._red_player
        else:
            self._current_player._score = self._current_player.score - score

        self._board.unset_piece(piece)

    def _check_box(self, box_coordinate):  # 判断格子是否封闭
        x = box_coordinate[0]
        y = box_coordinate[1]

        if (x < 0 or x > 10 or y < 0 or y > 10):  # 判断坐标是否越界，如果越界直接返回否
            return False
        if (self._board.pieces[x][y] == -1):  # 判断坐标是否为点，如果是点直接返回否
            return False

        if (self._board.pieces[x-1][y] == 0
            or self._board.pieces[x+1][y] == 0
            or self._board.pieces[x][y-1] == 0
            or self._board.pieces[x][y+1] == 0):
            return False

        return True


class GameError(DBException):
    def __init__(self, *args, **kwargs):
        super(GameError, self).__init__(args, kwargs)


class MoveError(GameError):
    def __init__(self, *args, **kwargs):
        super(MoveError, self).__init__(args, kwargs)


class BackError(GameError):
    def __init__(self, *args, **kwargs):
        super(BackError, self).__init__(args, kwargs)

