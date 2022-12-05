import cv2 as cv

class Agent:
    def __init__(self, turn_tolerance, VIEW_MODE):
        self.qr_detector = cv.QRCodeDetector()
        self.turn_tolerance = turn_tolerance
        self.VIEW_MODE = VIEW_MODE

    def process(self, frame):
        try:
            self.detectQR(frame)
            #self.findContours(frame)
            self.findQRMid(frame)
        except:
            print("agent couldn't process frame")
            return

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

    def findQRMid(self, frame):
        # find the middle point of QR
        if self.bbox is not None:
            first_x, first_y = self.bbox[0][0][0] + self.bbox[0][2][0], self.bbox[0][0][1] + self.bbox[0][2][1]
            first_x, first_y = first_x/2, first_y/2
            second_x, second_y = self.bbox[0][1][0] + self.bbox[0][3][0], self.bbox[0][1][1] + self.bbox[0][3][1]
            second_x, second_y = second_x/2, second_y/2
            x_coord = (first_x + second_x)/2
            y_coord = (first_y + second_y)/2
            self.qr_mid_x = x_coord
            self.qr_mid_y = y_coord
            if self.VIEW_MODE:
                cv.circle(frame, (int(x_coord), int(y_coord)), radius=10, color=(0, 0, 255), thickness=-1)

    def keepQRInMid(self, frame):
        if self.bbox is not None:
            # find center of frame
            height, width = frame.shape[:2]
            mid_x = int(width/2)
            mid_y = int(height/2)
            if self.VIEW_MODE:
                cv.circle(frame, (mid_x, mid_y), radius=10, color=(255, 0, 0), thickness=-1)

            # compare mid-qr
            if hasattr(self, 'qr_mid_x') and hasattr(self, 'qr_mid_y'):
                if self.qr_mid_x - mid_x > self.turn_tolerance:
                    print("turn right")
                    return 0
                elif self.qr_mid_x - mid_x < -self.turn_tolerance:
                    print("turn left")
                    return 1
                else:
                    return 2
            