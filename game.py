import threading
import time

from PySide6 import QtGui, QtWidgets

from ball import Ball


class Game(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        self.bg_color = QtGui.QColor('black')
        self.canvas = QtGui.QPixmap(1024, 768)
        self.canvas.fill(self.bg_color)

        self.ball = Ball(200, 150, 20, 1, 0, 'red', self.canvas, self.bg_color)
        self.setPixmap(self.canvas)
        self.tick_rate = 0.016
        self.flag = False

        self.canvas_thread = threading.Thread(target=self.canvas_update)

    def flag_change(self):
        self.flag = not self.flag
        if self.canvas_thread.is_alive():
            self.canvas_thread.join()
        else:
            self.canvas_thread.start()

    def test_move_ball(self):
        thread = threading.Thread(target=self.ball.move, args=(500, 500))
        thread.start()

    def canvas_update(self):
        while self.flag:
            self.ball.update()
            self.setPixmap(self.canvas)
            time.sleep(self.tick_rate)
