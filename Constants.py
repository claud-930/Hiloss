import math

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
    ball_critical_pos = {
        'player1': [
            0,
            int(player['thickness'])
        ],
        'player2': [
            int(canvas['width'] - player['thickness'] - ball),
            canvas['width']
        ]
    }
    bounce_offsets = {
        'y0': 0,
        'y1': int(player['size'] / 3),
        'y2': int(player['size'] / 3 * 2),
        'y3': player['size']
    }
    bounce_angles = {
        '45': math.sqrt(1/2)
    }
