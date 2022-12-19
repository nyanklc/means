import cv2 as cv
from stream_getter import StreamGetter
from agent import Agent
from serial_handler import SerialHandler
import time
import numpy as np
import serial
from params import *

def main():
    # serial
    if SERIAL_ON:
        serialh = SerialHandler(SERIAL_PORT, SERIAL_BAUDRATE)

    # init modules
    stream_getter = StreamGetter(VIDEO_SOURCE)
    stream_getter.startStream()
    frame = stream_getter.getFrame()
    agent = Agent(TURN_TOLERANCE, VIEW_MODE, QR_LENGTH, REFERENCE_IMG_PATH, QR_ENABLED, CONTOUR_ENABLED, MIDP_ENABLED, KNN_ENABLED, OBJ_LENGTH)

    # camera calibration
    if CALIBRATE_MODE:
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
        if not agent.isCalibrated():
            agent.setFocalLength(FOCAL_LENGTH)
    else:
        agent.setFocalLength(FOCAL_LENGTH)

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
        process_results_qr_distance, process_results_obj_corners, process_results_obj_distance = agent.process(frame)
        controls = []
        if (process_results_qr_distance != None) and (process_results_obj_corners != None):
            controls = agent.generateControls(process_results_qr_distance, process_results_obj_corners, process_results_obj_distance)

        # output
        if VIEW_MODE:
            agent.draw(frame)
            cv.imshow('agent', frame)
        if FPS_ON:
            print("MAIN: " + str(1/(new_frame_time-prev_frame_time)))
            prev_frame_time = new_frame_time
        if SERIAL_ON:
            controls = process_results_obj_distance ####################################
            serialh.sendMsg(controls)
            if ARDUINO_RESPONSE_ON:
                arduino_response = serialh.getMsg()
                if arduino_response is not None:
                    print(arduino_response)

    stream_getter.endStream()


if __name__ == "__main__":
    main()
