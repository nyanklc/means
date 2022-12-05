import cv2 as cv
from stream_getter import StreamGetter
from agent import Agent
import time
import numpy as np
from imutils import paths
import imutils
import initialization_sequence
import serial

VIDEO_SOURCE = 'http://nyn_cam:Means1122@192.168.43.1:8080/video'
#VIDEO_SOURCE = 1
VIEW_MODE = False
FPS_ON = True
NO_FRAME_FPS_ON = False

TURN_TOLERANCE = 50 # pixels

def displayQRBounds(im, bbox):
    n = len(bbox)
    for j in range(n):
        cv.line(im, tuple(bbox[j][0]), tuple(bbox[ (j+1) % n][0]), (255,0,0), 3)

def main():
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.reset_input_buffer()

    stream_getter = StreamGetter(VIDEO_SOURCE)
    stream_getter.startStream()
    frame = stream_getter.getFrame()

    agent = Agent(TURN_TOLERANCE, VIEW_MODE)

    prev_frame_time = 0
    new_frame_time = 0
    old_frame = frame

    initialization_sequence.initFocalLength()

    while True:
        new_frame_time = time.time()

        # quit application
        if VIEW_MODE:
            if cv.waitKey(2) == 27:
                break

        frame = stream_getter.getFrame()

        if not stream_getter.getRetrieved():
            print("Can't retrieve frame. Exiting...")
            break

        if np.array_equal(frame, old_frame):
            if NO_FRAME_FPS_ON:
                print("MAIN BREAK: " + str(1/(new_frame_time-prev_frame_time)))
                prev_frame_time = new_frame_time
            continue
        else:
            old_frame = frame
            # process frame here
            agent.process(frame)
            response = agent.keepQRInMid(frame)
            if response is not None:
                ser.write((str(response)+'/n').encode('utf-8'))
                print("sent ")
                print(response)
                line = ser.readline().decode('utf-8').rstrip()
                print(line)
            if VIEW_MODE:
                #agent.draw(frame)
                cv.imshow('agent', frame)

        if FPS_ON:
            print("MAIN: " + str(1/(new_frame_time-prev_frame_time)))
            prev_frame_time = new_frame_time

    stream_getter.endStream()


if __name__ == "__main__":
    main()
