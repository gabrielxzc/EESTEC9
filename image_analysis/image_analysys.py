import time
import cv2
import numpy as np
import sklearn.cluster as sk
import random
import globals_vars

previous = None
prev_centroid_left = None
prev_centroid_right = None
previous_hearth_player1 = None
previous_hearth_player2 = None


def initialize_centroids(width, height):
    global prev_centroid_left, prev_centroid_right

    prev_centroid_left = [int(0.65 * height), int(0.04 * width)]
    prev_centroid_right = [int(0.65 * height), int(0.96 * width)]


def get_players_hearts(top_heart_bar):
    size_x = len(top_heart_bar[0])

    processed_health_bar = cv2.cvtColor(top_heart_bar, cv2.COLOR_BGR2GRAY)

    ret, thresh1 = cv2.threshold(processed_health_bar, 50, 255, cv2.THRESH_BINARY)

    p1_healthbar = thresh1[:, range(0, int(size_x / 2))]
    p2_healthbar = thresh1[:, range(int(size_x / 2), size_x)]

    p1_health = np.count_nonzero(p1_healthbar)
    p2_health = np.count_nonzero(p2_healthbar)

    return p1_health, p2_health


def get_yellowed_image(frame):
    # BGR FOR YELLOW
    bgr = [82, 199, 235]
    hsv = cv2.cvtColor(np.uint8([[bgr]]), cv2.COLOR_BGR2HSV)[0][0]

    # minHSV = np.array([hsv[0] - 10, hsv[1] - 60, hsv[2] - 220])
    # maxHSV = np.array([hsv[0] + 8, hsv[1] + 60, hsv[2] + 220])
    minHSV = np.array([hsv[0] - 80, hsv[1] - 35, hsv[2] - 220])
    maxHSV = np.array([hsv[0] + 80, hsv[1] + 35, hsv[2] + 220])
    maskHSV = cv2.inRange(frame, minHSV, maxHSV)

    return maskHSV


def get_blued_image(frame):
    bgr = [154, 104, 75]
    hsv = cv2.cvtColor(np.uint8([[bgr]]), cv2.COLOR_BGR2HSV)[0][0]

    minHSV = np.array([hsv[0] - 20, hsv[1] - 60, hsv[2] - 60])
    maxHSV = np.array([hsv[0] + 20, hsv[1] + 60, hsv[2] + 50])
    maskHSV = cv2.inRange(frame, minHSV, maxHSV)

    return maskHSV


def draw_player(frame, players):
    for idx in (0, 1):

        size_y = len(frame)

        x = int(players[idx][0])
        y = int(players[idx][1])

        for _x in range(x - 2, x + 2):
            for _y in range(y - 2, y + 2):
                frame[_x][_y][0] = 0
                frame[_x][_y][1] = 0
                frame[_x][_y][2] = 255

    return frame


#
# def check_teleport(actual):
#     global previous
#     if previous is None:
#         previous = actual
#         return False
#     rez = abs(actual - previous) > 20
#     previous = actual
#     return rez


def check_player_down(centroid, width):
    return centroid[0] / width > 0.58


def check_players_down(kcc, width):
    return check_player_down(kcc[0], width), check_player_down(kcc[1], width)


def check_screen_for_teleport(frame):
    # BGR FOR CYAN
    bgr = [245, 246, 161]
    hsv = cv2.cvtColor(np.uint8([[bgr]]), cv2.COLOR_BGR2HSV)[0][0]

    minHSV = np.array([hsv[0] - 10, hsv[1] - 10, hsv[2] - 180])
    maxHSV = np.array([hsv[0] + 10, hsv[1] + 60, hsv[2] + 220])
    maskHSV = cv2.inRange(frame, minHSV, maxHSV)

    pixels = np.count_nonzero(maskHSV)
    globals_vars.ENEMY_TELEPORTING = pixels > 50


def check_screen_for_spear(full_image):
    size_y = len(full_image)

    spear_frame = full_image[range(int(0.597 * size_y), int(0.67 * size_y)), :]

    frame = cv2.cvtColor(spear_frame, cv2.COLOR_BGR2HSV)
    # BGR FOR YELLOW
    bgr = [144, 133, 129]
    hsv = cv2.cvtColor(np.uint8([[bgr]]), cv2.COLOR_BGR2HSV)[0][0]

    minHSV = np.array([hsv[0] - 15, hsv[1] - 10, hsv[2] - 97])
    maxHSV = np.array([hsv[0] + 15, hsv[1] + 20, hsv[2] + 100])
    maskHSV = cv2.inRange(frame, minHSV, maxHSV)

    # cv2.imshow("spear", maskHSV)
    # k = cv2.waitKey(0)
    #
    # print("spear count:", np.count_nonzero(maskHSV))

    spear_denoisified = cv2.fastNlMeansDenoising(maskHSV, searchWindowSize=13, h=59)
    # cv2.imshow("spear", spear_denoisified)
    # k = cv2.waitKey(0)

    print("spear count:", np.count_nonzero(spear_denoisified))
    globals_vars.ENEMY_SPEAR = np.count_nonzero(spear_denoisified) > 5000


    # spear = check_screen_for_spear(processed_image)


