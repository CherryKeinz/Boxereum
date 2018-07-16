# -*- coding: UTF-8 -*-
import sys

from DAndB.d_and_b.player import *
from DAndB.d_and_b import game
from DAndB.d_and_b import d_and_b
from DAndB.d_and_b.model import Color
from DAndB.d_and_b.AI.gm_AI import GMAI
from DAndB.d_and_b.game import Game

if __name__ == '__main__':
    # app = QApplication(sys.argv)
    # main_window_controller = MainWindowController()
    # main_window_controller.window.show()
    # sys.exit(app.exec_())

    red_player = HumanPlayer(Color.red, 'Hjh')
    blue_player = GMAI(Color.blue, 'Ai')
    DBGame = Game(red_player, blue_player)
    print('game start!\nscore:', DBGame.score)
    while DBGame.is_end is False:
        print("现在是", DBGame.current_player_color, "方下棋")
        if isinstance(DBGame._current_player, AIPlayer):
            print('你是AI')
            coordinate = blue_player.find_move(game=DBGame, depth=30, during_time=60, verbose=False)
            print(coordinate)
            DBGame.move(Piece(DBGame.current_player_color, coordinate))
        else:
            coordinate = input('输入下棋')
            try:
                DBGame.move(Piece(DBGame.current_player_color, coordinate))
                hist_pieces = DBGame.history
                for piece in hist_pieces:
                    print(piece.user_coordinate, piece.color)
                    for r in DBGame.board.pieces:
                        print(r)
            except (PieceCoordinateError, BoardError) as e:
                print(e)
