import cv2 as cv
import math

class QRFinder:
    def __init__(self, parent, real_QR_length):
        self.parent = parent
        self.real_QR_length = real_QR_length
        self.QR_detector = cv.QRCodeDetector()
        pass

    def detectQR(self, frame):
        self.data, self.bbox, self.rectified_image = self.QR_detector.detectAndDecode(frame)
        self.getQRMidPoint()
        self.getQRDistance()
        return self.data, self.bbox, self.rectified_image

    def isDetected(self):
        if len(self.data) > 0:
            return True
        return False

    def drawBounds(self, frame):
        if self.bbox is not None:
            bb_pts = self.bbox.astype(int).reshape(-1, 2)
            num_bb_pts = len(bb_pts)
            for i in range(num_bb_pts):
                cv.line(frame,
                        tuple(bb_pts[i]),
                        tuple(bb_pts[(i+1) % num_bb_pts]),
                        color=(255, 0, 255), thickness=3)
            cv.putText(frame, self.data,
                        (bb_pts[0][0], bb_pts[0][1] - 10),
                        cv.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 255, 0), 2)

    def getQRLength(self):
        if self.bbox  is not None:
            qr_line_length = math.hypot(abs(self.bbox[0][0][0] - self.bbox[0][1][0]), abs(self.bbox[0][0][1] - self.bbox[0][1][1]))
            return qr_line_length
        else:
            return -1

    def getQRMidPoint(self):
        if self.bbox is not None:
            # find the middle of two diagonal lines and average them
            first_x, first_y = self.bbox[0][0][0] + self.bbox[0][2][0], self.bbox[0][0][1] + self.bbox[0][2][1]
            first_x, first_y = first_x/2, first_y/2
            second_x, second_y = self.bbox[0][1][0] + self.bbox[0][3][0], self.bbox[0][1][1] + self.bbox[0][3][1]
            second_x, second_y = second_x/2, second_y/2
            self.x_coord = (first_x + second_x)/2
            self.y_coord = (first_y + second_y)/2
            return self.x_coord, self.y_coord
        return None

    def drawMidPoint(self, frame):
        # cv.circle(frame, (self.x_coord, self.y_coord), radius=10, color=(255, 0, 0), thickness=3)
        pass

    def getQRDistance(self):
        focal_len = self.parent.getFocalLength()
        self.distance = (self.real_QR_length * focal_len) / self.getQRLength()
        return self.distance

    def drawDistance(self, frame):
        print("QR Distance: " + str(self.distance) + "cm")