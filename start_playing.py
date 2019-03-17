import threading
import socketio
from time import sleep
import combos.common as combo
import combos.scorpion.moves as scorpion
from environment.environment_observer import environment_worker
from environment.environment_parameter_updater import update_environment_parameters

IP = "0.0.0.0"
PORT = 5005

environment_worker = threading.Thread(target=environment_worker,
                                      args=(IP, PORT, update_environment_parameters,))
environment_worker.start()

sio = socketio.Client()
sio.connect('http://10.81.176.102')

while True:
    pass
    # facing_direction = combo.MOVE_LEFT
    # scorpion.combo_2(facing_direction, sio)
    # sleep(5)
