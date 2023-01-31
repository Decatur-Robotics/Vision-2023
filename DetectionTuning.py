from pupil_apriltags import Detector
import cv2

img1 = cv2.imread('images\\Test_Image_1.png', cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread('images\\Test_Image_2.png', cv2.IMREAD_GRAYSCALE)
img3 = cv2.imread('images\\Test_Image_3.png', cv2.IMREAD_GRAYSCALE)
img4 = cv2.imread('images\\Test_Image_4.png', cv2.IMREAD_GRAYSCALE)
img5 = cv2.imread('images\\Test_Image_5.png', cv2.IMREAD_GRAYSCALE)
img6 = cv2.imread('images\\Test_Image_6.png', cv2.IMREAD_GRAYSCALE)
img7 = cv2.imread('images\\Test_Image_7.png', cv2.IMREAD_GRAYSCALE)
img8 = cv2.imread('images\\Test_Image_8.png', cv2.IMREAD_GRAYSCALE)
img9 = cv2.imread('images\\Test_Image_9.png', cv2.IMREAD_GRAYSCALE)
img10 = cv2.imread('images\\Test_Image_10.png', cv2.IMREAD_GRAYSCALE)

mostImages = 0

#Parameter ranges
quad_decimateValue = 0.2
quad_decimateChange = 0.025
quad_decimateMax = 0.3

quad_sigmaValue = 0.25
quad_sigmaChange = 0.025
quad_sigmaMax = 0.35

refine_edgesValue = 1
refine_edgesChange = 1
refine_edgesMax = 5

decode_sharpeningValue = 0.2
decode_sharpeningChange = 0.025
decode_sharpeningMax = 0.3

#Detect the apriltags
while quad_decimateValue <= quad_decimateMax:
   while quad_sigmaValue <= quad_sigmaMax:
      while refine_edgesValue <= refine_edgesMax:
         while decode_sharpeningValue <= decode_sharpeningMax:
            at_detector = Detector(
               families="tag16h5",
               nthreads=8,
               quad_decimate=quad_decimateValue,
               quad_sigma=quad_sigmaValue,
               refine_edges=refine_edgesValue,
               decode_sharpening=decode_sharpeningValue,
               debug=0
            )

            response1 = at_detector.detect(img1)
            response2 = at_detector.detect(img2)
            response3 = at_detector.detect(img3)
            response4 = at_detector.detect(img4)
            response5 = at_detector.detect(img5)
            response6 = at_detector.detect(img6)
            response7 = at_detector.detect(img7)
            response8 = at_detector.detect(img8)
            response9 = at_detector.detect(img9)
            response10 = at_detector.detect(img10)

            correctImages = 0

            if len(response1) == 1:
               correctImages += 1
            if len(response2) == 1:
               correctImages += 1
            if len(response3) == 1:
               correctImages += 1
            if len(response4) == 1:
               correctImages += 1
            if len(response5) == 1:
               correctImages += 1
            if len(response6) == 1:
               correctImages += 1
            if len(response7) == 1:
               correctImages += 1
            if len(response8) == 1:
               correctImages += 1
            if len(response9) == 1:
               correctImages += 1
            if len(response10) == 1:
               correctImages += 1

            if correctImages >= mostImages:
               print("\n----------\nquad_decimate:", quad_decimateValue, "\nquad_sigma:", quad_sigmaValue,
                     "\nrefine_edges:", refine_edgesValue, "\ndecode_sharpening:", decode_sharpeningValue,
                     "\n\nDetected 1 tag in", correctImages, "images.\n----------")

               mostImages = correctImages

            decode_sharpeningValue += decode_sharpeningChange

         refine_edgesValue += refine_edgesChange
         decode_sharpeningValue = 0.0

      quad_sigmaValue += quad_sigmaChange
      refine_edgesValue = 1
      decode_sharpeningValue = 0.0

   quad_decimateValue += quad_decimateChange
   quad_sigmaValue = 3.0
   refine_edgesValue = 1
   decode_sharpeningValue = 0.25
