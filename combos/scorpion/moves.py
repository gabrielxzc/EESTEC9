import combos.common as combo


def forward_2(direction_facing, sio):
    combo.press_double_move(direction_facing, 0.1, combo.MOVE_2, 0.1, 0.1, 0.65, sio)


def backward_2(direction_facing, sio):
    combo.press_double_move(combo.get_opposite_direction(direction_facing), 0.1, combo.MOVE_2, 0.1, 0.1, 0.4, sio)


def teleport(direction_not_facing, sio):
    combo.press_move(combo.MOVE_DOWN, 0.05, 0.05, sio)
    combo.press_double_move(direction_not_facing, 0.1, combo.MOVE_3, 0.1, 0.1, 0.5, sio)


def combo_1(facing_direction, sio):
    forward_2(facing_direction, sio)
    combo.press_move(facing_direction, 0.2, 0.1, sio)
    combo.press_move(combo.MOVE_2, 0.1, 0.1, sio)
    combo.press_move(combo.MOVE_1, 0.1, 0.45, sio)
    combo.press_move(combo.MOVE_4, 0.1, 0.43, sio)
    teleport(combo.get_opposite_direction(facing_direction), sio)
    combo.press_move(combo.MOVE_2, 0.1, 0.1, sio)
    combo.press_move(combo.MOVE_1, 0.1, 0.45, sio)


def combo_2(facing_direction, sio):
    forward_2(facing_direction, sio)
    backward_2(facing_direction, sio)
    backward_2(facing_direction, sio)
    combo.press_move(combo.MOVE_SQUARE, 0.1, 0.1, sio)
    combo.press_move(combo.MOVE_SQUARE, 0.1, 0.1, sio)
