import time
import threading

from PySide6 import QtGui, QtCore

from Drawables.game_object import DrawableGameObject
from Drawables.ball import Ball

from Constants import Dimensions


class Player(DrawableGameObject):
    def __init__(self, x, y, size, thickness,
                 canvas, color, bg_color,
                 listeners: list,
                 tick_rate=0.016):
        """
        Creates a player object.
        :param x: Initial __x coordinate
        :param y: Initial __y coordinate
        :param size: Size of the player bar
        :param thickness: Thickness of the player bar
        :param canvas: Canvas to draw the player bar on
        :param color: Color of the player bar
        :param bg_color: Background color of the canvas
        :param listeners: List of key listeners
        :param tick_rate: Tick rate for updating the player bar
        """
        super().__init__(x, y, thickness, color, bg_color, canvas)
        self.size = size
        self.speed = 10
        self.tick_rate = tick_rate
        # Key listeners
        self.key_up = listeners[0]
        self.key_down = listeners[1]
        self.key_special = listeners[2]
        self.keys = {
            listeners[0]: False,
            listeners[1]: False,
            listeners[2]: False
        }
        # Thread
        self.thread = threading.Thread(target=self.runner)
        self.runner_signal = False
        self.sticky = False
        self.ball = None

    def runner(self):
        while self.runner_signal:
            if self.keys[self.key_up]:
                self.move_up()
            elif self.keys[self.key_down]:
                self.move_down()
            elif self.keys[self.key_special]:
                if self.ball is not None:
                    self.launch_ball()
            self.update()
            time.sleep(self.tick_rate)

    def paint(self, color: QtGui.QColor, x, y):
        painter = QtGui.QPainter(self.canvas)
        rect = QtCore.QRect(x, y, self.thickness, self.size)
        painter.fillRect(rect, color)

    def move_up(self):
        if self.y <= 0:
            self.y = 0
            if self.sticky:
                self.ball.y = Dimensions.center_ball_on_player_y
        else:
            self.y -= self.speed
            if self.sticky:
                self.ball.y -= self.speed

    def move_down(self):
        max_y = self.canvas.height() - self.size
        if self.y >= max_y:
            self.y = max_y
            if self.sticky:
                self.ball.y = max_y + Dimensions.center_ball_on_player_y
        else:
            self.y += self.speed
            if self.sticky:
                self.ball.y += self.speed

    def keyboard_event(self, event: QtGui.QKeyEvent):
        if event.isAutoRepeat():
            return
        if event.key() in self.keys:
            self.keys[event.key()] = not self.keys[event.key()]

    def ball_sticky(self, ball: Ball):
        self.ball = ball
        self.sticky = True

    def launch_ball(self):
        self.ball.runner_signal = True
        self.ball.thread.start()
        self.ball = None
        self.sticky = False
