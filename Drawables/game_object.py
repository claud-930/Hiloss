from PySide6 import QtGui


class DrawableGameObject:
    def __init__(self,
                 x: int,
                 y: int,
                 thickness: int,
                 object_color: QtGui.QColor,
                 bg_color: QtGui.QColor,
                 canvas: QtGui.QPixmap):
        self.__x = x
        self.__y = y
        self.__last_drawn_x: int = None
        self.__last_drawn_y: int = None
        self.thickness = thickness
        self.object_color = object_color
        self.bg_color = bg_color
        self.canvas = canvas

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        self.__x = int(value)

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, value):
        self.__y = int(value)

    def paint(self, color: QtGui.QColor, x, y):
        pass

    def draw(self):
        self.paint(self.object_color, self.__x, self.__y)
        self.__last_drawn_x = self.__x
        self.__last_drawn_y = self.__y

    def erase(self):
        self.paint(self.bg_color, self.__last_drawn_x, self.__last_drawn_y)

    def update(self):
        if self.__last_drawn_x is None and self.__last_drawn_y is None:
            self.draw()
        else:
            self.erase()
            self.draw()
