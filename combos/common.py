from time import sleep

PLAYER_KEY = 'fjm30c2qa05t3e43'
# PLAYER_KEY = 'thickunnqcrv6a23'

MOVE_1 = MOVE_SQUARE = 'front_punch'
MOVE_2 = MOVE_TRIANGLE = 'back_punch'
MOVE_3 = MOVE_X = 'front_kick'
MOVE_4 = MOVE_CIRCLE = 'back_kick'
MOVE_UP = 'up'
MOVE_DOWN = 'down'
MOVE_LEFT = 'left'
MOVE_RIGHT = 'right'
MOVE_L1_THROW = 'throw'
MOVE_R2_BLOCK = 'block'
MOVE_R1_INTERACTION = 'interact'


def get_opposite_direction(direction):
    if direction == MOVE_RIGHT:
        return MOVE_LEFT

    return MOVE_RIGHT


def emit(command, value, sio):
    cmd = {
        'key': PLAYER_KEY,
        'commands': {
            command: value
        }
    }

    sio.emit('command', cmd)


def press_move(move, time_after_press, time_after_release, sio):
    emit(move, True, sio)
    sleep(time_after_press)
    emit(move, False, sio)
    sleep(time_after_release)


def press_double_move(move_one, time_after_move_one_press, move_two, time_after_move_two_press,
                      time_after_move_one_release, time_after_move_two_release, sio):
    emit(move_one, True, sio)
    sleep(time_after_move_one_press)

    emit(move_two, True, sio)
    sleep(time_after_move_two_press)

    emit(move_one, False, sio)
    sleep(time_after_move_one_release)

    emit(move_two, False, sio)
    sleep(time_after_move_two_release)
