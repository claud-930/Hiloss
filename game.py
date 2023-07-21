import threading
import time

from PySide6 import QtGui, QtWidgets

from Drawables.ball import Ball
from Drawables.player import Player


class Game(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        self.bg_color = QtGui.QColor('black')
        self.canvas = QtGui.QPixmap(1024, 768)
        self.canvas.fill(self.bg_color)

        self.ball = Ball(200, 150, 1, 0, 20, QtGui.QColor('red'), self.canvas, self.bg_color)
        self.setPixmap(self.canvas)
        self.tick_rate = 0.016
        self.flag = False

        self.canvas_thread = threading.Thread(target=self.canvas_update)

        self.player1_keys = [
            87,  # W
            83,  # S
            70   # F
        ]
        self.player2_keys = [
            79,  # O
            76,  # L
            74   # J
        ]
        self.player1: Player = None
        self.player2: Player = None
        self.instantiate_players()

    def instantiate_players(self):
        self.player1 = Player(0, 50, 100, 20,
                              self.canvas, QtGui.QColor('red'), self.bg_color,
                              self.player1_keys)
        self.player2 = Player(1004, 50, 100, 20,
                              self.canvas, QtGui.QColor('blue'), self.bg_color,
                              self.player2_keys)
        self.player1.runner_signal = True
        self.player2.runner_signal = True
        self.player1.thread.start()
        self.player2.thread.start()

    def test_move_ball(self):
        self.ball.runner_signal = True
        thread = threading.Thread(target=self.ball.runner)
        thread.start()

    def canvas_update(self):
        while self.flag:
            self.ball.update()
            self.setPixmap(self.canvas)
            time.sleep(self.tick_rate)

    def keyboard_event(self, event: QtGui.QKeyEvent):
        if event.key() in self.player1_keys:
            self.player1.keyboard_event(event)
        elif event.key() in self.player2_keys:
            self.player2.keyboard_event(event)
        else:
            return
