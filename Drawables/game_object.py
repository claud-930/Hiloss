from PySide6 import QtGui


class DrawableGameObject:
    def __init__(self,
                 x: float,
                 y: float,
                 thickness: int,
                 object_color: QtGui.QColor,
                 bg_color: QtGui.QColor,
                 canvas: QtGui.QPixmap):
        self.x = x
        self.y = y
        self.last_drawn_x: float = None
        self.last_drawn_y: float = None
        self.thickness = thickness
        self.object_color = object_color
        self.bg_color = bg_color
        self.canvas = canvas

    def paint(self, color: QtGui.QColor, x, y):
        pass

    def draw(self):
        self.paint(self.object_color, self.x, self.y)
        self.last_drawn_x = self.x
        self.last_drawn_y = self.y

    def erase(self):
        self.paint(self.bg_color, self.last_drawn_x, self.last_drawn_y)

    def update(self):
        if self.last_drawn_x is None and self.last_drawn_y is None:
            self.draw()
        else:
            self.erase()
            self.draw()
