import cv2
import math

cap = cv2.VideoCapture(1)

cap.set(cv2.CAP_PROP_EXPOSURE, -6)


while True:
  _, img = cap.read()

  img = cv2.resize(img, (800, 500))

  initImg = img

  img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

  mask = cv2.inRange(img, (0, 0, 0), (25, 255, 255))

  mask2 = cv2.inRange(img, (0, 150, 0), (360, 255, 255))

  mask = cv2.medianBlur(mask, 25)
  mask2 = cv2.medianBlur(mask2, 25)

  kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, ksize=(15, 15))
  mask = cv2.erode(mask, kernel)
  mask2 = cv2.erode(mask2, kernel)

  mask = cv2.dilate(mask, kernel)
  mask2 = cv2.dilate(mask2, kernel)

  mask3 = cv2.bitwise_and(mask, mask2)

  mask3 = cv2.medianBlur(mask3, 25)

  mask3 = cv2.erode(mask3, kernel)
  mask3 = cv2.dilate(mask3, kernel)

  cnts = cv2.findContours(mask3.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

  cntsAreas = []

  for i in cnts[0]:
    M = cv2.moments(i)

    cntsAreas.append(M["m00"])

  if len(cntsAreas) > 0:
    maxValue = max(cntsAreas)

    maxCntsIndex = cntsAreas.index(maxValue)
    
    if maxValue > 2000:
      M = cv2.moments(cnts[0][maxCntsIndex])

      cX = int((M["m10"] / M["m00"])) / 800
      cY = int((M["m01"] / M["m00"])) / 500

      initImg = cv2.circle(initImg, (math.floor(cX * 800), math.floor(cY * 500)), 20, (0, 0, 255), -1)
      initImg = cv2.drawContours(initImg, cnts[0][maxCntsIndex], -1, (0, 255, 0), 3)

  cv2.imshow("initial image", initImg)
  cv2.imshow("masked image", mask3)

  cv2.waitKey(5)