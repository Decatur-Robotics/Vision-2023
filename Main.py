from RioComms import RioComms
from pupil_apriltags import Detector
import cv2
import ast
import re

rioComms = RioComms("10.40.26.2")
tableName = "apriltags"

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

#cap is 640 pixels by 480 pixels
cap = cv2.VideoCapture(0)

while True:
  _, img = cap.read()

  imgGrayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

  apriltags = at_detector.detect(imgGrayscale)

  apriltags = [x for x in apriltags if x.hamming == 0]

  if len(apriltags) > 0:
    print("\nApriltags:")

  for i in range(len(apriltags)):
    centerXY = ast.literal_eval((re.sub(" +", " ", ((str(apriltags[i].center).replace("[", "")).replace("]", "")).strip())).replace(" ", ", "))
    centerXY = list(centerXY)
    centerXY[0] = centerXY[0] - 320
    centerXY[1] = centerXY[1] - 240
    print(" Tag:", apriltags[i].tag_id, "\n  X:", str(centerXY[0]), "\n  Y:", str(centerXY[1]))
    if (apriltags[i].tag_id >= 1 and apriltags[i].tag_id <= 3) or apriltags[i].tag_id == 5:
      img = cv2.putText(img, str(apriltags[i].tag_id), (int(centerXY[0]) + 300, int(centerXY[1]) + 260), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 6, 2)
      img = cv2.putText(img, str(int(centerXY[0])) + ", " + str(int(centerXY[1])), (int(centerXY[0]) + 300, int(centerXY[1]) + 300), cv2.FONT_HERSHEY_SIMPLEX, 2/3, (0, 0, 255), 3, 2)
    elif (apriltags[i].tag_id >= 6 and apriltags[i].tag_id <= 8) or apriltags[i].tag_id == 4:
      img = cv2.putText(img, str(apriltags[i].tag_id), (int(centerXY[0]) + 300, int(centerXY[1]) + 260), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 6, 2)
      img = cv2.putText(img, str(int(centerXY[0])) + ", " + str(int(centerXY[1])), (int(centerXY[0]) + 300, int(centerXY[1]) + 300), cv2.FONT_HERSHEY_SIMPLEX, 2/3, (255, 0, 0), 3, 2)

    rioComms.send("apriltags", "Tag " + str(apriltags[i].tag_id) + " X", centerXY[0])
    rioComms.send("apriltags", "Tag " + str(apriltags[i].tag_id) + " Y", centerXY[1])



    print(apriltags[i].corners)

    cornersString = str(apriltags[i].corners).replace("[", "").replace("]", "").strip()
    cornersString = ''.join(cornersString.splitlines())
    cornersString = re.sub(" +", " ", cornersString)
    cornersXYValues = list(cornersString.split(" "))

    tagWidth = abs(float(cornersXYValues[4]) - float(cornersXYValues[6]))

    rioComms.send("apriltags", "Tag" + str(apriltags[i].tag_id) + "Width", tagWidth)


  rioComms.send("apriltags", "Tags", len(apriltags))

  apriltagIDs = []
  for i in range(len(apriltags)):
    apriltagIDs.append(apriltags[i].tag_id)

  for i in range(8):
    if apriltagIDs.count(i+1) > 0:
      tagVisible = 1
    else:
      tagVisible = 0

    rioComms.send("apriltags", "Tag " + str(i + 1) + " Visible", tagVisible)

  cv2.imshow("Camera", img)

  cv2.waitKey(5)




