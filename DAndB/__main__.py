# -*- coding: UTF-8 -*-
import sys

from DAndB.d_and_b.player import *
from DAndB.d_and_b.AI.uct_AI import GMAI
from DAndB.d_and_b.game import Game
from DAndB.d_and_b.AI.alphabeta_AI import AlphaBetaAI

RED = 1
BLUE = -1
if __name__ == '__main__':
    red_player = AlphaBetaAI(RED, 'Hjh')
    blue_player = AlphaBetaAI(BLUE, 'Ai')
    DBGame = Game(red_player, blue_player)
    print('game start!\nscore:', DBGame.score)
    while DBGame.is_end is False:
        print("现在是", DBGame.current_player_color, "方下棋")
        if DBGame.current_player_color == RED:
            print('红方下棋')
            coordinate = red_player.getNextMove(DBGame, 15)
            print(coordinate)
            DBGame.move(coordinate, DBGame.current_player_color)
        else:
            print('蓝方下棋')
            coordinate = blue_player.getNextMove(DBGame, 15)
            print(coordinate)
            DBGame.move(coordinate, DBGame.current_player_color)
        # if isinstance(DBGame._current_player, AIPlayer):
        #     print('你是AI')
        #     # coordinate = blue_player.find_move(game=DBGame, depth=30, during_time=30, verbose=False)
        #     coordinate = blue_player.getNextMove(DBGame, 15)
        #     print(coordinate)
        #     DBGame.move(coordinate, DBGame.current_player_color)
        #     for i in DBGame._board.pieces:
        #         print(i)
        # else:
        #     coordinate = input('输入下棋')
        #     try:
        #         DBGame.move(coordinate, DBGame.current_player_color)
        #         hist_pieces = DBGame.history
        #         for piece in hist_pieces:
        #             print(piece[0], piece[1])
        #         for i in DBGame._board.pieces:
        #             print(i)
        #     except BoardError as e:
        #         print(e)
    if DBGame.winner == RED:
        print('红方获胜！')
        print(DBGame.score)
    else:
        print('蓝方获胜！')
        print(DBGame.score)
    print(DBGame.history)

