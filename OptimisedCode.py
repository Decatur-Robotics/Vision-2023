import cv2
from RioComms import RioComms
import keyboard
import threading

print("Initializing.")

rioComms = RioComms("10.40.26.2")

cap = cv2.VideoCapture(1)

cap.set(cv2.CAP_PROP_EXPOSURE, -6)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, ksize=(15, 15))

coneHueMask = None
coneSaturationMask = None
cubeHueMask = None
cubeSaturationMask = None
finalConeMask = None
finalCubeMask = None

def cone_hue_mask(lower, upper):
  global coneHueMask

  coneHueMask = (cv2.dilate(cv2.erode(cv2.medianBlur(cv2.inRange(img, (lower, 0, 0), (upper, 255, 255)), 25), kernel), kernel))

def cone_saturation_mask(lower, upper):
  global coneSaturationMask

  coneSaturationMask = (cv2.dilate(cv2.erode(cv2.medianBlur(cv2.inRange(img, (0, lower, 0), (180, upper, 255)), 25), kernel), kernel))

def cone_mask_merge(mask1, mask2):
  global finalConeMask

  finalConeMask = (cv2.bitwise_and(mask1, mask2))

def cube_hue_mask(lower, upper):
  global cubeHueMask

  cubeHueMask = (cv2.dilate(cv2.erode(cv2.medianBlur(cv2.inRange(img, (lower, 0, 0), (upper, 255, 255)), 25), kernel), kernel))

def cube_saturation_mask(lower, upper):
  global cubeSaturationMask

  cubeSaturationMask = (cv2.dilate(cv2.erode(cv2.medianBlur(cv2.inRange(img, (0, lower, 0), (180, upper, 255)), 25), kernel), kernel))

def cube_mask_merge(mask1, mask2):
  global finalCubeMask

  finalCubeMask = (cv2.bitwise_and(mask1, mask2))

def find_cone_position():
  coneCnts = cv2.findContours(finalConeMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  coneCntsAreas = []

  for i in coneCnts[0]:
    M = cv2.moments(i)

    coneCntsAreas.append(M["m00"])

  if len(coneCntsAreas) > 0:
    M = cv2.moments(coneCnts[0][coneCntsAreas.index(max(coneCntsAreas))])

    cX = int((M["m10"] / M["m00"]))
    cY = int((M["m01"] / M["m00"]))

    rioComms.send("cones", "Cone X", cX - 100)
    rioComms.send("cones", "Cone Y", cY - 62)
    rioComms.send("cones", "Cone Visible", 1)

  else:
    rioComms.send("cones", "Cone X", 0)
    rioComms.send("cones", "Cone Y", 0)
    rioComms.send("cones", "Cone Visible", 0)

def find_cube_position():
  cubeCnts = cv2.findContours(finalCubeMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  cubeCntsAreas = []

  for i in cubeCnts[0]:
    M = cv2.moments(i)

    cubeCntsAreas.append(M["m00"])

  if len(cubeCntsAreas) > 0:
    M = cv2.moments(cubeCnts[0][cubeCntsAreas.index(max(cubeCntsAreas))])

    cX = int((M["m10"] / M["m00"]))
    cY = int((M["m01"] / M["m00"]))

    rioComms.send("cubes", "Cube X", cX - 100)
    rioComms.send("cubes", "Cube Y", cY - 62)
    rioComms.send("cubes", "Cube Visible", 1)

  else:
    rioComms.send("cubes", "Cube X", 0)
    rioComms.send("cubes", "Cube Y", 0)
    rioComms.send("cubes", "Cube Visible", 0)

coneHueMaskThread = threading.Thread(target=cone_hue_mask, args=(16, 25))
coneSaturationMaskThread = threading.Thread(target=cone_saturation_mask, args=(180, 255))

cubeHueMaskThread = threading.Thread(target=cube_hue_mask, args=(115, 135))
cubeSaturationMaskThread = threading.Thread(target=cube_saturation_mask, args=(60, 230))

print("Running loop.")

while True:
  if keyboard.is_pressed("z"):
    exit()

  _, img = cv2.cvtColor(cv2.resize(cap.read(), (200, 124)), cv2.COLOR_BGR2HSV)

  coneHueMaskThread.start()
  coneSaturationMaskThread.start()
  cubeHueMaskThread.start()
  cubeSaturationMaskThread.start()

  coneHueMaskThread.join()
  coneSaturationMaskThread.join()
  cubeHueMaskThread.join()
  cubeSaturationMaskThread.join()

  coneMaskMergeThread = threading.Thread(target=cone_mask_merge(), args=(coneHueMask, coneSaturationMask))
  cubeMaskMergeThread = threading.Thread(target=cube_mask_merge(), args=(cubeHueMask, cubeSaturationMask))

  coneMaskMergeThread.start()
  cubeMaskMergeThread.start()

  coneMaskMergeThread.join()
  cubeMaskMergeThread.join()