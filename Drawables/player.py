import time
import threading

from PySide6 import QtGui, QtCore

from Drawables.game_object import DrawableGameObject
from Drawables.ball import Ball

from Constants import Dimensions, Colors


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
        self.score = 0

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
            if self.sticky:
                self.ball.update()
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

    def reset(self):
        # End thread and start a new one
        self.thread.join()
        self.thread = threading.Thread(target=self.runner)
        # Reset player attributes
        self.y = Dimensions.center_player_y
        self.sticky = False
        self.ball = None
        self.__last_drawn_x = None
        self.__last_drawn_y = None
        self.draw()

    def spawn_ball(self):
        y_ball = Dimensions.center_player_y + \
                 Dimensions.center_ball_on_player_y

        if self.x == 0:
            x_ball = Dimensions.player['thickness']
            ux = 1
        else:
            x_ball = Dimensions.canvas['width'] - \
                     Dimensions.player['thickness'] - Dimensions.ball
            ux = -1

        self.ball = Ball(
            x_ball, y_ball,
            ux, 0,
            Dimensions.ball,
            Colors.neutral, self.canvas, Colors.canvas
        )
        ball_receiver = 'player2' if self.x == 0 else 'player1'
        critical_pos = Dimensions.ball_critical_pos[ball_receiver]
        self.ball.critical_zone['x1'] = critical_pos[0]
        self.ball.critical_zone['x2'] = critical_pos[1]
        self.sticky = True
        self.ball.update()
