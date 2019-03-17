import combos.common as combo
import combos.scorpion.moves as scorpion
import socketio
import random
from time import sleep

possible_moves = [scorpion.teleport, scorpion.takedown, scorpion.combo_1, scorpion.spear, scorpion.forward_2,
                  scorpion.backward_2, scorpion.backward_3, scorpion.forward_4]

sio = socketio.Client()
sio.connect('http://10.81.176.102')

while True:
    facing_direction = random.choice([combo.MOVE_LEFT, combo.MOVE_RIGHT])
    random.choice(possible_moves)(facing_direction, sio)
    sleep(0.2)
