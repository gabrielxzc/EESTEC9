import cv2
import image_analysis.image_analysys as analysys


def update_environment_parameters(frame):
    # processed_results = analysys.process_image(frame)
    # cv2.imshow('processed', processed_results['frame'])
    cv2.imwrite('frame-scorpion-down.png', frame)
    cv2.waitKey(1)
