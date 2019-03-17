import cv2
import image_analysis.image_analysys as analysis
import globals_vars
import time


def update_environment_parameters(frame):
    info = analysis.process_image(frame)

    globals_vars.LEFT_PLAYER_X = info['left_pl_x']
    globals_vars.LEFT_PLAYER_Y = info['left_pl_y']
    globals_vars.RIGHT_PLAYER_X = info['right_pl_x']
    globals_vars.RIGHT_PLAYER_Y = info['right_pl_y']
    globals_vars.LAST_FRAME = info['frame']
    globals_vars.NUMBER_OF_FRAMES_SINCE_LAST_FACING_SIDE_CHECK += 1
