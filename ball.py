import time
import threading

from PySide6 import QtGui


class Ball:
    def __init__(self, x, y, ux, uy, size, color, canvas, bg_color):
        """
        Creates a ball object.
        :param x: Starting x coordinate
        :param y: Starting y coordinate
        :param ux: Unitary vector in the x direction
        :param uy: Unitary vector in the y direction
        :param size: Size of the ball
        :param color: Color of the ball
        :param canvas: Canvas to draw the ball on
        :param bg_color: Background color of the canvas
        """
        self.x = x
        self.y = y
        self.ux = ux
        self.uy = uy
        self.size = size
        self.color = QtGui.QColor(color)
        self.canvas = canvas
        self.bg_color = bg_color
        # Internal variables
        self.impact_x = None
        self.impact_y = None
        self.last_drawn_x = None
        self.last_drawn_y = None
        self.speed = 150
        self.moving = False
        self.tick_rate = 0.016
        self.tread = threading.Thread(target=self.runner)

    def draw(self):
        """
        Draws the ball on the canvas.
        :return:
        """
        painter = QtGui.QPainter(self.canvas)
        pen = QtGui.QPen()
        pen.setWidth(self.size)
        pen.setColor(self.color)
        painter.setPen(pen)
        painter.drawPoint(self.x, self.y)
        painter.end()
        self.last_drawn_x = self.x
        self.last_drawn_y = self.y

    def erase(self):
        """
        Erases the ball from the canvas.
        :return:
        """
        painter = QtGui.QPainter(self.canvas)
        pen = QtGui.QPen()
        pen.setWidth(self.size + 1)
        pen.setColor(self.bg_color)
        painter.setPen(pen)
        painter.drawPoint(self.last_drawn_x, self.last_drawn_y)
        painter.end()

    def update(self):
        """
        Updates the ball's position on the canvas.
        :return:
        """
        if self.last_drawn_x is None and self.last_drawn_y is None:
            self.draw()
        else:
            self.erase()
            self.draw()

    def move(self, x, y):
        """
        Moves the ball to the given coordinates.
        :param x: Coordinate x
        :param y: Coordinate y
        :return:
        """
        self.moving = True
        unitary_vector = self.unitary_vector(x, y)
        distance = self.distance_to_point(x, y)
        speed = self.speed * self.tick_rate
        while distance > 0:
            if distance < speed:
                self.x = x
                self.y = y
                distance = 0
            else:
                self.x += unitary_vector[0] * speed
                self.y += unitary_vector[1] * speed
                distance = self.distance_to_point(x, y)
            time.sleep(self.tick_rate)
        self.moving = False

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
            impact_point = self.impact_point_right(ux, uy)
        else:
            # La bola se mueve hacia la izquierda
            impact_point = self.impact_point_left(ux, uy)
        self.impact_x = impact_point[0]
        self.impact_y = impact_point[1]
        return impact_point

    def impact_point_right(self, ux, uy):
        """
        Calculates the impact point of the ball on the right side.
        :param ux: Unitary vector in the x direction
        :param uy: Unitary vector in the y direction
        :return:
        """
        y = self.intersection_y(1024, ux, uy)
        if 0 <= y <= 768:
            # La bola impacta en el lado derecho
            return [1024, y]
        elif y < 0:
            # La bola impacta en la parte superior
            x = self.intersection_x(0, ux, uy)
            return [x, 0]
        elif y > 768:
            # La bola impacta en la parte inferior
            x = self.intersection_x(768, ux, uy)
            return [x, 768]

    def impact_point_left(self, ux, uy):
        """
        Calculates the impact point of the ball on the left side.
        :param ux: Unitary vector in the x direction
        :param uy: Unitary vector in the y direction
        :return:
        """
        y = self.intersection_y(0, ux, uy)
        if 0 <= y <= 768:
            # La bola impacta en el lado izquierdo
            return [0, y]
        elif y < 0:
            # La bola impacta en la parte superior
            x = self.intersection_x(0, ux, uy)
            return [x, 0]
        elif y > 768:
            # La bola impacta en la parte inferior
            x = self.intersection_x(768, ux, uy)
            return [x, 768]

    def intersection_y(self, x, ux, uy):
        """
        Calculates the intersection point in the y axis.
        :param x: A coordinate in the x axis
        :param ux: Unitary vector in the x direction
        :param uy: Unitary vector in the y direction
        :return:
        """
        return (x - self.x) * uy / ux + self.y

    def intersection_x(self, y, ux, uy):
        """
        Calculates the intersection point in the x axis.
        :param y: A coordinate in the y axis
        :param ux: Unitary vector in the x direction
        :param uy: Unitary vector in the y direction
        :return:
        """
        return (y - self.y) * ux / uy + self.x
