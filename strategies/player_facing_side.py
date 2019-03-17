import time
import combos.common as combo
import globals_vars
from time import sleep


def get_facing_side_by_jumping(sio):
    initial_left_player_y = globals_vars.LEFT_PLAYER_Y
    initial_right_player_y = globals_vars.RIGHT_PLAYER_Y

    left_player_y_max_diff = 0
    right_player_y_max_diff = 0

    start_jump = time.time()

    combo.press_move(combo.MOVE_UP, 0.1, 0.1, sio)

    while True:
        left_player_y_max_diff = max(left_player_y_max_diff, globals_vars.LEFT_PLAYER_Y - initial_left_player_y)
        right_player_y_max_diff = max(right_player_y_max_diff, globals_vars.RIGHT_PLAYER_Y - initial_right_player_y)

        if time.time() - start_jump >= 2.0:
            break

    if left_player_y_max_diff > right_player_y_max_diff:
        return combo.MOVE_RIGHT

    return combo.MOVE_LEFT


def get_facing_side_by_ducking(sio):
    number_of_tries = 0
    max_number_of_tries = 500

    combo.emit(combo.MOVE_DOWN, True, sio)
    sleep(0.1)

    combo.emit(combo.MOVE_R2_BLOCK, True, sio)
    sleep(0.5)

    while True:
        if number_of_tries > max_number_of_tries:
            facing_side = None
            break

        number_of_tries += 1

        if globals_vars.LEFT_PLAYER_Y / len(globals_vars.LAST_FRAME) > 0.4 and \
                globals_vars.RIGHT_PLAYER_Y / len(globals_vars.LAST_FRAME) > 0.4:
            continue
        elif globals_vars.LEFT_PLAYER_Y / len(globals_vars.LAST_FRAME) > 0.4:
            facing_side = combo.MOVE_RIGHT
            break
        elif globals_vars.RIGHT_PLAYER_Y / len(globals_vars.LAST_FRAME) > 0.4:
            facing_side = combo.MOVE_LEFT
            break

    combo.emit(combo.MOVE_DOWN, False, sio)
    sleep(0.1)

    combo.emit(combo.MOVE_R2_BLOCK, False, sio)
    sleep(0.1)

    return facing_side
