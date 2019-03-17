import threading
import socketio
from environment.environment_observer import environment_worker
from environment.environment_parameter_updater import update_environment_parameters
import strategies.player_facing_side
import combos.scorpion.moves as scorpion
import combos.common as combo
import random
from time import sleep
import globals_vars
import numpy as np

IP = "0.0.0.0"
PORT = 5005

environment_worker = threading.Thread(target=environment_worker,
                                      args=(IP, PORT, update_environment_parameters,))
environment_worker.start()

sio = socketio.Client()
sio.connect('http://10.81.176.102')

while True:
    if globals_vars.LAST_FRAME is not None:
        break

while True:
    if globals_vars.ENEMY_TELEPORTING:
        combo.press_move(combo.MOVE_R2_BLOCK, 0.3, 0.1, sio)
        scorpion.combo_1(combo.get_opposite_direction(globals_vars.CURRENT_FACING_SIDE), sio)
        globals_vars.CURRENT_FACING_SIDE = combo.get_opposite_direction(globals_vars.CURRENT_FACING_SIDE)
        print('Detected enemy teleported, blocked and parried him ...')
    elif globals_vars.NUMBER_OF_FRAMES_SINCE_LAST_FACING_SIDE_CHECK >= 60:
        print('Trying to detect side I\'m on by ducking ...')
        facing_side = strategies.player_facing_side.get_facing_side_by_ducking(sio)

        if facing_side is None:
            print('Could not determine side I\'m facing, will go into safe move' +
                  'and try to determine facing side again ...')
            scorpion.forward_2(globals_vars.CURRENT_FACING_SIDE, sio)
        else:
            print('Detected I\'m on facing the ' + str(facing_side) + ' side!')
            globals_vars.CURRENT_FACING_SIDE = facing_side
            scorpion.takedown(facing_side, sio)
            globals_vars.NUMBER_OF_FRAMES_SINCE_LAST_FACING_SIDE_CHECK = 0
    else:
        distance = abs(globals_vars.LEFT_PLAYER_X - globals_vars.RIGHT_PLAYER_X)
        if distance <= 100:
            print('CLOSE RANGE')
            scorpion.combo_1(globals_vars.CURRENT_FACING_SIDE, sio)
        elif distance <= 200:
            print('MID RANGE')
            if np.random.random_sample() < distance / 100:
                scorpion.teleport(globals_vars.CURRENT_FACING_SIDE, sio)
            else:
                scorpion.takedown(globals_vars.CURRENT_FACING_SIDE, sio)
        else:
            print('LONG RANGE')
            scorpion.spear(globals_vars.CURRENT_FACING_SIDE, sio)
