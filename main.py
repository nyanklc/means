import cv2 as cv
from stream_getter import StreamGetter
from agent import Agent
import time
import numpy as np
from imutils import paths
import imutils
import initialization_sequence

#VIDEO_SOURCE = 'http://nyn_cam:Means1122@192.168.1.92:8080/video'
VIDEO_SOURCE = 1
VIEW_MODE = True
FPS_ON = False

def displayQRBounds(im, bbox):
    n = len(bbox)
    for j in range(n):
        cv.line(im, tuple(bbox[j][0]), tuple(bbox[ (j+1) % n][0]), (255,0,0), 3)

def main():
    stream_getter = StreamGetter(VIDEO_SOURCE)
    stream_getter.startStream()
    frame = stream_getter.getFrame()

    agent = Agent()

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
            if FPS_ON:
                print("MAIN BREAK: " + str(1/(new_frame_time-prev_frame_time)))
                prev_frame_time = new_frame_time
            continue
        else:
            old_frame = frame
            # process frame here
            agent.process(frame)
            if VIEW_MODE:
                agent.draw(frame)
                cv.imshow('agent', frame)

        if FPS_ON:
            print("MAIN: " + str(1/(new_frame_time-prev_frame_time)))
            prev_frame_time = new_frame_time

    stream_getter.endStream()


if __name__ == "__main__":
    main()
