import math
from networktables import NetworkTables
import logging
import keyboard
from pupil_apriltags import Detector
import cv2

#Create the Apriltag Detector
at_detector = Detector(
   families="tag16h5",
   nthreads=1,
   quad_decimate=3.0,
   quad_sigma=3.0,
   refine_edges=1,
   decode_sharpening=0.25,
   debug=0
)

cap = cv2.VideoCapture(1)

while True:
  _, img = cap.read()

  cv2.imshow("Camera", img)

  cv2.waitKey(5)




