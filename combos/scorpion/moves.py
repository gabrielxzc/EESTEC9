import combos.common as combo
import socketio
from time import sleep


def forward_2(direction_facing, sio):  # OVERHEAD
    combo.press_double_move(direction_facing, 0.1, combo.MOVE_2, 0.1, 0.1, 0.65, sio)


def forward_4(direction_facing, sio):  # OVERHEAD
    combo.press_double_move(direction_facing, 0.1, combo.MOVE_4, 0.1, 0.1, 0.65, sio)


def backward_2(direction_facing, sio):
    combo.press_double_move(combo.get_opposite_direction(direction_facing), 0.1, combo.MOVE_2, 0.1, 0.1, 0.4, sio)


def backward_3(direction_facing, sio):  # LOW
    combo.press_double_move(combo.get_opposite_direction(direction_facing), 0.1, combo.MOVE_3, 0.1, 0.1, 0.4, sio)


def teleport(direction_facing, sio):
    combo.press_move(combo.MOVE_DOWN, 0.05, 0.05, sio)
    combo.press_double_move(combo.get_opposite_direction(direction_facing), 0.1, combo.MOVE_3, 0.1, 0.1, 0.5, sio)


def spear(direction_facing, sio):
    combo.press_move(combo.get_opposite_direction(direction_facing), 0.05, 0.05, sio)
    combo.press_double_move(direction_facing, 0.1, combo.MOVE_1, 0.1, 0.1, 0.5, sio)


def takedown(direction_facing, sio):
    combo.press_move(combo.get_opposite_direction(direction_facing), 0.05, 0.05, sio)
    combo.press_double_move(direction_facing, 0.1, combo.MOVE_4, 0.1, 0.1, 0.5, sio)


def combo_1(facing_direction, sio):  # CLOSE-MID RANGE
    forward_2(facing_direction, sio)
    backward_2(facing_direction, sio)
    backward_2(facing_direction, sio)
    sleep(0.2)
    combo.press_move(combo.MOVE_SQUARE, 0.3, 0.2, sio)


if __name__ == '__main__':
    sio = socketio.Client()
    sio.connect('http://10.81.176.102')
    teleport(combo.MOVE_RIGHT, sio)
    sleep(1)
    sio.disconnect()
