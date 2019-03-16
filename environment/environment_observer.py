import numpy as np
import cv2
import struct
import pickle
import socket

data = ''
payload_size = struct.calcsize(">L")

cur_frame = -1
last_frame = -1
frame_fragments = None
cur_fragments = 0
compression_ratio = 1


def init_frame_fragments():
    global frame_fragments, cur_fragments
    frame_fragments = None
    cur_fragments = 0


def decode_data(p):
    res = p[payload_size:]
    return pickle.loads(res)


def render_frame(callback):
    global compression_ratio
    frame = np.concatenate(frame_fragments)

    resized = cv2.resize(frame, (0, 0), fx=1 / compression_ratio, fy=1 / compression_ratio)
    callback(resized)

    init_frame_fragments()


def environment_worker(ip, port, callback):
    global frame_fragments, cur_fragments, last_frame, cur_frame
    global data, compression_ratio

    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP
    sock.bind((ip, port))

    while True:
        try:
            while len(data) < payload_size:
                data += sock.recv(65000)

            (metadata, fragment) = decode_data(data)

            data = ''
            (cur_frame, curFragment, max_fragments, compression_ratio) = metadata
            # check if we receive a new fragment or server has restarted
            if cur_frame - 20 > last_frame != -1:
                print('Mismatching stream', cur_frame, last_frame)
                # server or internet was restarted, lost too many frames, drop anything saved
                init_frame_fragments()
                last_frame = cur_frame

            # frame had some lost packets, but a new frame already arrived
            # so we forcefully render the last, incomplete frame
            forced_render = False
            if cur_frame > last_frame or cur_frame == 0:
                # some packets were lost along the way
                if max_fragments >= 10 and float(cur_fragments) / max_fragments > 0.9:
                    # if the frame has lost less than 10% of its required packets, still render it
                    empty_fragment = None
                    for index, elem in enumerate(frame_fragments):
                        if not (frame_fragments[index] is None):
                            empty_fragment = np.zeros(frame_fragments[index].shape, np.uint8)
                            break

                    for index, elem in enumerate(frame_fragments):
                        if frame_fragments[index] is None:
                            frame_fragments[index] = empty_fragment
                    render_frame(callback)
                    forced_render = True
                last_frame = cur_frame
                init_frame_fragments()

            if frame_fragments is None:
                # array of <None> with <max_fragments> elements
                frame_fragments = [None] * max_fragments

            frame_fragments[curFragment] = fragment
            cur_fragments += 1
            if cur_fragments == max_fragments and not forced_render:
                render_frame(callback)

            data = ''

        except Exception as e:
            print('error', e)
            init_frame_fragments()
            data = ''
