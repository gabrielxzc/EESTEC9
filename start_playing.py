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
    pass
