import threading
import time

from PySide6 import QtGui, QtWidgets

from Drawables.ball import Ball
from Drawables.player import Player
from Constants import KeyBinds, Colors, Dimensions


class Game(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        self.canvas = QtGui.QPixmap(
            Dimensions.canvas['width'],
            Dimensions.canvas['height']
        )
        self.canvas.fill(Colors.canvas)
        self.setPixmap(self.canvas)
        self.tick_rate = 0.016

        self.canvas_thread = threading.Thread(target=self.canvas_update)
        self.canvas_thread_runner_signal = False

        self.player1 = Player(
            0,
            Dimensions.center_player_y,
            Dimensions.player['size'],
            Dimensions.player['thickness'],
            self.canvas,
            Colors.player1,
            Colors.canvas,
            KeyBinds.player1
        )
        self.player2 = Player(
            Dimensions.canvas['width'] -
            Dimensions.player['thickness'],
            Dimensions.center_player_y,
            Dimensions.player['size'],
            Dimensions.player['thickness'],
            self.canvas,
            Colors.player2,
            Colors.canvas,
            KeyBinds.player2
        )
        self.ball: Ball = None
        self.ball_owner = self.player1
        self.start_player_threads()

    def score(self):
        self.stop_objects_threads()

        self.ball_owner.score += 1
        if self.ball_owner == self.player1:
            self.ball_owner = self.player2
        else:
            self.ball_owner = self.player1

        self.reset()

    def reset(self):
        self.canvas.fill(Colors.canvas)
        self.setPixmap(self.canvas)
        self.player1.reset()
        self.player2.reset()

    def stop_objects_threads(self):
        self.ball.runner_signal = False
        self.player1.runner_signal = False
        self.player2.runner_signal = False

    def start_player_threads(self):
        self.player1.runner_signal = True
        self.player2.runner_signal = True
        self.player1.thread.start()
        self.player2.thread.start()
        self.ball_owner.spawn_ball()
        self.ball = self.ball_owner.ball

    def canvas_update(self):
        while self.canvas_thread_runner_signal:
            self.setPixmap(self.canvas)
            time.sleep(self.tick_rate)

    def keyboard_event(self, event: QtGui.QKeyEvent):
        if event.key() in self.player1.keys.keys():
            self.player1.keyboard_event(event)
        elif event.key() in self.player2.keys.keys():
            self.player2.keyboard_event(event)
        else:
            return
