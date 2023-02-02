import math
from networktables import NetworkTables
import logging
import keyboard
from pupil_apriltags import Detector
import cv2

#Create the Apriltag Detector

#  Working Parameters:
#    quad_decimate=0.3
#    quad_sigma=0.35
#    refine_edges=1
#    decode_sharpening=0.25

at_detector = Detector(
   families="tag16h5",
   nthreads=1,
   quad_decimate=0.3,
   quad_sigma=0.35,
   refine_edges=1,
   decode_sharpening=0.25,
   debug=0
)

#Tag size in meters
tag_size = 0.1524

cap = cv2.VideoCapture(1)

while True:
  _, img = cap.read()

  imgGrayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

  apriltags = at_detector.detect(imgGrayscale)

  apriltags = [x for x in apriltags if x.hamming == 0]

  if len(apriltags) > 0:
    print("\nApriltags:")

  for i in range(len(apriltags)):
    print("Tag", apriltags[i].tag_id, "center:", apriltags[i].center)

  cv2.imshow("Camera", img)

  #print(len(apriltags))

  cv2.waitKey(5)




