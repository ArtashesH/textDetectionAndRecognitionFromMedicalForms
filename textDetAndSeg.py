from swtloc import SWTLocalizer
import numpy as np
import cv2
import os
import sys
import random
import pytesseract

#Preprocessing and applying gaussian blur filter
def image_smoothening(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  
    img = cv2.GaussianBlur(img, (3, 3), 0)
    return img


#Check intersection of rectangles

def rectsAreintersecting(firstRect, secondRect):
    rectInters =  (not (firstRect[0][0] < secondRect[2][0] or firstRect[2][0] > secondRect[0][0] or firstRect[0][1] or secondRect[2][1] or firstRect[2][1] > secondRect[0][1]))  or (firstRect[3][0] < secondRect[3][0] and  firstRect[3][1] < secondRect[3][1] and  firstRect[1][0] > secondRect[1][0] and  firstRect[1][1] > secondRect[1][1])
    return rectInters

#Find rectangle center point
def findCenterOfTheRect(currentRect):
    centerPoint = []
    centerPoint = ((currentRect[0][0] +   currentRect[1][0]  +  currentRect[2][0] +   currentRect[3][0])  / 4.0,
                  (currentRect[0][1] +   currentRect[1][1]  +  currentRect[2][1] +   currentRect[3][1])  / 4.0)
    return centerPoint

#Join two rectangles
def joinRects(firstRect, secondRect):
    finalRect = firstRect
    if firstRect[3][0] < secondRect[3][0]:
        finalRect[3][0] = firstRect[3][0]
    if firstRect[3][0] >= secondRect[3][0]:
        finalRect[3][0] = secondRect[3][0]

    if firstRect[3][1] < secondRect[3][1]:
        finalRect[3][1] = firstRect[3][1]
    if firstRect[3][1] >= secondRect[3][1]:
        finalRect[3][1] = secondRect[3][1]


    if firstRect[1][0] > secondRect[1][0]:
        finalRect[1][0] = firstRect[1][0]
    if firstRect[1][0] <= secondRect[1][0]:
        finalRect[1][0] = secondRect[1][0]

    if firstRect[1][1] > secondRect[1][1]:
        finalRect[1][1] = firstRect[1][1]
    if firstRect[1][1] <= secondRect[1][1]:
        finalRect[1][1] = secondRect[1][1]

    
    finalRect[0][0] = finalRect[1][0]
    finalRect[0][1] = finalRect[3][1]

    finalRect[2][0] = finalRect[3][0]
    finalRect[2][1] = finalRect[1][1]
    return finalRect

#Join rectangles on the same line, and get final rect gor given line
def filterAndJoinRects(inputRectsVec):
    doProcessing = True
    while doProcessing:
        doProcessing = False
        for i in range(0,len(inputRectsVec)):
            for j in range(i+1, len(inputRectsVec)):
                centerInputRect1 = findCenterOfTheRect(inputRectsVec[i])
                centerInputRect2 = findCenterOfTheRect(inputRectsVec[j])
                if abs(centerInputRect1[1] - centerInputRect2[1]) < 20   or  rectsAreintersecting(inputRectsVec[i], inputRectsVec[j]):
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

#   return filteredRectangles

 
#From found rectangles get only with size > 2/3 of page width
def findRectanglesBySize(inputRectsVec, imgWidth):
    filteredRectangles = []
    for i in range(len(inputRectsVec)):
       # centerPoint = findCenterOfTheRect(inputRectsVec[i])
        if abs(inputRectsVec[i][0][0]  -  inputRectsVec[i][3][0])   > imgWidth  /2:
            filteredRectangles.append(inputRectsVec[i])
    return filteredRectangles





def  main():
    #Initialize swt 
    swtl = SWTLocalizer()
   
    #Read input image path
    if len(sys.argv[1:]) != 1:
        print("Please call script with input folder path");
        return
    #Setting path to tesseract ocr 
    pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
    #Setting configurations
    custom_config = r'--oem 3  --psm 6 -l eng '
    
    #First argument is input image path, by the same name it will create a folder and save croped images and recognize texts in .txt files
    #Also result rectangles are shown on the image with name inputPath_res 

    
  
    inputFolderPath = str(sys.argv[1])
   # print(inputFolderPath)
    filesInFolder = os.listdir(inputFolderPath)
    for currentFilePath in filesInFolder:
        if currentFilePath.endswith(('.jpg', '.png', '.jpeg')):
            inputImagePath = currentFilePath
            splitOutputPath = inputImagePath.split('.')
            print(splitOutputPath)
            outputFolderPath = inputFolderPath + '/'
            for i in range(0,len(splitOutputPath)-1):
                outputFolderPath  = outputFolderPath +  splitOutputPath[i]
            print("Output folder path ")
            print(outputFolderPath)
            resImagePath = str(outputFolderPath) + "_res.jpg"
            #Load input image from inputImagePath           
            inputImagePath = inputFolderPath + '/' + inputImagePath
            print("Read image path")
            print(inputImagePath)
            loaded_image = cv2.imread(inputImagePath)
            #Blur preprocessing
            loaded_image = cv2.medianBlur(loaded_image, 5)
            #Create output folder, if that does not exist
            isExist = os.path.exists(outputFolderPath)
            if not(isExist):
                os.mkdir(outputFolderPath)
            heightImg, widthImg, channels = loaded_image.shape
            #image , on which will be drawn line rectangles
            resImg = loaded_image.copy()
            #Erode preprocessing
            kernel = np.ones((3,3), np.uint8)
            img_erosion = cv2.erode(loaded_image, kernel, iterations=1)
            #Do SWT(Stroke Width Transform)
            swtl.swttransform(image=loaded_image, save_results=True, save_rootpath='swtres/',
                  edge_func = 'ac', ac_sigma = 1.0, text_mode = 'lb_df',
                  gs_blurr=True, blurr_kernel = (3,3), minrsw = 9, 
                  maxCC_comppx = 5000, maxrsw = 1500, max_angledev = np.pi/6, 
                  acceptCC_aspectratio = 9.0)
            #Find initial boxes for components
            min_bboxes, min_bbox_annotated = swtl.get_extreme_bbox(show=False, padding=1)
            rectsForProcessing = []
            print("Rects size befire filter ")
            print(len(min_bboxes))
            for i in range(len(min_bboxes)):
                if min_bboxes[i][0][0] < 0:
                    min_bboxes[i][0][0] = 0
                if min_bboxes[i][0][1] < 0:
                    min_bboxes[i][0][1] = 0

                if min_bboxes[i][1][0] < 0:
                    min_bboxes[i][1][0] = 0
                if min_bboxes[i][1][1] < 0:
                    min_bboxes[i][1][1] = 0

                if min_bboxes[i][2][0] < 0:
                    min_bboxes[i][2][0] = 0
                if min_bboxes[i][2][1] < 0:
                    min_bboxes[i][2][1] = 0

                if min_bboxes[i][3][0] < 0:
                    min_bboxes[i][3][0] = 0
                if min_bboxes[i][3][1] < 0:
                    min_bboxes[i][3][1] = 0

            rectsForProcessing = min_bboxes
            #Make filtering of found rectangles, join rectangles on the same line
            rectsForProcessing = filterAndJoinRects(rectsForProcessing)
            print("Rects size after first filter ")         
            print(len(rectsForProcessing))
            #Make filtering rects by size.
           ############ rectsFinal = findRectanglesBySize(rectsForProcessing, widthImg)
            min_bboxes = rectsForProcessing
            print("Rects size after filtering")
            print(len(min_bboxes))
            currentIndexForRes = 0
            for i in range(len(min_bboxes)): 
                print("Croped rect details")
                print(str(min_bboxes[i]))
            #Go over into all images                   
            for i in range(len(min_bboxes)):               
                #Get croped image by rectangle
              

                if min_bboxes[i][3][0] - 3 >= 0:
                    min_bboxes[i][3][0] = min_bboxes[i][3][0] -3
                else:
                    min_bboxes[i][3][0] = 0


                if min_bboxes[i][1][0] + 6 <= widthImg:
                    min_bboxes[i][1][0] = min_bboxes[i][1][0] + 6 
              


                cropImage = resImg[min_bboxes[i][3][1]:min_bboxes[i][1][1],  min_bboxes[i][3][0]:min_bboxes[i][1][0]]              
                scale_percent = 170 # percent of original size
                width = int(cropImage.shape[1] * scale_percent / 100)
                height = int(cropImage.shape[0] * scale_percent / 100)               
                if height == 0 or width == 0:
                    continue
                dim = (width, height)  
                #Resize croped rect  
                img = cv2.resize(cropImage, dim, interpolation = cv2.INTER_AREA)
                #Call preprocessing , filtering
                img = image_smoothening(img)
                #Call tesseract for text recognition on cropped image
                recogText = pytesseract.image_to_string(img, config=custom_config)       
                #Save cropped image and text in corresponding files        
                resImagePathFinal = outputFolderPath + '/' + str(currentIndexForRes) + '.jpg'
                resTextPathFinal = outputFolderPath + '/' + str(currentIndexForRes) + '.txt'
                resTextFile = open(resTextPathFinal,"w")
                resTextFile.write(recogText)
                resTextFile.close()
                cv2.imwrite(resImagePathFinal, cropImage)
                currentIndexForRes = currentIndexForRes + 1    
            #Draw detected rectangles and save result image 
            for i in range(len(min_bboxes)):
                r = random.randint(0, 255)
                g = random.randint(0, 255) 
                b = random.randint(0, 255)
                rand_color = (r, g, b)
                #Draw detected line rectangles on image and save 
                cv2.rectangle(resImg,(min_bboxes[i][3][0]-3,min_bboxes[i][3][1]-3),(min_bboxes[i][1][0]+6,min_bboxes[i][1][1]+6),rand_color,2)
            cv2.imwrite(resImagePath, resImg)
            print("Processing of " + inputImagePath)
            print('Finished !!!!!!!!!')

if __name__ == "__main__":
    main()