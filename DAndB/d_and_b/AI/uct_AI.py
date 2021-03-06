# -*- coding: UTF-8 -*-
import random
import time
from math import sqrt, log

from ..player import AIPlayer
from ..model import *

class Node:
    """ A node in the game tree. Note wins is always from the viewpoint of playerJustMoved.
        Crashes if state not specified.
    """
    def __init__(self, move = None, parent = None, game_state = None):
        self.state = game_state
        self.move = move # the move that got us to this node - "None" for the root node
        self.parentNode = parent # "None" for the root node
        self.childNodes = []
        self.score = 0.0
        self.visits = 0.0
        self.untriedMoves = game_state.get_moves() # future child nodes
        self.playerTurn = game_state.current_player_color

    def UCTSelectChild(self):
        """ Use the UCB1 formula to select a child node. Often a constant UCTK is applied so we have
            lambda c: c.wins/c.visits + UCTK * sqrt(2*log(self.visits)/c.visits to vary the amount of
            exploration versus exploitation.
        """
        s = sorted(self.childNodes, key = lambda c: c.score/c.visits + sqrt(2*log(self.visits)/c.visits))[-1]
        return s

    def AddChild(self, m, s):
        """ Remove m from untriedMoves and add a new child node for this move.
            Return the added child node
        """
        n = Node(move = m, parent = self, game_state = s)
        self.untriedMoves.remove(m)
        self.childNodes.append(n)
        return n

    def Update(self, result):
        """ Update this node - one additional visit and result additional wins. result must be from the viewpoint of playerJustmoved.
        """
        self.visits += 1
        self.score += result


