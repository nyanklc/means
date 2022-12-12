import cv2 as cv
from stream_getter import StreamGetter
from agent import Agent
import time
import numpy as np
import serial
from params import *

def main():
    # serial
    if SERIAL_ON:
        ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        ser.reset_input_buffer()

    # init modules
    stream_getter = StreamGetter(VIDEO_SOURCE)
    stream_getter.startStream()
    frame = stream_getter.getFrame()
    agent = Agent(TURN_TOLERANCE, VIEW_MODE, QR_LENGTH, REFERENCE_IMG_PATH, QR_ENABLED, CONTOUR_ENABLED, MIDP_ENABLED, BF_ENABLED)

    # camera calibration
    if (not agent.isCalibrated()) and CALIBRATE_MODE:
        trials = 0
        camera_calibration_required = input("start camera calibration ? (y/n)")
        while camera_calibration_required != 'n':
            if camera_calibration_required == 'y':
                if agent.initFocalLengthCalibration(stream_getter.getFrame()):
                    if agent.isCalibrated():
                        break
                else:
                    trials += 1
                    if not QR_ENABLED:
                        exit()
                    if trials == CALIBRATE_MODE_TRIAL_COUNT:
                        print("Camera calibration failed, terminating.")
                        exit()
                    continue

            camera_calibration_required = input("start camera calibration ? (y/n)")

    # fps
    prev_frame_time = 0
    new_frame_time = 0
    old_frame = frame

    # main loop
    while True:
        new_frame_time = time.time()

        # quit application
        if VIEW_MODE:
            if cv.waitKey(2) == 27:
                break

        # get frame
        frame = stream_getter.getFrame()
        if not stream_getter.getRetrieved():
            print("Can't retrieve frame. Exiting...")
            break
        if np.array_equal(frame, old_frame):
            if NO_FRAME_FPS_ON:
                print("MAIN BREAK: " + str(1/(new_frame_time-prev_frame_time)))
                prev_frame_time = new_frame_time
            continue
        old_frame = frame
        frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # process frame
        agent.process(frame)
        controls = agent.generateControls()

        # output
        if VIEW_MODE:
            agent.draw(frame)
            cv.imshow('agent', frame)
        if FPS_ON:
            print("MAIN: " + str(1/(new_frame_time-prev_frame_time)))
            prev_frame_time = new_frame_time

    stream_getter.endStream()


if __name__ == "__main__":
    main()
