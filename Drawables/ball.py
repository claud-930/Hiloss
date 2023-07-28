import time
import threading

from PySide6 import QtGui, QtCore

from Drawables.game_object import DrawableGameObject

from Constants import Dimensions


class Ball(DrawableGameObject):
    def __init__(self, x, y, ux, uy, thickness, color, canvas, bg_color):
        """
        Creates a ball object.
        :param x: Starting x coordinate
        :param y: Starting y coordinate
        :param ux: Unitary vector in the x direction
        :param uy: Unitary vector in the y direction
        :param thickness: thickness of the ball
        :param color: Color of the ball
        :param canvas: Canvas to draw the ball on
        :param bg_color: Background color of the canvas
        """
        super().__init__(x, y, thickness, color, bg_color, canvas)
        self.direction = [ux, uy]
        self.dx = None
        self.dy = None

        self.speed = 500
        self.tick_rate = 0.016
        self.set_displacement()
        self.thread = threading.Thread(target=self.runner)
        self.runner_signal = False
        self.bounce_flag = False
        self.critical_zone = {
            'flag': False,
            'x1': None,
            'x2': None
        }

    def runner(self):
        while self.runner_signal:
            if self.critical_zone['flag'] is False:
                self.move()
            time.sleep(self.tick_rate)

    def paint(self, color: QtGui.QColor, x, y):
        painter = QtGui.QPainter(self.canvas)
        rect = QtCore.QRect(x, y, self.thickness, self.thickness)
        painter.fillRect(rect, color)

    def move(self):
        self.x += self.dx
        self.y += self.dy
        if self.x_critical_zone(self.x + self.dx):
            self.critical_zone['flag'] = True
        if self.y <= 0 \
                or self.y >= Dimensions.canvas['height'] - self.thickness:
            self.bounce([self.direction[0], -self.direction[1]])
        self.update()

    def bounce(self, direction: list):
        self.direction = direction
        self.set_displacement()

    def set_displacement(self):
        self.dx = int(self.direction[0] * self.speed * self.tick_rate)
        self.dy = int(self.direction[1] * self.speed * self.tick_rate)

    def x_critical_zone(self, x):
        return self.critical_zone['x1'] <= x <= self.critical_zone['x2']
