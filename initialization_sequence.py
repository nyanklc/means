import cv2 as cv

def initFocalLength():
    print("starting focal length calibration")
    measured_distance = input("input distance to object")
    real_width = input("input real width of the object")