def get_players_centroids(processed_image, initial_width, initial_height):
    merged_players_image = np.bitwise_or(get_blued_image(processed_image), get_yellowed_image(processed_image))
    # merged_players_image = cv2.fastNlMeansDenoising(merged_players_image,searchWindowSize=13, h=79)

    # cv2.imshow("merged", merged_players_image)
    # k = cv2.waitKey(0)
    x = np.where(merged_players_image != 0)
    xy_coo = np.array([x[0], x[1]]).T

    global prev_centroid_right, prev_centroid_left
    if prev_centroid_right == None or prev_centroid_left == None:
        initialize_centroids(initial_width, initial_height)

    centroids_for_initalization = [] + prev_centroid_left + prev_centroid_right

    randomness = random.randint(0, 5)

    k_means = ""
    if randomness == 0:
        k_means = sk.KMeans(n_clusters=2, random_state=1, max_iter=5, n_init=10).fit(xy_coo)
    else:
        k_means = sk.KMeans(n_clusters=2, random_state=0, max_iter=5, n_init=1,
                            init=np.array(centroids_for_initalization).reshape(2, 2)).fit(xy_coo)

    kcc = k_means.cluster_centers_
    # print(kcc)

    # xy_coo_2 = np.fromfunction(lambda i: xy_coo[i] if min(np.linalg.norm(xy_coo[i]-kcc[0]), np.linalg.norm(xy_coo[i]-kcc[1])) > 20 else None,\
    #                            (len(xy_coo), ), dtype=int)
    # xy_coo_2 = xy_coo_2[xy_coo_2 is not None]

    xy_coo_2 = [xy_coo[i] for i in range(len(xy_coo)) if
                min(np.linalg.norm(xy_coo[i] - kcc[0]), np.linalg.norm(xy_coo[i] - kcc[1])) < 30]
    k_means = sk.KMeans(n_clusters=2, random_state=0, max_iter=5, n_init=1, init=np.reshape(kcc, (2, 2))).fit(xy_coo_2)
    kcc = k_means.cluster_centers_

    prev_centroid_left = kcc[0].tolist()
    prev_centroid_right = kcc[1].tolist()

    # print(kcc)

    # cv2.imshow("merged", merged_players_image)
    # k = cv2.waitKey(0)

    return kcc


def process_image(image):
    size_y = len(image)
    size_x = len(image[0])
    image_for_tp_check = image[range(int(0.55 * size_y), int(0.88 * size_y)), :]
    hsv_tp_check = cv2.cvtColor(image_for_tp_check, cv2.COLOR_BGR2HSV)
    check_screen_for_teleport(hsv_tp_check)

    check_screen_for_spear(image)

    process_results = {}

    health_bars = image[range(int(0.18 * size_y), int(0.20 * size_y)), :]

    p1_health, p2_health = get_players_hearts(health_bars)
    global previous_hearth_player1, previous_hearth_player2

    if previous_hearth_player1 == None or previous_hearth_player2 == None:
        previous_hearth_player1 = p1_health
        previous_hearth_player2 = p2_health

    if p1_health < 0.95 * previous_hearth_player1:
        process_results["p1_is_hit"] = True

    if p2_health < 0.95 * previous_hearth_player2:
        process_results["p2_is_hit"] = True

    previous_hearth_player1 = p1_health
    previous_hearth_player2 = p2_health

    particular_image = image[range(int(0.25 * size_y), int(0.8 * size_y)), :]

    processed_image = cv2.cvtColor(particular_image, cv2.COLOR_BGR2HSV)

    kcc = get_players_centroids(processed_image, len(image), len(image[0]))

    players = [(kcc[0][0] + 0.25 * size_y, kcc[0][1]), (kcc[1][0] + 0.25 * size_y, kcc[1][1])]

    after_draw = draw_player(image, players)

    process_results["frame"] = after_draw
    # process_results["enemy_teleported"] = check_screen_for_teleport(processed_image)

    if kcc[0][1] < kcc[1][1]:
        left_x, left_y = kcc[0][1], kcc[0][0]
        right_x, right_y = kcc[1][1], kcc[1][0]
    else:
        left_x, left_y = kcc[1][1], kcc[1][0]
        right_x, right_y = kcc[0][1], kcc[0][0]

    process_results["left_pl_x"] = left_x
    process_results["left_pl_y"] = left_y

    process_results["right_pl_x"] = right_x
    process_results["right_pl_y"] = right_y

    process_results["p1_health"] = p1_health
    process_results["p2_health"] = p2_health

    return process_results

# full_image = cv2.imread('frame-scorpion-down.png')
# full_image = cv2.imread(
#     '/Users/alexmititelu/Documents/Work/HackathonEESTEC_REPO/EESTEC9/frames/teleport-frame4.png')
# full_image = cv2.imread('frame1.png')
# full_image = cv2.imread('frame0.png')
#
# frame =cv2.cvtColor(full_image, cv2.COLOR_BGR2HSV)
# # spear = check_screen_for_spear(frame)
# tp = check_screen_for_teleport(frame)
# print(tp)
# cv2.imshow("teleport", tp)
# k = cv2.waitKey(0)
#
#
# #
# start = time.time()
# process_result = process_image(full_image)
# print(time.time() - start)
# cv2.imshow("final", process_result["frame"])
# k = cv2.waitKey(0)
