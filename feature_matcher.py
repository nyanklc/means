import cv2 as cv
import matplotlib.pyplot as plt

class FeatureMatcher:
    def __init__(self, reference_image_path):
        self.orb = cv.ORB_create()
        self.reference_image = cv.imread(reference_image_path, cv.IMREAD_GRAYSCALE)
        self.reference_image_kp, self.reference_image_des = self.orb.detectAndCompute(self.reference_image, None)
        self.bf = cv.BFMatcher()
        pass

    def findBF(self, frame):
        self.kp, self.des = orb.detectAndCompute(frame, None)
        self.matches = self.bf.match(self.reference_image_des, self.des)
        self.matches = sorted(matches, key = lambda x:x.distance)
        return

    def drawMatches(self, frame, matchCount):
        img = cv.drawMatches(self.reference_image, self.reference_image_kp, frame, self.kp, matches[:matchCount], None, flags = cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        plt.imshow(img), plt.show()
