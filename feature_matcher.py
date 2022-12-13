import cv2 as cv
import matplotlib.pyplot as plt

class FeatureMatcher:
    def __init__(self, reference_image_path):
        self.orb = cv.ORB_create()
        try:
            self.reference_image = cv.imread(reference_image_path, cv.IMREAD_GRAYSCALE)
            self.reference_image_kp, self.reference_image_des = self.orb.detectAndCompute(self.reference_image, None)
        except Exception as e:
            print("reference image could not be processed.")
            print(e)
        self.bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck = True)

    def findBF(self, frame):
        try:
            self.kp, self.des = self.orb.detectAndCompute(frame, None)
            self.matches = self.bf.match(self.reference_image_des, self.des)
            self.matches = sorted(self.matches, key = lambda x:x.distance)
        except Exception as e:
            print("could not find features on frame")
            print(e)
        return

    def drawMatches(self, frame, matchCount):
        img = cv.drawMatches(self.reference_image, self.reference_image_kp, frame, self.kp, self.matches[:matchCount], None, flags = cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        plt.imshow(img), plt.show()
