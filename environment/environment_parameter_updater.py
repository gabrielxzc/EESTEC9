import cv2
import image_analysis.image_analysys as analysis
import globals_vars
import time


def update_environment_parameters(frame):
    global frame_count
    info = analysis.process_image(frame)

    globals_vars.LEFT_PLAYER_X = info['left_pl_x']
    globals_vars.LEFT_PLAYER_Y = info['left_pl_y']
    globals_vars.RIGHT_PLAYER_X = info['right_pl_x']
    globals_vars.RIGHT_PLAYER_Y = info['right_pl_y']
    globals_vars.ENEMY_TELEPORTING = info['enemy_teleported']
    globals_vars.LAST_FRAME = info['frame']

    cv2.imshow('client', info['frame'])
    cv2.waitKey(1)
