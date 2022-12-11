import cv2 as cv
from threading import Thread, Lock
import time

class StreamGetter:
    def __init__(self, src=0):
        self.cap = cv.VideoCapture(src)
        (self.retrieved, self.frame) = self.cap.read()
        self.stopped = False
        self.read_lock = Lock()
        self.prev_frame_time = 0
        self.new_frame_time = 0

    def startStream(self):
        try:
            self.th = Thread(target = self.getStream, args = ())
            self.th.start()
        except any:
            print("Stream getter thread couldn't start.")
            return False
        return True

    def getStream(self):
        while not self.stopped:
            self.new_frame_time = time.time()
            if not self.retrieved:
                self.stopStream()
            else:
                (retrieved, frame) = self.cap.read()
                self.read_lock.acquire()
                self.retrieved, self.frame = retrieved, frame
                self.read_lock.release()
            #print("GETTER: " + str(1/(self.new_frame_time-self.prev_frame_time)))
            self.prev_frame_time = self.new_frame_time

    def stopStream(self):
        self.stopped = True
        self.th.join()

    def endStream(self):
        self.stopped = True
        self.cap.release()

    def getFrame(self):
        self.read_lock.acquire()
        frame = self.frame
        self.read_lock.release()
        return frame

    def getRetrieved(self):
        self.read_lock.acquire()
        retrieved = self.retrieved
        self.read_lock.release()
        return retrieved


