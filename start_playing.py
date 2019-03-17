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

IP = "0.0.0.0"
PORT = 5005

environment_worker = threading.Thread(target=environment_worker,
                                      args=(IP, PORT, update_environment_parameters,))
environment_worker.start()

sio = socketio.Client()
sio.connect('http://10.81.176.102')

possible_actions = [scorpion.spear, scorpion.takedown, scorpion.combo_1, scorpion.teleport]

while True:
    if globals_vars.LAST_FRAME is not None:
        break

while True:
    print('Trying to detect side I\'m on by ducking ...')
    facing_side = strategies.player_facing_side.get_facing_side_by_ducking(sio)

    if facing_side is None:
        print('Could not determine side I\'m facing, will go into safe move and try to determine facing side again ...')
        scorpion.forward_2(globals_vars.CURRENT_FACING_SIDE, sio)
    else:
        print('Detected I\'m on facing the ' + str(facing_side) + ' side!')

    '''
    if globals_vars.ENEMY_TELEPORTING:
        print('Detected enemy teleporting, starting block and then counter-combo ...')
        combo.press_move(combo.MOVE_R2_BLOCK, 1, 0.1, sio)
        scorpion.combo_1(facing_side, sio)
    elif abs(globals_vars.LEFT_PLAYER_X - globals_vars.RIGHT_PLAYER_X) <= 100:
        print('Detected enemy is close by on X axis, starting combo ...')
        scorpion.combo_1(facing_side, sio)
    else:
        print('Enemy is far away, waiting for him to get close ...')
        sleep(0.5)
    '''
