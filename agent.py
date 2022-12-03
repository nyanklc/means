import cv2 as cv

class Agent:
    def __init__(self):
        self.qr_detector = cv.QRCodeDetector()

    def process(self, frame):
        self.detectQR(frame)
        self.findContours(frame)

    def draw(self, frame):
        self.drawBounds(frame)
        self.drawContours(frame)

    def detectQR(self, frame):
        self.data, self.bbox, self.rectified_image = self.qr_detector.detectAndDecode(frame)
    def drawBounds(self, frame):

        if (self.isDetected()) and (self.bbox is not None):
            bb_pts = self.bbox.astype(int).reshape(-1, 2)
            num_bb_pts = len(bb_pts)
            for i in range(num_bb_pts):
                cv.line(frame,
                        tuple(bb_pts[i]),
                        tuple(bb_pts[(i+1) % num_bb_pts]),
                        color=(255, 0, 255), thickness=2)
            cv.putText(frame, self.data,
                        (bb_pts[0][0], bb_pts[0][1] - 10),
                        cv.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 255, 0), 2)

    def isDetected(self):
        if len(self.data) > 0:
            return True
        else:
            return False

    def findContours(self, frame):
        # convert the image to grayscale, blur it, and detect edges
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        gray = cv.GaussianBlur(gray, (5, 5), 0)
        edged = cv.Canny(gray, 35, 125)
        # find the contours in the edged image
        self.contours = cv.findContours(edged.copy(), cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

    def drawContours(self, frame):
        cv.drawContours(frame, self.contours[0], -1, (0, 255, 0), 3)

    def calculateFocalLength(self, measured_distance, real_width, width_in_rf_image):
        self.focal_length = (width_in_rf_image * measured_distance) / real_width

    def getFocalLength(self):
        return self.focal_length
