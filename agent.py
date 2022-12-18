import cv2 as cv
import math
from camera_calibrator import CameraCalibrator
from mid_point_tracker import MidPointTracker
from contour_finder import ContourFinder
from QR_finder import QRFinder
from feature_matcher import FeatureMatcher

class Agent:
    def __init__(self, turn_tolerance, VIEW_MODE, real_QR_length, REFERENCE_IMG_PATH, QR_ENABLED, CONTOUR_ENABLED, MIDP_ENABLED, KNN_ENABLED, OBJ_LENGTH):
        self.turn_tolerance_ = turn_tolerance
        self.VIEW_MODE = VIEW_MODE
        self.REFERENCE_IMG_PATH = REFERENCE_IMG_PATH
        self.calibrated_ = False
        self.focal_length_ = -1
        self.camera_calibrator = CameraCalibrator(self)
        self.mid_point_tracker = MidPointTracker(self)
        self.contour_finder = ContourFinder(self)
        self.QR_finder = QRFinder(self, real_QR_length)
        self.feature_matcher = FeatureMatcher(self, self.REFERENCE_IMG_PATH, OBJ_LENGTH)
        self.QR_ENABLED = QR_ENABLED
        self.CONTOUR_ENABLED = CONTOUR_ENABLED
        self.MIDP_ENABLED = MIDP_ENABLED
        self.KNN_ENABLED = KNN_ENABLED

    def process(self, frame):
        qr_dist = None
        obj_corners = None
        obj_distance = -1.0
        try:
            if self.QR_ENABLED:
                self.QR_finder.detectQR(frame)
                qr_dist = self.QR_finder.getDistance()
            if self.CONTOUR_ENABLED:
                self.contour_finder.findContours(frame)
            if self.MIDP_ENABLED:
                self.mid_point_tracker.findFrameMid(frame)
            if self.KNN_ENABLED:
                obj_corners = self.feature_matcher.findObject(frame)
                if obj_corners is not None:
                    obj_distance = self.feature_matcher.getDistance()
        except:
            print("agent couldn't process frame")
            return None

        return qr_dist, obj_corners, obj_distance

    def generateControls(self, qr_dist, obj_corners, obj_distance):
        # TODO: should return the control data for camera mount and motors
        controls = []
        return controls 

    def draw(self, frame):
        if self.VIEW_MODE:
            if self.QR_ENABLED:
                self.QR_finder.drawBounds(frame)
                self.QR_finder.drawMidPoint(frame)
                self.QR_finder.drawDistance(frame)
            if self.CONTOUR_ENABLED:
                self.contour_finder.drawContours(frame)
            if self.MIDP_ENABLED:
                self.mid_point_tracker.drawPoint(frame)
            if self.KNN_ENABLED:
                self.feature_matcher.drawMatches(frame)

    def getFocalLength(self):
        return self.focal_length_

    def initFocalLengthCalibration(self, frame):
        if self.KNN_ENABLED:
            print("starting focal length calibration")
            print("make sure the object faces the camera los perpendicularly")
            measured_distance = float(input("input distance to object: "))
            real_width = float(input("input real width of the object: "))
            self.feature_matcher.findObject(frame)
            if not self.feature_matcher.isDetected():
                print("object not detected")
                return False
            width_in_rf_image = self.feature_matcher.getObjLength()
            self.focal_length_ = self.camera_calibrator.calculateFocalLength(measured_distance, real_width, width_in_rf_image)
            self.camera_calibrator.getCameraParameters()
            if (self.focal_length_ != -1) or (self.focal_length_ != None):
                self.calibrated_ = True
                print("focal length calculated: " + str(self.focal_length_))
            return True
        else:
            print("Object detector is not enabled for agent, checking if QR is available.")
        
        if not self.QR_ENABLED:
            print("QR Scanner is not enabled for agent, abort.")
            return False
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
        return True

    def isCalibrated(self):
        return self.calibrated_

