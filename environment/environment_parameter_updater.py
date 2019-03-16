import cv2


def update_environment_parameters(frame):
    cv2.imshow('client', frame)
    cv2.waitKey(1)
