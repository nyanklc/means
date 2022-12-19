import cv2 as cv
import numpy as np
import math

class FeatureMatcher:
    def __init__(self, parent, reference_image_path, real_object_length):
        self.parent = parent
        self.real_obj_length = real_object_length
        self.detector = cv.SIFT_create()
        self.detected = False
        try:
            self.reference_image = cv.imread(reference_image_path, cv.IMREAD_GRAYSCALE)
            self.reference_image_kp, self.reference_image_des = self.detector.detectAndCompute(self.reference_image, None)
        except Exception as e:
            print("reference image could not be processed.")
            print(e)
        self.matcher = cv.DescriptorMatcher_create(cv.DescriptorMatcher_FLANNBASED)

    def findObject(self, frame):
        self.good_matches = []
        try:
            # match
            self.kp, self.des = self.detector.detectAndCompute(frame, None)
            self.matches = self.matcher.knnMatch(self.reference_image_des, self.des, 2)
            # filter (Lowe's ratio test)
            ratio_thresh = 0.75
            
            for m,n in self.matches:
                if m.distance < ratio_thresh * n.distance:
                    self.good_matches.append(m)
        except Exception as e:
            print("could not find features on frame")
            print(e)
            return None
        if len(self.good_matches) > 5:
            # print("object found")
            # print("matches len: " + str(len(self.matches)))
            # print("good matches len: " + str(len(self.good_matches)))
            try:
                #-- homography
                obj = np.empty((len(self.good_matches),2), dtype=np.float32)
                scene = np.empty((len(self.good_matches),2), dtype=np.float32)
                for i in range(len(self.good_matches)):
                    #-- Get the keypoints from the good matches
                    obj[i,0] = self.reference_image_kp[self.good_matches[i].queryIdx].pt[0]
                    obj[i,1] = self.reference_image_kp[self.good_matches[i].queryIdx].pt[1]
                    scene[i,0] = self.kp[self.good_matches[i].trainIdx].pt[0]
                    scene[i,1] = self.kp[self.good_matches[i].trainIdx].pt[1]
                H, _ =  cv.findHomography(obj, scene, cv.RANSAC)

                #-- Get the corners from the image_1 ( the object to be "detected" )
                obj_corners = np.empty((4,1,2), dtype=np.float32)
                obj_corners[0,0,0] = 0
                obj_corners[0,0,1] = 0
                obj_corners[1,0,0] = self.reference_image.shape[1]
                obj_corners[1,0,1] = 0
                obj_corners[2,0,0] = self.reference_image.shape[1]
                obj_corners[2,0,1] = self.reference_image.shape[0]
                obj_corners[3,0,0] = 0
                obj_corners[3,0,1] = self.reference_image.shape[0]
                self.scene_corners = cv.perspectiveTransform(obj_corners, H)
                self.detected = True
                self.getObjDistance()
                print("object detected: " , str((self.scene_corners[0,0,0], self.scene_corners[0,0,1])), str((self.scene_corners[1,0,0], self.scene_corners[1,0,1])), str((self.scene_corners[2,0,0], self.scene_corners[2,0,1])), str((self.scene_corners[3,0,0], self.scene_corners[3,0,1])))
            except Exception as e:
                self.scene_corners = None
                print("object bounding box failed with the exception: ")
                print(e)
                self.detected = False
                return None
        else: # not detected
            self.detected = False
            return None
        return (self.scene_corners[0,0,0], self.scene_corners[0,0,1]), (self.scene_corners[1,0,0], self.scene_corners[1,0,1]), (self.scene_corners[2,0,0], self.scene_corners[2,0,1]), (self.scene_corners[3,0,0], self.scene_corners[3,0,1])

    def drawMatches(self, frame):
        # obj -> reference image
        # scene -> current frame
        if self.scene_corners is not None:
            #-- Draw lines between the corners (the mapped object in the scene - image_2 )
            cv.line(frame, (int(self.scene_corners[0,0,0]), int(self.scene_corners[0,0,1])),\
                (int(self.scene_corners[1,0,0]), int(self.scene_corners[1,0,1])), (0,255,0), 4)
            cv.line(frame, (int(self.scene_corners[1,0,0]), int(self.scene_corners[1,0,1])),\
                (int(self.scene_corners[2,0,0]), int(self.scene_corners[2,0,1])), (0,255,0), 4)
            cv.line(frame, (int(self.scene_corners[2,0,0]), int(self.scene_corners[2,0,1])),\
                (int(self.scene_corners[3,0,0]), int(self.scene_corners[3,0,1])), (0,255,0), 4)
            cv.line(frame, (int(self.scene_corners[3,0,0]), int(self.scene_corners[3,0,1])),\
                (int(self.scene_corners[0,0,0]), int(self.scene_corners[0,0,1])), (0,255,0), 4)
        return

    def getObjLength(self):
        if self.detected:
            obj_len = math.hypot(abs(self.scene_corners[0,0,0] - self.scene_corners[3,0,0]) , abs(self.scene_corners[0,0,1] - self.scene_corners[3,0,1]))
            return obj_len
        else:
            return -1

    def getObjDistance(self):
        if self.getObjLength() == -1:
            self.distance = -1.0
            return -1.0
        focal_len = self.parent.getFocalLength()
        self.distance = (self.real_obj_length * focal_len) / self.getObjLength()
        return self.distance

    def getDistance(self):
        print("Obj Distance: " + str(self.distance) + " cm")
        return self.distance

    def isDetected(self):
        return self.detected

