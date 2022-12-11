class CameraCalibrator:
    def __init__(self, parent):
        self.parent = parent
        pass

    def calculateFocalLength(self, measured_distance, real_width, width_in_rf_image):
        if width_in_rf_image == -1:
            print("unable to calculate focal length, probably no qr detected")
            return None
        focal_length = (width_in_rf_image * measured_distance) / real_width
        return focal_length

    def getCameraParameters(self):
        # TODO: return camera matrix, intrinsic/extrinsic stuff
        pass
