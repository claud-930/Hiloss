import math
import threading
import time

from PySide6 import QtGui, QtWidgets

from Drawables.ball import Ball
from Drawables.player import Player
from Constants import KeyBinds, Colors, Dimensions


class Game(QtWidgets.QLabel):
    """
    Main game class that handles the game logic
    """
    def __init__(self):
        super().__init__()
        self.canvas = QtGui.QPixmap(
            Dimensions.canvas['width'],
            Dimensions.canvas['height']
        )
        self.canvas.fill(Colors.canvas)
        self.setPixmap(self.canvas)
        self.tick_rate = 0.016

        self.thread = threading.Thread(target=self.runner)
        self.runner_signal = False

        self.player1 = Player(
            0,
            Dimensions.center_player_y,
            Dimensions.player['size'],
            Dimensions.player['thickness'],
            self.canvas,
            Colors.player1,
            Colors.canvas,
            KeyBinds.player1
        )
        self.player2 = Player(
            Dimensions.canvas['width'] -
            Dimensions.player['thickness'],
            Dimensions.center_player_y,
            Dimensions.player['size'],
            Dimensions.player['thickness'],
            self.canvas,
            Colors.player2,
            Colors.canvas,
            KeyBinds.player2
        )
        self.players = [self.player1, self.player2]
        self.ball: Ball = None
        self.ball_owner = self.player1
        self.ball_receiver = self.player2
        self.start_player_threads()

    def runner(self):
        """
        Method that runs the game logic in a separate thread from the GUI
        :return:
        """
        while self.runner_signal:
            if self.ball.critical_zone['flag'] is True:
                self.critical_zone_logic()
            self.setPixmap(self.canvas)
            time.sleep(self.tick_rate)

    def critical_zone_logic(self):
        """
        Handles the logic when the ball is in the critical zone
        :return:
        """
        ball_receiver_surface = [
            self.ball_receiver.y,
            self.ball_receiver.y + self.ball_receiver.size
        ]
        if ball_receiver_surface[0] <= self.ball.y <= \
                ball_receiver_surface[1]:
            bounce_zones = [
                self.ball_receiver.y + Dimensions.bounce_offsets['y0'],
                self.ball_receiver.y + Dimensions.bounce_offsets['y1'],
                self.ball_receiver.y + Dimensions.bounce_offsets['y2'],
                self.ball_receiver.y + Dimensions.bounce_offsets['y3']
            ]
            ball_middle = self.ball.y + self.ball.thickness / 2
            self.bounce_ball(bounce_zones, ball_middle)
        else:
            self.score()

    def bounce_ball(self, bounce_zones, ball_middle):
        """
        Bounces the ball according to the bounce zones
        :param bounce_zones: Pass the bounce zones as a list
        :param ball_middle: Pass the middle of the ball as a float
        :return:
        """
        if bounce_zones[0] <= ball_middle <= bounce_zones[1]:
            if self.ball.direction[0] < 0:
                self.ball.bounce([math.sqrt(1 / 2), -math.sqrt(1 / 2)])
            else:
                self.ball.bounce([-math.sqrt(1 / 2), -math.sqrt(1 / 2)])

        elif bounce_zones[1] < ball_middle < bounce_zones[2]:
            if self.ball.direction[0] < 0:
                self.ball.bounce([1, 0])
            else:
                self.ball.bounce([-1, 0])

        elif bounce_zones[2] <= ball_middle <= bounce_zones[3]:
            if self.ball.direction[0] < 0:
                self.ball.bounce([math.sqrt(1 / 2), math.sqrt(1 / 2)])
            else:
                self.ball.bounce([-math.sqrt(1 / 2), math.sqrt(1 / 2)])

        self.switch_ball_owner()
        self.ball.critical_zone['flag'] = False

    def score(self):
        """
        Handles the score logic
        :return:
        """
        self.send_stop_signals()
        self.ball_owner.score += 1
        print(f"Player 1: {self.player1.score} - "
              f"Player 2: {self.player2.score}")
        self.switch_ball_owner()
        self.reset()

    def switch_ball_owner(self):
        """
        Switches the ball owner and receiver
        :return:
        """
        if self.ball_owner == self.player1:
            self.ball_owner = self.player2
            self.ball_receiver = self.player1
            critical_zone = Dimensions.ball_critical_pos['player1']

        else:
            self.ball_owner = self.player1
            self.ball_receiver = self.player2
            critical_zone = Dimensions.ball_critical_pos['player2']

        self.ball.critical_zone['x1'] = critical_zone[0]
        self.ball.critical_zone['x2'] = critical_zone[1]

    def reset(self):
        """
        Resets the game after a score
        :return:
        """
        self.ball.thread.join()
        self.canvas.fill(Colors.canvas)
        for player in self.players:
            player.reset()
        self.start_player_threads()

    def send_stop_signals(self):
        """
        Sends stop signals to all threads
        :return:
        """
        self.ball.runner_signal = False
        for player in self.players:
            player.runner_signal = False

    def start_player_threads(self):
        """
        Starts the player threads and spawns the ball
        :return:
        """
        for player in self.players:
            player.runner_signal = True
            player.thread.start()
        # Spawn ball
        self.ball_owner.spawn_ball()
        self.ball = self.ball_owner.ball

    def keyboard_event(self, event: QtGui.QKeyEvent):
        """
        Handles the keyboard events and passes them to the players
        :param event:
        :return:
        """
        if event.key() in self.player1.keys.keys():
            self.player1.keyboard_event(event)
        elif event.key() in self.player2.keys.keys():
            self.player2.keyboard_event(event)
        else:
            return
