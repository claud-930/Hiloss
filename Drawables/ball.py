import time
import threading

from PySide6 import QtGui, QtCore

from Drawables.game_object import DrawableGameObject


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
        self.ux = ux
        self.uy = uy
        self.__impact_x = None
        self.__impact_y = None
        self.speed = 500
        self.tick_rate = 0.016
        self.thread = threading.Thread(target=self.runner)
        self.runner_signal = False

    @property
    def impact_x(self):
        return self.__impact_x

    @impact_x.setter
    def impact_x(self, value):
        value = int(value)
        max_x = self.canvas.width() - self.thickness
        if value < 0:
            self.__impact_x = 0
        elif value > max_x:
            self.__impact_x = max_x
        else:
            self.__impact_x = value

    @property
    def impact_y(self):
        return self.__impact_y

    @impact_y.setter
    def impact_y(self, value):
        value = int(value)
        max_y = self.canvas.height() - self.thickness
        if value < 0:
            self.__impact_y = 0
        elif value > max_y:
            self.__impact_y = max_y
        else:
            self.__impact_y = value

    def runner(self):
        initial_impact_point = self.impact_point(self.ux, self.uy)
        self.impact_x = initial_impact_point[0]
        self.impact_y = initial_impact_point[1]
        while self.runner_signal:
            self.move(self.impact_x, self.impact_y)
            self.bounce()

    def paint(self, color: QtGui.QColor, x, y):
        painter = QtGui.QPainter(self.canvas)
        rect = QtCore.QRect(x, y, self.thickness, self.thickness)
        painter.fillRect(rect, color)

    def move(self, x, y):
        """
        Moves the ball to the given coordinates.
        :param x: Coordinate x
        :param y: Coordinate y
        :return:
        """
        self.unitary_vector(x, y)
        distance = self.distance_to_point(x, y)
        speed = self.speed * self.tick_rate
        while distance > 0:
            if distance < speed:
                self.x = x
                self.y = y
                distance = 0
            else:
                self.x += self.ux * speed
                self.y += self.uy * speed
                distance = self.distance_to_point(x, y)
            time.sleep(self.tick_rate)

    def bounce(self):
        self.ux = -self.ux
        self.uy = -self.uy
        self.impact_point(self.ux, self.uy)

    def distance_to_point(self, x, y):
        """
        Calculates the distance to a point.
        :param x: Coordinate x
        :param y: Coordinate y
        :return:
        """
        return ((self.x - x) ** 2 + (self.y - y) ** 2) ** 0.5

    def unitary_vector(self, x, y):
        """
        Calculates the unitary vector of the direction.
        :param x: Coordinate x
        :param y: Coordinate y
        :return:
        """
        distance_x = x - self.x
        distance_y = y - self.y
        distance = self.distance_to_point(x, y)
        ux = distance_x / distance
        uy = distance_y / distance
        return [ux, uy]

    def impact_point(self, ux, uy):
        """
        Calculates the impact point of the ball.
        :param ux: Unitary vector in the x direction
        :param uy: Unitary vector in the y direction
        :return:
        """
        impact_point = []
        if ux > 0:
            # La bola se mueve hacia la derecha
            impact_point = self.__impact_point_right(ux, uy)
        else:
            # La bola se mueve hacia la izquierda
            impact_point = self.__impact_point_left(ux, uy)
        self.impact_x = impact_point[0]
        self.impact_y = impact_point[1]
        return [self.impact_x, self.impact_y]

    def __impact_point_right(self, ux, uy):
        """
        Calculates the impact point of the ball on the right side.
        :param ux: Unitary vector in the x direction
        :param uy: Unitary vector in the y direction
        :return:
        """
        y = self.__intersection_y(self.canvas.width(), ux, uy)
        if 0 <= y <= self.canvas.height():
            # La bola impacta en el lado derecho
            return [self.canvas.width(), y]
        elif y < 0:
            # La bola impacta en la parte superior
            x = self.__intersection_x(0, ux, uy)
            return [x, 0]
        elif y > self.canvas.height():
            # La bola impacta en la parte inferior
            x = self.__intersection_x(self.canvas.height(), ux, uy)
            return [x, self.canvas.height()]

    def __impact_point_left(self, ux, uy):
        """
        Calculates the impact point of the ball on the left side.
        :param ux: Unitary vector in the x direction
        :param uy: Unitary vector in the y direction
        :return:
        """
        y = self.__intersection_y(0, ux, uy)
        if 0 <= y <= self.canvas.height():
            # La bola impacta en el lado izquierdo
            return [0, y]
        elif y < 0:
            # La bola impacta en la parte superior
            x = self.__intersection_x(0, ux, uy)
            return [x, 0]
        elif y > self.canvas.height():
            # La bola impacta en la parte inferior
            x = self.__intersection_x(self.canvas.height(), ux, uy)
            return [x, self.canvas.height()]

    def __intersection_y(self, x, ux, uy):
        """
        Calculates the intersection point in the y axis.
        :param x: A coordinate in the x axis
        :param ux: Unitary vector in the x direction
        :param uy: Unitary vector in the y direction
        :return:
        """
        return (x - self.x) * uy / ux + self.y

    def __intersection_x(self, y, ux, uy):
        """
        Calculates the intersection point in the x axis.
        :param y: A coordinate in the y axis
        :param ux: Unitary vector in the x direction
        :param uy: Unitary vector in the y direction
        :return:
        """
        return (y - self.y) * ux / uy + self.x
