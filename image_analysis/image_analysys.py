import time
import cv2
import numpy as np
import sklearn.cluster as sk

previous = None

def get_player_health(player_healthbar):
    return np.count_nonzero(player_healthbar)

def get_yellowed_image(frame):
    # BGR FOR YELLOW
    bgr = [82, 199, 235]
    hsv = cv2.cvtColor(np.uint8([[bgr]]), cv2.COLOR_BGR2HSV)[0][0]

    minHSV = np.array([hsv[0] - 10, hsv[1] - 60, hsv[2] - 220])
    maxHSV = np.array([hsv[0] + 8, hsv[1] + 60, hsv[2] + 220])
    maskHSV = cv2.inRange(frame, minHSV, maxHSV)

    return maskHSV


def get_blued_image(frame):
    lower_blue = np.array([70, 50, 50])
    upper_blue = np.array([120, 255, 255])
    mask = cv2.inRange(frame, lower_blue, upper_blue)
    return mask

def draw_player(frame, players):
    for idx in (0, 1):

        size_y = len(frame)

        x = int(players[idx][0]+ 0.25 * size_y)
        y = int(players[idx][1])



        for _x in range(x - 20, x + 20):
            for _y in range(y - 40, y + 40):
                frame[_x][_y][0] = 0
                frame[_x][_y][1] = 0
                frame[_x][_y][2] = 255

    return frame

def check_teleport(actual):
    global previous
    if previous is None:
        previous = actual
        return False
    rez = abs(actual - previous) > 20
    previous = actual
    return rez

# merged_players_image = cv2.bitwise_or(get_blued_image(processed_image), get_yellowed_image(processed_image))
def get_players_centroids(processed_image):
    merged_players_image = np.bitwise_or(get_blued_image(processed_image), get_yellowed_image(processed_image))
    merged_players_image = cv2.fastNlMeansDenoising(merged_players_image,searchWindowSize=13, h=79)

    x = np.where(merged_players_image != 0)
    xy_coo = np.array([x[0], x[1]]).T

    teleported = check_teleport(len(xy_coo))

    k_means = sk.KMeans(n_clusters=2, random_state=0, max_iter=2).fit(xy_coo)
    kcc = k_means.cluster_centers_
    return (kcc,teleported)


def process_image(image):

    process_results = {}

    size_y = len(image)
    size_x = len(image[0])

    health_bar = image[range(int(0.18 * size_y), int(0.20 * size_y)), :]
    processed_health_bar = cv2.cvtColor(health_bar, cv2.COLOR_BGR2GRAY)
    #
    #
    p1_healthbar = health_bar[:, range(0, int(size_x / 2) - 6)]
    p2_healthbar = health_bar[:, range(int(size_x / 2) + 6, size_x)]
    #
    # print("P1 health: ", get_player_health(p1_healthbar))
    # print("P2 health: ", get_player_health(p2_healthbar))

    particular_image = image[range(int(0.25 * size_y), int(0.8 * size_y)), :]

    processed_image = cv2.cvtColor(particular_image, cv2.COLOR_BGR2HSV)

    kcc,teleported = get_players_centroids(processed_image)
    # print(kcc)
    # print("Colors for left player:",full_image[int(kcc[0][0] + 0.25*size_y),int(kcc[0][1])])
    #
    # print("Colors for right player:",full_image[int(kcc[1][0]+0.25*size_y),int(kcc[1][1])])

    players = [(kcc[0][0], kcc[0][1]), (kcc[1][0], kcc[1][1])]

    after_draw = draw_player(image, players)

    process_results["frame"] = after_draw
    process_results["enemy_teleported"] = teleported

    process_results["left_pl_x"] = kcc[0][0]
    process_results["left_pl_y"] = kcc[0][1]

    process_results["right_pl_x"] = kcc[1][0]
    process_results["right_pl_y"] = kcc[1][0]

    process_results["p1_health"] = get_player_health(p1_healthbar)
    process_results["p2_health"] = get_player_health(p2_healthbar)

    return process_results

# full_image = cv2.imread('subz_subz.png')
# start = time.time()
# process_result = process_image(full_image)
# print(time.time() - start)
# cv2.imshow("final", process_result["frame"])
# k = cv2.waitKey(0)
#
# cv2.destroyAllWindows()

#
# for window_size in range(1, 22, 2):
#     print("Try number %d" % window_size)
#     total_time = 0
#     total_tries = 0
#     for i in range(0, 20):
#         st = time.time()
#         after_draw = process_image(full_image, window_size)
#         total_time += time.time() - st
#         total_tries += 1
#
#     print("Average time for %f tries: %f" % (total_time/total_tries, total_tries))
