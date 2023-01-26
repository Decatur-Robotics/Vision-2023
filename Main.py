import math
import keyboard
from networktables import NetworkTables
import logging
from pupil_apriltags import Detector
import cv2

#Create the Apriltag Detector
at_detector = Detector(
   families="tag36h11 tag16h5",
   nthreads=1,
   quad_decimate=1.0,
   quad_sigma=0.0,
   refine_edges=1,
   decode_sharpening=0.25,
   debug=0
)

#Init NetworkTables
logging.basicConfig(level=logging.DEBUG)
NetworkTables.initialize()
sd = NetworkTables.getTable("SmartDashboard")
sd.putNumberArray("pos", {-1, -1, -1})
sd.putNumber("rot", -1)

#create a video capture
cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_EXPOSURE, -6)

bounds = 10

colorBlueUnsaturated = 125

while True:
    #read frame from the camera
    _, img = cap.read()

    #resize camera, used later with contours
    img = cv2.resize(img, (800,500))

    #image without masks
    initImg = img

    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #only show things between certain saturations
    mask = cv2.inRange(img, (0, 0, 50), (360, 255, 255))

    if keyboard.is_pressed('d'):
        colorBlueUnsaturated += 1
        print(colorBlueUnsaturated)

    if keyboard.is_pressed('a'):
        colorBlueUnsaturated -= 1
        print(colorBlueUnsaturated)

    #only show things between color range
    mask2 = cv2.inRange(img, (colorBlueUnsaturated - bounds, 0, 0), (colorBlueUnsaturated + bounds, 255, 255))

    #show both masks at once, only shows pixels picked up by both masks
    mask3 = cv2.bitwise_and(mask, mask2)

    #improve accuracy of the mask detection
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, ksize=(3,3))
    mask3 = cv2.erode(mask3, kernel)
    mask3 = cv2.dilate(mask3, kernel)

    #find countours, basically finding the edges of the game piece
    cnts = cv2.findContours(mask3.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for i in cnts[0]:
        M = cv2.moments(i)
        cX = int((M["m10"] / M["m00"])) / 800
        cY = int((M["m01"] / M["m00"])) / 500

        initImg = cv2.circle(initImg,(math.floor(cX * 800), math.floor(cY * 500)), 20, (0, 0, 255), -1)
        img = cv2.circle(initImg,(math.floor(cX * 800), math.floor(cY * 500)), 20, (0, 0, 255), -1)

        break

    img = cv2.bitwise_and(img, img, mask=mask3)

    #show the capture from camera
    cv2.imshow("image with masks", img)
    cv2.imshow("initial image", initImg)
    
    #Uncomment below two lines if reading from image file instead of camera
    # img = cv2.imread('images\\IMG_0442.png', cv2.IMREAD_GRAYSCALE)
    # cv2.imshow('img', img)

    cv2.waitKey(0)
    
    #Detect the apriltags
    response = at_detector.detect(img)
    print(response)

    #wait in milliseconds
    cv2.waitKey(5)