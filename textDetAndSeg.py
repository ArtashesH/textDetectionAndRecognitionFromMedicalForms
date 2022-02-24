from swtloc import SWTLocalizer
import numpy as np
import cv2
import os
import random
import pytesseract


def image_smoothening(img):
   # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
   # ret1, th1 = cv2.threshold(img, BINARY_THREHOLD, 155, cv2.THRESH_OTSU)
   # ret2, th2 = cv2.threshold(th1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
   # img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
   #         cv2.THRESH_BINARY,11,2)
    #img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
     #       cv2.THRESH_BINARY,15,7)
   # img = cv2.medianBlur(img, 3)
  #  img = cv2.GaussianBlur(img, (3, 3), 0)
   # ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return img


def findCenterOfTheRect(currentRect):
    centerPoint = []
    centerPoint = ((currentRect[0][0] +   currentRect[1][0]  +  currentRect[2][0] +   currentRect[3][0])  / 4.0,
                  (currentRect[0][1] +   currentRect[1][1]  +  currentRect[2][1] +   currentRect[3][1])  / 4.0)
    return centerPoint


def joinRects(firstRect, secondRect):
    finalRect = firstRect
    if firstRect[3][0] < secondRect[3][0]:
        finalRect[3][0] = firstRect[3][0]
    if firstRect[3][0] > secondRect[3][0]:
        finalRect[3][0] = secondRect[3][0]

    if firstRect[3][1] < secondRect[3][1]:
        finalRect[3][1] = firstRect[3][1]
    if firstRect[3][1] > secondRect[3][1]:
        finalRect[3][1] = secondRect[3][1]


    if firstRect[1][0] > secondRect[1][0]:
        finalRect[1][0] = firstRect[1][0]
    if firstRect[1][0] < secondRect[1][0]:
        finalRect[1][0] = secondRect[1][0]

    if firstRect[1][1] > secondRect[1][1]:
        finalRect[1][1] = firstRect[1][1]
    if firstRect[1][1] < secondRect[1][1]:
        finalRect[1][1] = secondRect[1][1]

    finalRect[0][0] = finalRect[1][0]
    finalRect[0][1] = finalRect[3][1]

    finalRect[2][0] = finalRect[1][0]
    finalRect[2][1] = finalRect[3][1]
    return finalRect

def filterAndJoinRects(inputRectsVec):
    doProcessing = True
    while doProcessing:
        doProcessing = False
        for i in range(0,len(inputRectsVec)):
            for j in range(i+1, len(inputRectsVec)):
                centerInputRect1 = findCenterOfTheRect(inputRectsVec[i])
                centerInputRect2 = findCenterOfTheRect(inputRectsVec[j])
                if abs(centerInputRect1[1] - centerInputRect2[1]) < 10:
                     joinRect = joinRects(inputRectsVec[i],inputRectsVec[j])
                     doProcessing = True
                     inputRectsVec.pop(j)
                     inputRectsVec.pop(i)
                     inputRectsVec.append(joinRect)
                     #return inputRectsVec
                     i =  len(inputRectsVec)
                     j = len(inputRectsVec)
                     break


    return inputRectsVec


#def findRectanglesByLine(inputRectsVec):
#    filteredRectangles = []
#    doProcessing = True
#    while doProcessing:
#        doProcessing = False
#        for i in range(len(inputRectsVec)):
#            centerInputRect = findCenterOfTheRect(inputRectsVec[i])
#            for j  in range(len(filteredRectangles)):
#                centerCurrRect = findCenterOfTheRect(filteredRectangles[j])
#                if abs(centerInputRect[0] - centerCurrRect[0]) < 5:
#                    joinRect = joinRects(filteredRectangles[j],inputRectsVec[i])
#                    filteredRectangles[j] = joinRect
#                    doProcessing = True
#                    inputRectsVec.pop(i)
#                    i = len(inputRectsVec)
#                    j = len(filteredRectangles)
#            if not(doProcessing):
#                filteredRectangles.append(inputRectsVec[i])

    return filteredRectangles

                   
def findRectanglesBySize(inputRectsVec, imgWidth):
    filteredRectangles = []
    for i in range(len(inputRectsVec)):
       # centerPoint = findCenterOfTheRect(inputRectsVec[i])
        if abs(inputRectsVec[i][0][0]  -  inputRectsVec[i][3][0])   > imgWidth * 2/3:
            filteredRectangles.append(inputRectsVec[i])
    return filteredRectangles


def findRectanglesOnTheSameLine(inputRectsVec, imgWidth):
    filteredRectangles = []
    doProcessing = True
    for i in range(len(inputRectsVec)):
        centerPoint = findCenterOfTheRect(inputRectsVec[i])
        if centerPoint[0] < imgWidth / 6 or centerPoint[0] > imgWidth *4 /5:
            filteredRectangles.append(inputRectsVec[i])
    return filteredRectangles
   # while doProcessing:
      #  for i in range(inputRectsVec):



