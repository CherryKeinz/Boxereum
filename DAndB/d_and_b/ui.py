import pygame,sys
import time
import random
import copy
import sys


from .player import *
from .model import Color
from .AI.gm_AI import GMAI
from .game import Game


AI = 1 # need fix
HUMAN = -1  # need fix
PLAYER1_COLOR = [255, 0, 0]
PLAYER2_COLOR = [0, 0, 255]
BOARD_RANGE_MIN = 70
BOARD_RANGE_MAX = 500
CONVERSION = {0:"a6",1:"b6",2:"c6",3:"d6",4:"e6",5:"f6",6:"a5",7:"b5",8:"c6",9:"d5",10:"e5",11:"f5",12:"a4",13:"b4",14:"c4",15:"d4",16:"e4",17:"f4",18:"a3",19:"b3",20:"c3",21:"d3",22:"e3",23:"f3",24:"a2",25:"b2",26:"c2",27:"d2",28:"e2",29:"f2",30:"a1",31:"b1",32:"c1",33:"d1",34:"e1",35:"f1"}
class UI():
    def __init__(self):
        pygame.init()
        screencaption = pygame.display.set_caption('Pandora')
        self.screen = pygame.display.set_mode([640, 640])
        self.screen.fill([255, 255, 255])
        self.button1 = pygame.image.load("d_and_b/button1.png").convert_alpha()
        self.button2 = pygame.image.load("d_and_b/button2.png").convert_alpha()
        self.screen.blit(self.button1, (220, 150))
        self.screen.blit(self.button2, (220, 350))
        self.score_surf_1 = None
        self.score_surf_2 = None

        self.game_status = False
        self.unavailable = set('')
        self.i = 0
        pygame.display.flip()

    def game_start(self, player):
        self.player_human = HumanPlayer(Color.red, 'Hjh')
        self.player_Pandora = GMAI(Color.blue, 'Ai')
        self.DBGame = Game(self.player_human, self.player_Pandora)
        print('game start!\nscore:', self.DBGame.score)

        self.screen.fill([255, 255, 255])
        # 坐标轴
        self.x_axis = pygame.image.load("d_and_b/x_axis.png").convert_alpha()
        self.button2 = pygame.image.load("d_and_b/y_axis.png").convert_alpha()
        self.screen.blit(self.x_axis, (0, 475))
        self.screen.blit(self.button2, (25, 0))
        # 边框
        pygame.draw.lines(self.screen, [0, 0, 0], True, [(25, 25), (25, 500), (500, 500), (500, 25)], 1)
        # 加载文字
        self.load_text()
        self.points = {}
        for i in range(0, 6):
            for j in range(0, 6):
                self.points[i * 6 + j] = ((i + 1) * 75,(j + 1) * 75)
                pygame.draw.circle(self.screen, [0, 0, 0], self.points[i * 6 + j], 2, 0)
        pygame.display.update()
        # AI move
        if player == AI:
            self.DBGame.transform_player()
            print('你是AI')
            coordinate = self.player_Pandora.find_move(game=self.DBGame, depth=30, during_time=5, verbose=False)
            print(coordinate)
            self.DBGame.move(Piece(self.DBGame.current_player_color, coordinate))
            pointA, pointB = self.str2point(coordinate)
            pygame.draw.line(self.screen, PLAYER2_COLOR, self.points[pointA], self.points[pointB], 1)
        pygame.display.update()

    def draw(self, x, y):
        if BOARD_RANGE_MIN < x < BOARD_RANGE_MAX and  BOARD_RANGE_MIN < y < BOARD_RANGE_MAX:
            points = copy.deepcopy(self.points)
            pointA = self.find_nearest_point(x, y, points)
            points.pop(pointA)
            pointB = self.find_nearest_point(x, y, points)
            # 判断是否已下过了
            if (pointA, pointB) not in self.unavailable:
                print("current_player:"),
                print(self.DBGame.current_player_color)
                # if player is human
                if not isinstance(self.DBGame._current_player, AIPlayer):
                    print("human turn")
                    pygame.draw.line(self.screen, PLAYER1_COLOR, self.points[pointA], self.points[pointB], 1)
                    try:
                        self.DBGame.move(Piece(self.DBGame.current_player_color, self.point2str(pointA, pointB)))
                        hist_pieces = self.DBGame.history
                        for piece in hist_pieces:
                            # print(piece.user_coordinate, piece.color)
                            for r in self.DBGame.board.pieces:
                                print(r)
                    except (PieceCoordinateError, BoardError) as e:
                        print(e)
                    pygame.display.update()

                    # AI move
                    while(isinstance(self.DBGame._current_player, AIPlayer)):
                        print('你是AI')
                        coordinate = self.player_Pandora.find_move(game=self.DBGame, depth=30, during_time=5,
                                                                   verbose=False)
                        print(coordinate)
                        self.DBGame.move(Piece(self.DBGame.current_player_color, coordinate))
                        pointA, pointB = self.str2point(coordinate)
                        pygame.draw.line(self.screen, PLAYER2_COLOR, self.points[pointA], self.points[pointB], 1)


                # 分数接口
                self.score_diaplay(self.DBGame.score)
                print("score:"),
                print(self.DBGame.score)
                self.unavailable.add((pointA, pointB))
                self.unavailable.add((pointB, pointA))
                pygame.display.update()

    # 显示分数
    def score_diaplay(self, text):
        self.score_surf_1.fill([255, 255, 255])
        TextRect = self.score_surf_1.get_rect()
        TextRect.center = (570, 120)
        self.screen.blit(self.score_surf_1, TextRect)
        self.score_surf_2.fill([255, 255, 255])
        TextRect = self.score_surf_2.get_rect()
        TextRect.center = (570, 120)
        self.screen.blit(self.score_surf_2, TextRect)

        largeText = pygame.font.Font('freesansbold.ttf', 20)
        self.score_surf_1 = largeText.render(str(text[0]), True, [0, 0, 0])
        TextRect = self.score_surf_1.get_rect()
        TextRect.center = (570, 120)
        self.screen.blit(self.score_surf_1, TextRect)

        self.score_surf_2 = largeText.render(str(text[1]), True, [0, 0, 0])
        TextRect2 = self.score_surf_2.get_rect()
        TextRect2.center = (570, 220)
        self.screen.blit(self.score_surf_2, TextRect2)
        pygame.display.update()

    def load_text(self):
        my_font = pygame.font.Font('freesansbold.ttf', 20)
        textstr = 'Pandora'
        TextSurf = my_font.render(textstr, True, [0, 0, 0])
        TextRect = TextSurf.get_rect()
        TextRect.center = (570, 70)
        self.screen.blit(TextSurf, TextRect)

        textstr2 = 'Human'
        TextSurf2 = my_font.render(textstr2, True, [0, 0, 0])
        TextRect = TextSurf2.get_rect()
        TextRect.center = (570, 170)
        self.screen.blit(TextSurf2, TextRect)

        self.score_surf_1 = my_font.render("0", True, [0, 0, 0])
        TextRect = self.score_surf_1.get_rect()
        TextRect.center = (570, 120)
        self.screen.blit(self.score_surf_1, TextRect)

        self.score_surf_2 = my_font.render("0", True, [0, 0, 0])
        TextRect2 = self.score_surf_2.get_rect()
        TextRect2.center = (570, 220)
        self.screen.blit(self.score_surf_2, TextRect2)

    def find_nearest_point(self, x, y, points):
        instance = sys.maxsize
        nearest_point = -1
        for index, point in points.items():
            if (point[0] - x) ** 2 + (point[1] - y) ** 2 < instance:
                instance = (point[0] - x) ** 2 + (point[1] - y) ** 2
                nearest_point = index
        return nearest_point

    def who_first(self, x, y):
        if 220 < x < 420 and 150 < y < 250:
            return HUMAN
        elif 220 < x < 420 and 350 < y < 450:
            return AI
        else:
            return False

    def start(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pressed_x, pressed_y = event.pos
                    if self.game_status == False:
                        player = self.who_first(pressed_x, pressed_y)
                        if player:
                            self.game_start(player)
                            self.game_status = True
                    else:
                        self.draw(pressed_x, pressed_y)

    def gaming(self):
        print("现在是", self.DBGame.current_player_color, "方下棋")
        if isinstance(self.DBGame._current_player, AIPlayer):
            print('你是AI')
            # print(blue_player.longest_chain_from(self.DBGame.board, dict(), 1, 1, 0))
            self.DBGame.transform_player()
        else:
            coordinate = input('输入下棋')
            try:
                self.DBGame.move(Piece(self.DBGame.current_player_color, coordinate))
                hist_pieces = self.DBGame.history
                for piece in hist_pieces:
                    print(piece.user_coordinate, piece.color)
                    for r in self.DBGame.board.pieces:
                        print(r)
            except (PieceCoordinateError, BoardError) as e:
                print(e)

    def point2str(self, pointA, pointB):
        # 横的
        if (pointA - pointB) ** 2 == 1:
            index = pointA if pointA < pointB else pointB
            return CONVERSION[pointA if pointA < pointB else pointB] + 'h'
        # 竖着的
        else:
            return CONVERSION[pointA if pointA > pointB else pointB] + 'v'

    def str2point(self, str):
        if str[-1] == 'h':
            for k, v in CONVERSION.items():
                if v == str[:-1]:
                    return k, k + 1
        else:
            for k, v in CONVERSION.items():
                if v == str[:-1]:
                    return k, k + 6

ui = UI()
ui.start()
