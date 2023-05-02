import cv2
from RioComms import RioComms
import keyboard
import math

print("Initializing.")

rioComms = RioComms("10.40.26.2")

cap = cv2.VideoCapture(1)

cap.set(cv2.CAP_PROP_EXPOSURE, -6)

print("Running loop.")

while True:
  if keyboard.is_pressed("z"):
    exit()

  _, img = cap.read()

  img = cv2.resize(img, (200, 124)) #200, 124

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

    coneCntsAreas.append(M["m00"])

  if len(coneCntsAreas) > 0:
    maxValue = max(coneCntsAreas)

    maxConeCntsIndex = coneCntsAreas.index(maxValue)

    M = cv2.moments(coneCnts[0][maxConeCntsIndex])

    cX = int((M["m10"] / M["m00"]))
    cY = int((M["m01"] / M["m00"]))

    # img = cv2.circle(img, (math.floor(cX), math.floor(cY)), 20, (0, 0, 255), -1)
    #img = cv2.drawContours(img, coneCnts[0][maxConeCntsIndex], -1, (0, 255, 0), 3)

    rioComms.send("cones", "Cone X", cX - 100)
    rioComms.send("cones", "Cone Y", cY - 62)
    rioComms.send("cones", "Cone Visible", 1)

  else:
    rioComms.send("cones", "Cone X", 0)
    rioComms.send("cones", "Cone Y", 0)
    rioComms.send("cones", "Cone Visible", 0)

  for i in cubeCnts[0]:
    M = cv2.moments(i)

    cubeCntsAreas.append(M["m00"])

  if len(cubeCntsAreas) > 0:
    maxValue = max(cubeCntsAreas)

    maxCubeCntsIndex = cubeCntsAreas.index(maxValue)

    M = cv2.moments(cubeCnts[0][maxCubeCntsIndex])

    cX = int((M["m10"] / M["m00"]))
    cY = int((M["m01"] / M["m00"]))

    # img = cv2.circle(img, (math.floor(cX), math.floor(cY)), 20, (0, 0, 255), -1)
    # img = cv2.drawContours(img, cubeCnts[0][maxCubeCntsIndex], -1, (0, 255, 0), 3)

    rioComms.send("cubes", "Cube X", cX - 100)
    rioComms.send("cubes", "Cube Y", cY - 62)
    rioComms.send("cubes", "Cube Visible", 1)

  else:
    rioComms.send("cubes", "Cube X", 0)
    rioComms.send("cubes", "Cube Y", 0)
    rioComms.send("cubes", "Cube Visible", 0)

  # cv2.imshow("image", img)
  # cv2.imshow("cone", coneMask3)
  # cv2.imshow("cube", cubeMask3)
  #
  # cv2.waitKey(5)