from PySide6 import QtGui


class KeyBinds:
    player1 = [
        87,  # W
        83,  # S
        70  # F
    ]
    player2 = [
        79,  # O
        76,  # L
        74  # J
    ]


class Colors:
    canvas = QtGui.QColor('black')
    neutral = QtGui.QColor('white')
    player1 = QtGui.QColor('red')
    player2 = QtGui.QColor('blue')


class Dimensions:
    canvas = {
        'width': 1024,
        'height': 768
    }
    player = {
        'size': 100,
        'thickness': 20
    }
    ball = 20
    center_player_y = canvas['height'] / 2 - player['size'] / 2
    center_ball_on_player_y = player['size'] / 2 - ball / 2