swtl = SWTLocalizer()
imgpaths = ... # Image paths, can be one image(path as str) or more than one(paths as list of str)
#swtl.swttransform(imgpaths=imgpath, save_results=True, save_rootpath='swtres/',
     #             edge_func = 'ac', ac_sigma = 1.0, text_mode = 'lb_df',
      #            gs_blurr=True, blurr_kernel = (5,5), minrsw = 3, 
       #           maxCC_comppx = 10000, maxrsw = 200, max_angledev = np.pi/6, 
        #          acceptCC_aspectratio = 5.0)
# If you have a pre-loaded image then


#Setting path to tesseract ocr 

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'


#Setting configurations

custom_config = r'--oem 3  --psm 6 -l eng '




outputFolderPath = './medsamplesocr/formsmedical_681'
inputImagePath = outputFolderPath + ".jpg"
resImagePath = outputFolderPath + "_res.jpg"
loaded_image = cv2.imread(inputImagePath)
loaded_image = cv2.blur(loaded_image, (3,3))
isExist = os.path.exists(outputFolderPath)
if not(isExist):
    os.mkdir(outputFolderPath)
heightImg, widthImg, channels = loaded_image.shape
resImg = loaded_image.copy()


#Erode preprocessing
kernel = np.ones((3,3), np.uint8)
img_erosion = cv2.erode(loaded_image, kernel, iterations=1)

cv2.imshow("blur image ", loaded_image)
cv2.waitKey(10)

swtl.swttransform(image=loaded_image, save_results=True, save_rootpath='swtres/',
                  edge_func = 'ac', ac_sigma = 1.0, text_mode = 'lb_df',
                  gs_blurr=True, blurr_kernel = (3,3), minrsw = 9, 
                  maxCC_comppx = 5000, maxrsw = 1500, max_angledev = np.pi/6, 
                  acceptCC_aspectratio = 9.0)

min_bboxes, min_bbox_annotated = swtl.get_extreme_bbox(show=True, padding=1)
rectsForProcessing = []

#rectsForProcessing = findRectanglesOnTheSameLine(min_bboxes, widthImg)
print("Rects size befire filter ")
print(len(min_bboxes))
rectsForProcessing = min_bboxes
rectsForProcessing = filterAndJoinRects(rectsForProcessing)
rectsFinal = findRectanglesBySize(rectsForProcessing, widthImg)

#min_bboxes = []
#min_bboxes = rectsFinal
print("Rects size after filtering")
print(len(min_bboxes))
#for i in range(len(min_bboxes)):
 #   rectsForProcessing.append(min_bboxes[i])
currentIndexForRes = 0
for i in range(len(min_bboxes)):
   # print(min_bboxes[0])
#    cv2.circle(resImg,(min_bboxes[i][2][0], min_bboxes[i][2][1]),5,(0,255,0),-1)
    cropImage = resImg[min_bboxes[i][3][1]:min_bboxes[i][1][1],  min_bboxes[i][3][0]-3:min_bboxes[i][1][0]+9]
    scale_percent = 150 # percent of original size
    width = int(cropImage.shape[1] * scale_percent / 100)
    height = int(cropImage.shape[0] * scale_percent / 100)
    if height == 0 or width == 0:
        continue
    dim = (width, height)  
    print("size image ")
    print(height)
    print(width)
    # resize image
    img = cv2.resize(cropImage, dim, interpolation = cv2.INTER_AREA)
    img = image_smoothening(img)
    recogText = pytesseract.image_to_string(img, config=custom_config)
   # print(recogText)




    resImagePathFinal = outputFolderPath + '/' + str(currentIndexForRes) + '.jpg'
    resTextPathFinal = outputFolderPath + '/' + str(currentIndexForRes) + '.txt'
    resTextFile = open(resTextPathFinal,"w")
    resTextFile.write(recogText)
    resTextFile.close()
    cv2.imwrite(resImagePathFinal, cropImage)
   # cv2.rectangle(resImg,(min_bboxes[i][3][0],min_bboxes[i][3][1]),(min_bboxes[i][1][0],min_bboxes[i][1][1]),(255,0,0),3)
    currentIndexForRes = currentIndexForRes + 1

for i in range(len(min_bboxes)):
    r = random.randint(0, 255)
    g = random.randint(0, 255) 
    b = random.randint(0, 255)
    rand_color = (r, g, b)
    cv2.rectangle(resImg,(min_bboxes[i][3][0],min_bboxes[i][3][1]),(min_bboxes[i][1][0],min_bboxes[i][1][1]),rand_color,2)
cv2.imshow('resImg',resImg)
cv2.waitKey(10)
 #exit()
cv2.imwrite(resImagePath, resImg)
#print(min_bboxes[0])
print(min_bboxes[0][2][0])
print(min_bboxes[0][2][1])

print('!!!!!!!!!')
print(min_bboxes[0][0][0])
print(min_bboxes[0][0][1])