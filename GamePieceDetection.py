import cv2
import keyboard
import math

#create a video capture
cap = cv2.VideoCapture(2)

cap.set(cv2.CAP_PROP_EXPOSURE, -6)

bounds = 10

num = 120

while True:
    #read frame from the camera
    _, img = cap.read()

    img = cv2.resize(img, (800,500))

    initImg = img

    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #only show things between certain saturations
    mask = cv2.inRange(img, (0, 255*1/2, 50), (360, 255, 255))

    if keyboard.is_pressed('q'):
        num += 1
        print(num)

    #only show things between color range
    mask2 = cv2.inRange(img, (num - bounds, 0, 0), (num + bounds, 255, 255))

    mask3 = cv2.bitwise_and(mask, mask2)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, ksize=(5,5))

    mask3 = cv2.erode(mask3, kernel)
    mask3 = cv2.erode(mask3, kernel)

    mask3 = cv2.dilate(mask3, kernel)
    mask3 = cv2.dilate(mask3, kernel)

    cnts = cv2.findContours(mask3.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for i in cnts[0]:
        M = cv2.moments(i)
        cX = int((M["m10"] / M["m00"])) / 800
        cY = int((M["m01"] / M["m00"])) / 500

        initImg = cv2.circle(initImg,(math.floor(cX * 800), math.floor(cY * 500)), 20, (0, 0, 255), -1)

        break

    img = cv2.bitwise_and(img, img, mask=mask3)

    #show the capture from camera
    cv2.imshow("test", initImg)

    #wait in milliseconds
    cv2.waitKey(5)