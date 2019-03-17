import cv2
import image_analysis.image_analysys as analysys


def update_environment_parameters(frame):
    # cv2.imshow('client', frame)
    cv2.imshow('processed', analysys.process_image(frame)['frame'])
    cv2.waitKey(1)
