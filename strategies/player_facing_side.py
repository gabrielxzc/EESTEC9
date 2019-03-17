import time
import combos.common as combo
import globals_vars


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
