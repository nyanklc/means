import cv2 as cv
from threading import Thread

# class that controls the camera mount (keeps master in frame)
class MidPointTracker:
    def __init__(self, parent):
        self.parent = parent
        pass

    def findFrameMid(self, frame):
        # find center of frame
        height, width = frame.shape[:2]
        self.mid_x = int(width/2)
        self.mid_y = int(height/2)
            

    def drawPoint(self, frame):
        cv.circle(frame, (self.mid_x, self.mid_y), radius=10, color=(255, 0, 0), thickness=3)


    # if bbox is not None:
    #         # compare mid-qr
    #         if hasattr(self, 'qr_mid_x') and hasattr(self, 'qr_mid_y'):
    #             if self.qr_mid_x - mid_x > self.turn_tolerance_:
    #                 print("turn right")
    #                 return 0
    #             elif self.qr_mid_x - mid_x < -self.turn_tolerance_:
    #                 print("turn left")
    #                 return 1
    #             else:
    #                 return 2
