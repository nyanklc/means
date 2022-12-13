import cv2 as cv
import matplotlib.pyplot as plt

FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks=50)   # or pass empty dictionary

knn_k = 2

class FeatureMatcher:
    def __init__(self, reference_image_path):
        self.sift = cv.SIFT_create()
        try:
            self.reference_image = cv.imread(reference_image_path, cv.IMREAD_GRAYSCALE)
            self.reference_image_kp, self.reference_image_des = self.sift.detectAndCompute(self.reference_image, None)
        except Exception as e:
            print("reference image could not be processed.")
            print(e)
        self.flann = cv.FlannBasedMatcher(index_params, search_params)

    def findFLANN(self, frame):
        try:
            self.kp, self.des = self.sift.detectAndCompute(frame, None)
            self.matches = self.flann.knnMatch(self.reference_image_des, self.des, k = knn_k)
            # Need to draw only good matches, so create a mask
            self.matchesMask = [[0,0] for i in range(len(self.matches))]
            # ratio test as per Lowe's paper
            for i,(m,n) in enumerate(self.matches):
                if m.distance < 0.7*n.distance:
                    self.matchesMask[i]=[1,0]
        except Exception as e:
            print("could not find features on frame")
            print(e)
        return

    def drawMatches(self, frame, matchCount):
        draw_params = dict(matchColor = (0,255,0),
                   singlePointColor = (255,0,0),
                   matchesMask = self.matchesMask,
                   flags = cv.DrawMatchesFlags_DEFAULT)

        img = cv.drawMatchesKnn(frame, self.kp, self.reference_image, 
                                self.reference_image_kp, self.matches, 
                                None, **draw_params)
        plt.imshow(img), plt.show()

class ContourFinder:
    def __init__(self):
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


fm = FeatureMatcher('ref_img/ref_img4.jpeg')
cn = ContourFinder()

img = cv.imread('test_img/test4.jpeg', cv.IMREAD_GRAYSCALE)

fm.findFLANN(img)
cn.findContours(img)

fm.drawMatches(img, 10)


# class FeatureMatcher:
#     def __init__(self, reference_image_path):
#         self.orb = cv.ORB_create()
#         try:
#             self.reference_image = cv.imread(reference_image_path, cv.IMREAD_GRAYSCALE)
#             self.reference_image_kp, self.reference_image_des = self.orb.detectAndCompute(self.reference_image, None)
#         except Exception as e:
#             print("reference image could not be processed.")
#             print(e)
#         self.bf = cv.BFMatcher(cv.NORM_RELATIVE, crossCheck = True)

#     def findBF(self, frame):
#         try:
#             self.kp, self.des = self.orb.detectAndCompute(frame, None)
#             self.matches = self.bf.match(self.reference_image_des, self.des)
#             self.matches = sorted(self.matches, key = lambda x:x.distance)
#         except Exception as e:
#             print("could not find features on frame")
#             print(e)
#         return

#     def drawMatches(self, frame, matchCount):
#         img = cv.drawMatches(self.reference_image, self.reference_image_kp, frame, 
#                             self.kp, self.matches[:matchCount], None, 
#                             flags = cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
#         plt.imshow(img), plt.show()

# class ContourFinder:
#     def __init__(self):
#         pass

#     def findContours(self, gray):
#         # convert the image to grayscale, blur it, and detect edges
#         # gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
#         gray = cv.GaussianBlur(gray, (5, 5), 0)
#         edged = cv.Canny(gray, 35, 125)
#         # find the contours in the edged image
#         self.contours = cv.findContours(edged.copy(), cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
#         #print("self.contours = " + str(self.contours))
#         return self.contours

#     def drawContours(self, frame):
#         cv.drawContours(frame, self.contours[0], -1, (0, 255, 0), 3)

