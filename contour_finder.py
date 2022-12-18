import cv2 as cv

class ContourFinder:
    def __init__(self, parent):
        self.parent = parent
        pass

    def findContours(self, gray):
        # convert the image to grayscale, blur it, and detect edges
        # gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        gray = cv.GaussianBlur(gray, (5, 5), 0)
        edged = cv.Canny(gray, 35, 125)
        # find the contours in the edged image
        self.contours = cv.findContours(edged.copy(), cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
        #print("self.contours = " + str(self.contours))
        return self.contours

    def drawContours(self, frame):
        cv.drawContours(frame, self.contours[0], -1, (0, 255, 0), 3)
