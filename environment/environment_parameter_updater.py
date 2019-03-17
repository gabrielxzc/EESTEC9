import cv2
import image_analysis.image_analysys as analysys


def update_environment_parameters(frame):
    cv2.imshow('processed', frame)
    cv2.imwrite('frames/frame-lower-hp-players.png', frame)
    # print(processed_results)
    cv2.waitKey(1)
