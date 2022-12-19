import cv2
import numpy as np
import sys
import time

if len(sys.argv)>1:
    inputImage = cv2.imread(sys.argv[1])
else:
    inputImage = cv2.imread("./rpi_photos/image.jpg")

# Display barcode and QR code location
def display(im, bbox):
    n = len(bbox)
    for j in range(n):
        print((bbox[j][0][0], bbox[j][0][1]))
        print((bbox[ (j+1) % n][0][0], bbox[ (j+1) % n][0][1]))
        # cv2.line(im, (0.0), (150,150), (255,0,0), 3)
        # cv2.line(im, (bbox[j][0][0], bbox[j][0][1]), (bbox[ (j+1) % n][0][0], bbox[ (j+1) % n][0][1]), (255,0,0), 3)

    # Display results
    cv2.imshow("Results", im)

qrDecoder = cv2.QRCodeDetector()

# Detect and decode the qrcode
data,bbox,rectifiedImage = qrDecoder.detectAndDecode(inputImage)
if len(data)>0:
    print("Decoded Data : {}".format(data))
    print(inputImage.shape)
    display(inputImage, bbox)
    rectifiedImage = np.uint8(rectifiedImage)
    cv2.imshow("Rectified QRCode", rectifiedImage)
else:
    print("QR Code not detected")
    cv2.imshow("Results", inputImage)

cv2.waitKey(0)
cv2.destroyAllWindows()