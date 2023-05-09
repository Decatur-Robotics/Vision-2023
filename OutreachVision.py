import cv2
from pupil_apriltags import Detector
import keyboard
import math
import numpy as np
import ast
import re
import time

print("Initializing.")

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_EXPOSURE, -6)

#Scales resolution and window size
cameraScaler = .8 # .8 for Renato's computer

cameraX = int(960 * cameraScaler)
cameraY = int(540 * cameraScaler)

at_detector = Detector(
   families="tag16h5",
   nthreads=1,
   quad_decimate=0.3,
   quad_sigma=0.35,
   refine_edges=1,
   decode_sharpening=0.25,
   debug=0
)

print("Running loop.")

while True:
  startTime = time.time()

  if keyboard.is_pressed("z"):
    exit()

  _, img = cap.read()

  img = cv2.resize(img, (cameraX, cameraY))

  initImg1 = img

  initImg2 = img

  imgGrayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

  apriltags = at_detector.detect(imgGrayscale)

  apriltags = [x for x in apriltags if x.hamming == 0]

  img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

  coneMask1 = cv2.inRange(img, (16, 0, 0), (25, 255, 255))

  coneMask2 = cv2.inRange(img, (0, 180, 0), (180, 255, 255))

  coneMask1 = cv2.medianBlur(coneMask1, 25)
  coneMask2 = cv2.medianBlur(coneMask2, 25)

  kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, ksize=(15, 15))
  coneMask1 = cv2.erode(coneMask1, kernel)
  coneMask2 = cv2.erode(coneMask2, kernel)

  coneMask1 = cv2.dilate(coneMask1, kernel)
  coneMask2 = cv2.dilate(coneMask2, kernel)

  coneMask3 = cv2.bitwise_and(coneMask1, coneMask2)

  coneMask3 = cv2.medianBlur(coneMask3, 25)

  coneMask3 = cv2.erode(coneMask3, kernel)
  coneMask3 = cv2.dilate(coneMask3, kernel)

  coneCnts = cv2.findContours(coneMask3.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

  coneCntsAreas = []

  cubeMask1 = cv2.inRange(img, (115, 60, 0), (135, 230, 255))

  cubeMask2 = cv2.inRange(img, (0, 60, 0), (180, 230, 255))

  cubeMask1 = cv2.medianBlur(cubeMask1, 25)
  cubeMask2 = cv2.medianBlur(cubeMask2, 25)

  kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, ksize=(15, 15))
  cubeMask1 = cv2.erode(cubeMask1, kernel)
  cubeMask2 = cv2.erode(cubeMask2, kernel)

  cubeMask1 = cv2.dilate(cubeMask1, kernel)
  cubeMask2 = cv2.dilate(cubeMask2, kernel)

  cubeMask3 = cv2.bitwise_and(cubeMask1, cubeMask2)

  cubeMask3 = cv2.medianBlur(cubeMask3, 25)

  cubeMask3 = cv2.erode(cubeMask3, kernel)
  cubeMask3 = cv2.dilate(cubeMask3, kernel)

  cubeCnts = cv2.findContours(cubeMask3.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

  cubeCntsAreas = []

  for i in coneCnts[0]:
    M = cv2.moments(i)

    cX = int((M["m10"] / M["m00"]))
    cY = int((M["m01"] / M["m00"]))

    initImg2 = cv2.putText(initImg2, "Cone", (math.floor(cX) - 20, math.floor(cY) + 20), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 6, 2)
    initImg2 = cv2.putText(initImg2, str(str(math.floor(cX)) + ", " + str(math.floor(cY))), (math.floor(cX) - 20, math.floor(cY) + 60), cv2.FONT_HERSHEY_SIMPLEX, 2 / 3, (0, 0, 255), 3, 2)
    initImg2 = cv2.drawContours(initImg2, i, -1, (0, 255, 0), 3)

  for i in cubeCnts[0]:
    M = cv2.moments(i)

    cX = int((M["m10"] / M["m00"]))
    cY = int((M["m01"] / M["m00"]))

    initImg2 = cv2.putText(initImg2, "Cube", (math.floor(cX) - 20, math.floor(cY) + 20), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 6, 2)
    initImg2 = cv2.putText(initImg2, str(str(math.floor(cX)) + ", " + str(math.floor(cY))), (math.floor(cX) - 20, math.floor(cY) + 60), cv2.FONT_HERSHEY_SIMPLEX, 2 / 3, (0, 0, 255), 3, 2)
    initImg2 = cv2.drawContours(initImg2, i, -1, (0, 255, 0), 3)

  for i in range(len(apriltags)):
    # Get the center from Apriltags
    centerXY = ast.literal_eval((re.sub(" +", " ", ((str(apriltags[i].center).replace("[", "")).replace("]", "")).strip())).replace(" ", ", "))
    centerXY = list(centerXY)
    initImg2 = cv2.putText(initImg2, str(apriltags[i].tag_id), (int(centerXY[0]) - 20, int(centerXY[1]) + 20), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 6, 2)
    initImg2 = cv2.putText(initImg2, str(int(centerXY[0])) + ", " + str(int(centerXY[1])), (int(centerXY[0]) - 20, int(centerXY[1]) + 60), cv2.FONT_HERSHEY_SIMPLEX, 2 / 3, (0, 0, 255), 3, 2)

  coneMask3 = cv2.bitwise_and(initImg1, initImg1, mask=coneMask3)
  cubeMask3 = cv2.bitwise_and(initImg1, initImg1, mask=cubeMask3)

  maskedImgs = np.concatenate((cubeMask3, coneMask3), axis = 1)
  unmaskedImgs = np.concatenate((initImg2, img), axis = 1)

  finalImg = np.concatenate((unmaskedImgs, maskedImgs), axis = 0)

  elapsedTime = time.time() - startTime

  # FPS counter
  finalImg = cv2.putText(finalImg, str(round(1/elapsedTime)) + " FPS", (3, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3, 2)  

  cv2.imshow("Image", finalImg)

  cv2.waitKey(5)