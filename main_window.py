from PySide6.QtWidgets import QWidget, QMainWindow, QVBoxLayout, QPushButton
from PySide6.QtGui import QKeyEvent
from game import Game


class MainWindow(QMainWindow):
    def __init__(self):
        """
        This is the main window of the application.
        """
        super().__init__()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.game = Game()

        # Widgets to be added to the layout
        layout_widgets = [
            self.game
        ]
        # Add widgets to the layout and set the layout to the central widget
        layout = QVBoxLayout()
        for widget in layout_widgets:
            layout.addWidget(widget)
        central_widget.setLayout(layout)

        self.game.runner_signal = True
        self.game.thread.start()

    def keyPressEvent(self, event: QKeyEvent):
        self.game.keyboard_event(event)

    def keyReleaseEvent(self, event: QKeyEvent):
        self.game.keyboard_event(event)
