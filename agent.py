import cv2 as cv
import math
from camera_calibrator import CameraCalibrator
from mid_point_tracker import MidPointTracker
from contour_finder import ContourFinder
from QR_finder import QRFinder

class Agent:
    def __init__(self, turn_tolerance, VIEW_MODE, real_QR_length):
        self.turn_tolerance_ = turn_tolerance
        self.VIEW_MODE = VIEW_MODE
        self.calibrated_ = False
        self.focal_length_ = -1
        self.camera_calibrator = CameraCalibrator(self)
        self.mid_point_tracker = MidPointTracker(self)
        self.contour_finder = ContourFinder(self)
        self.QR_finder = QRFinder(self, real_QR_length)

    def process(self, frame):
        try:
            # process
            self.QR_finder.detectQR(frame)
            self.contour_finder.findContours(frame)
            self.mid_point_tracker.findFrameMid(frame)
            self.QR_finder.drawDistance(frame)
        except:
            print("agent couldn't process frame")
            return

    def generateControls(self):
        # TODO
        pass # should return the control data for camera mount and motors

    def draw(self, frame):
        if self.VIEW_MODE:
            self.QR_finder.drawBounds(frame)
            self.QR_finder.drawMidPoint(frame)
            self.QR_finder.drawDistance(frame)
            self.contour_finder.drawContours(frame)
            self.mid_point_tracker.drawPoint(frame)

    def getFocalLength(self):
        return self.focal_length_

    def initFocalLengthCalibration(self, frame):
        print("starting focal length calibration")
        print("make sure the qr code faces the camera los perpendicularly")
        measured_distance = float(input("input distance to object: "))
        real_width = float(input("input real width of the object: "))
        self.QR_finder.detectQR(frame)
        if not self.QR_finder.isDetected():
            print("QR Code not detected")
            return False
        width_in_rf_image = self.QR_finder.getQRLength()
        self.focal_length_ = self.camera_calibrator.calculateFocalLength(measured_distance, real_width, width_in_rf_image)
        self.camera_calibrator.getCameraParameters()
        if (self.focal_length_ != -1) or (self.focal_length_ != None):
            self.calibrated_ = True
            print("focal length calculated: " + str(self.focal_length_))
        return  True
    
    def isCalibrated(self):
        return self.calibrated_

