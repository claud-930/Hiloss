from PySide6.QtWidgets import QWidget, QMainWindow, QVBoxLayout, QPushButton

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
        self.canvas_thread_button = QPushButton("canvas_thread")
        self.canvas_thread_button.clicked.connect(self.game.flag_change)
        self.test_button = QPushButton("move_ball")
        self.test_button.clicked.connect(self.game.test_move_ball)

        # Widgets to be added to the layout
        layout_widgets = [
            self.game,
            self.canvas_thread_button,
            self.test_button
        ]
        # Add widgets to the layout and set the layout to the central widget
        layout = QVBoxLayout()
        for widget in layout_widgets:
            layout.addWidget(widget)
        central_widget.setLayout(layout)