# 这是一个AI示例，使用随机算法
class GMAI(AIPlayer):
    def __init__(self, color, name):
        super(GMAI, self).__init__(color, name)
        self.step_num = 0

    def start_new_game(self):
        pass
        # self.step_num = 0
        #             #  0  1  2  3  4  5  6  7  8  9  10
        # self.board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 0
        #               [0, 4, 0, 4, 0, 4, 0, 4, 0, 4, 0],  # 1
        #               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 2
        #               [0, 4, 0, 4, 0, 4, 0, 4, 0, 4, 0],  # 3
        #               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 4
        #               [0, 4, 0, 4, 0, 4, 0, 4, 0, 4, 0],  # 5
        #               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 6
        #               [0, 4, 0, 4, 0, 4, 0, 4, 0, 4, 0],  # 7
        #               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 8
        #               [0, 4, 0, 4, 0, 4, 0, 4, 0, 4, 0],  # 9
        #               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]  # 10
        # self.box = ([], [], [], [], [])
        # for x in (1, 3, 5, 7, 9):
        #     for y in (1, 3, 5, 7, 9):
        #         self.box[4].append((x, y))

    def game_is_over(self, is_win):
        print(is_win)

    def find_move(self, game, depth, during_time, verbose):
        return self.UCT(rootstate=game, rolloutDepth=depth, dur=during_time, verbose=verbose)

    def UCT(self, rootstate, rolloutDepth=float('inf'), dur=1, verbose=False):
        """ Conduct a UCT search for dur second(s) starting from rootstate.
            Return the best move from the rootstate."""

        rootnode = Node(game_state=rootstate)
        print("rootstate color is ", rootstate.current_player_color)
        debugStr = "rootState is " + str(rootstate)

        me = rootstate.current_player_color

        debugStr += ", it is " + str(me) + "'s turn.\n"

        t_start = time.time()
        t_deadline = t_start + dur

        iterations = 0

        while True:
            iterations += 1

            # MCTS
            node = rootnode
            # print(len(node.childNodes), '子节点', len(node.untriedMoves), '可移动个数')
            state = rootstate.copy()

            # 选择
            while node.untriedMoves == [] and node.childNodes != []:
                # for child in node.childNodes:
                #     print(state.current_player_color)
                #     print(child.playerTurn)
                # debugStr += "\tAll movies tried, selecting a child.\n"
                # debugStr += rootnode.TreeToString(1)
                node = node.UCTSelectChild()
                # print(node.playerTurn)
                state.move(node.move, state.current_player_color)
                debugStr += "\tSelected node " + node.move + ".\n"

            # 扩展
            if node.untriedMoves != []:
                m = random.choice(node.untriedMoves)
                # print(node.playerTurn)
                state.move(m, node.playerTurn)
                # print(state.current_player_color)
                node = node.AddChild(m, state)
                debugStr += "\t\tCreating child " + node.move + ".\n"

            # 模拟
            depth = 0
            while state.get_moves() != [] and depth < rolloutDepth:
                """
                moves = state.get_moves()
                best_move = moves[0]
                best_expectation = float('-inf')
                for move in moves:
                    rollout_state = state.copy()
                    rollout_state.apply_move(move)
                    score = outcome(rollout_state.get_score())
                    if score > best_expectation:
                        best_expectation = score
                        best_move = move

                state.apply_move(best_move)
                """
                m = random.choice(state.get_moves())
                state.move(m, state.current_player_color)
                depth += 1

            # 反向传播
            score = state.score
            if me == BLUE:
                gamescore = score[1] - score[0]
            else:
                gamescore = score[0] - score[1]
            debugStr += "\t\tSimulation score is " + str(gamescore) + ".\n"
            while node != None:
                if node.parentNode != None:
                    # print(node.parentNode.playerTurn)#输出父节点玩家
                    if node.parentNode.playerTurn != me:
                        gamescore = -gamescore

                node.Update(gamescore)
                node = node.parentNode

            # end MCTS

            t_now = time.time()
            if t_now > t_deadline:
                break
        print(state.red_player.score)
        sample_rate = float(iterations) / (t_now - t_start)
        print("%s samples per second" % (sample_rate))
        # print rootnode.TreeToString(0)
        rootnode.childNodes.sort(key=lambda c: c.score / c.visits)
        for c in rootnode.childNodes:
            print("S: " + str(c.score) + " V: " + str(c.visits) + " S/V: " + str(c.score / c.visits) + " Move: " + str(c.move))

        movelist = sorted(rootnode.childNodes, key=lambda c: c.score / c.visits)
        print("Selected move = " + str(movelist[-1].move))
        debugStr += "Selecting move " + str(movelist[-1].move)
        if (verbose):
            print(debugStr)
        return str(movelist[-1].move)

    def last_move(self, piece, board, next_player_color):
        if piece != None:
            self.step_num = self.step_num + 1
            x, y = piece.coordinate
            self.board[x][y] = 1 if piece.color == self.color else -1
            if x % 2 == 0:
                if x + 1 < 10:
                    if self.board[x+1][y] != 0:
                        self.box[self.board[x+1][y]].remove((x+1, y))
                        self.board[x+1][y] = self.board[x+1][y] - 1
                        self.box[self.board[x+1][y]].append((x+1, y))
                if x - 1 > 0:
                    if self.board[x-1][y] != 0:
                        self.box[self.board[x-1][y]].remove((x-1, y))
                        self.board[x-1][y] = self.board[x-1][y] - 1
                        self.box[self.board[x-1][y]].append((x-1, y))
            else:
                if y + 1 < 10:
                    if self.board[x][y+1] != 0:
                        self.box[self.board[x][y+1]].remove((x, y+1))
                        self.board[x][y+1] = self.board[x][y+1] - 1
                        self.box[self.board[x][y+1]].append((x, y+1))
                if y - 1 > 0:
                    if self.board[x][y-1] != 0:
                        self.box[self.board[x][y-1]].remove((x, y-1))
                        self.board[x][y-1] = self.board[x][y-1] - 1
                        self.box[self.board[x][y-1]].append((x, y-1))

        super(GMAI, self).last_move(piece, board, next_player_color)

    def coordinate_exchange(self, coordinate):  # 坐标转换函数
        x, y = coordinate
        type = 'h' if x % 2 == 0 else 'v'
        x = x if x % 2 == 0 else x+1
        x = str(int(6 - x / 2))
        y = ['a', 'b', 'c', 'd', 'e', 'f'][y//2]
        return (y, x, type)
