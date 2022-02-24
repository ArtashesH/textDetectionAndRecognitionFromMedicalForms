import cv2 
import pytesseract
import numpy as np
import random
#import textDetAndSeg

BINARY_THREHOLD = 220



















def image_smoothening(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret1, th1 = cv2.threshold(img, BINARY_THREHOLD, 155, cv2.THRESH_OTSU)
   # ret2, th2 = cv2.threshold(th1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
   # img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
   #         cv2.THRESH_BINARY,11,2)
    #img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
     #       cv2.THRESH_BINARY,15,7)
    img = cv2.medianBlur(img, 3)
  #  img = cv2.GaussianBlur(img, (3, 3), 0)
   # ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return img



#Setting path to tesseract ocr 

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'


#Setting configurations

custom_config = r'--oem 3  --psm 6 -l eng '


#Reading input image 
img = cv2.imread('E:/UpworkProjects/TextDetection/medsamplesocr/formsmedical_346/42.jpg')

scale_percent = 150 # percent of original size
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)
  
# resize image
img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)


img = image_smoothening(img)
img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
#hImg, wImg, _ = img.shape


d = pytesseract.image_to_data(img, output_type= pytesseract.Output.DICT)
n_boxes = len(d['level'])
for i in range(n_boxes):
    (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
    r = random.randint(0, 255)
    g = random.randint(0, 255) 
    b = random.randint(0, 255)
    rand_color = (r, g, b)
 #   cv2.rectangle(img, (x, y), (x + w, y + h), rand_color, 2)



#kernel = np.ones((3, 3), np.uint8)
  
# Using cv2.erode() method 
#img = cv2.dilate(img, kernel) 
cv2.imwrite("resFromOCR.png", img)
cv2.imshow("img", img)
cv2.waitKey(0)
#img = cv2.blur(img, (3,3))


#Getting output string 

print(pytesseract.image_to_string(img, config=custom_config))

