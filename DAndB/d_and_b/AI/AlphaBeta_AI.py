# -*- coding: UTF-8 -*-
import random
import time
from math import sqrt, log

from ..player import AIPlayer
from ..model import *

class Pair:
    def __init__(self, move, value):
        self._move = move
        self._value = value

    @property
    def move(self):
        return self._move

    @property
    def value(self):
        return self._value

    def set_move(self, move):
        self._move = move

    def set_value(self, value):
        self._value = value

class AlphaBetaAI(AIPlayer):
    def __init__(self, color, name):
        super(AlphaBetaAI, self).__init__(color, name)
        self.MIN = -float('inf')
        self.MAX = float('inf')
        self.cScore = 20
        self.cThree = 15
        self.cTwo = 1
        self.maxLevel = None
        self.moveTime = None
        self.startTime = None

    def heuristic(self, game_state):
        red_score = game_state.score[0]
        blue_score = game_state.score[1]
        if self.color == RED:
            value = self.cScore * red_score - self.cScore * blue_score
        else:
            value = self.cScore * blue_score - self.cScore * red_score
        if self.color == game_state.current_player_color:
            value += self.cThree * game_state.get_box_count(3) - self.cTwo * game_state.get_box_count(2)
        else:
            value -= self.cThree * game_state.get_box_count(3) - self.cTwo * game_state.get_box_count(2)
        return value

    def getNextMove(self, game_state, during_time):
        self.startTime = time.time()
        referenceColor = self.color
        self.maxLevel = 5
        self.moveTime = during_time
        # while self.maxLevel <= len(game_state.get_moves()):
        #     pair = self.dfs(game_state, referenceColor, self.MIN, self.MAX, 0)
        #     if (time.time() - self.startTime) < during_time:
        #         move = pair.move
        #     else:
        #         break
        #     self.maxLevel += 1
        move = self.dfs(game_state, referenceColor, self.MIN, self.MAX, 0).move
        return move

    def dfs(self, game_state, color, a, b, level):
        if level < self.maxLevel and (time.time() - self.startTime) < self.moveTime:
            moves = game_state.get_moves()
            moves_num = len(moves)

            if moves_num == 0:
                return Pair(None, self.heuristic(game_state))

            random.shuffle(moves)

            neighbours = []
            for i in range(moves_num):
                new_state = game_state.copy()
                new_state.move(moves[i], color)
                neighbours.append(Pair(moves[i], self.heuristic(new_state)))
            neighbours.sort(key=lambda x: x.value, reverse=False)
            # for i in neighbours:
            #     print(i.move, i.value)
            moves = []
            if self.color == game_state.current_player_color:
                for i in neighbours[::-1]:
                    moves.append(i.move)
            else:
                for i in neighbours:
                    moves.append(i.move)
            # print(moves)
            if self.color == game_state.current_player_color:
                new_pair = Pair(None, self.MIN)
                for move in moves:
                    child = game_state.copy()
                    child.move(move, child.current_player_color)
                    child_score = child.score[0] if game_state.current_player_color == RED else child.score[1]
                    current_score = game_state.score[0] if game_state.current_player_color == RED else game_state.score[1]
                    flag = False
                    if child_score == current_score:
                        pair = self.dfs(child, child.current_player_color, a, b, level+1)
                        flag = True
                    else:
                        pair = self.dfs(child, child.current_player_color, a, b, level+1)
                    child_value = pair.value
                    if new_pair.value < child_value:
                        new_pair.set_value(child_value)
                        new_pair.set_move(move)
                    if flag:
                        if child_value >= b:
                            return new_pair
                    a = max(a, new_pair.value)
                return new_pair
            else:
                new_pair = Pair(None, self.MAX)
                for move in moves:
                    child = game_state.copy()
                    child.move(move, child.current_player_color)
                    child_score = child.score[0] if game_state.current_player_color == RED else child.score[1]
                    current_score = game_state.score[0] if game_state.current_player_color == RED else game_state.score[1]
                    flag = False
                    if child_score == current_score:
                        pair = self.dfs(child, child.current_player_color, a, b, level+1)
                        flag = True
                    else:
                        pair = self.dfs(child, child.current_player_color, a, b, level+1)
                    child_value = pair.value
                    if new_pair.value > child_value:
                        new_pair.set_value(child_value)
                        new_pair.set_move(move)
                    if flag:
                        if child_value <= a:
                            return new_pair
                    b = min(b, new_pair.value)
                return new_pair
        else:
            return Pair(None, self.heuristic(game_state))



