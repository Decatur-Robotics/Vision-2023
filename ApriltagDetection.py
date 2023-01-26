import cv2
import math
from pupil_apriltags import Detector

#create a video capture
cap = cv2.VideoCapture(2)

cap.set(cv2.CAP_PROP_EXPOSURE, -6)

while True:
    _, initImg = cap.read()

    img = cv2.cvtColor(initImg, cv2.COLOR_BGR2GRAY)
    
    at_detector = Detector(
    families="tag16h5",
    nthreads=1,
    quad_decimate=1.0,
    quad_sigma=0.0,
    refine_edges=1,
    decode_sharpening=0.25,
    debug=0
    )

    tags = at_detector.detect(img, estimate_tag_pose=False, camera_params=None, tag_size=None)

    cv2.imshow("Image", img)

    cv2.waitKey(5)