import cv2 
import pytesseract
import numpy as np
import random
import os
import sys
import glob


#Preprocessing and applying gaussian blur filter
def image_smoothening(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img, (3, 3), 0)
    return img


def main():

   #Get input folder path for processing as an input argument    
    if len(sys.argv[1:]) != 1:
        print("Please call script with input folder path");
        return

    #Setting path to tesseract ocr 
    pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
    
    #Setting configurations
    custom_config = r'--oem 3  --psm 6 -l eng '
    folder = str(sys.argv[1])
    #Creating txt file for writing recognized texts
    resTextPathFinal = folder  +  '/res.txt'
    resTextFile = open(resTextPathFinal,"w")
    folderImages =  os.listdir(folder) 
    fileNamesList = open(folder + '/AccEst.txt',"w")
    #Read and process all images in jpg, png, jpeg formats from input folder
    for filename in folderImages:
        if filename.endswith(('.jpg', '.png', '.jpeg')):
            print("current file ")
            print(filename)
            fileNamesList.write(filename)
            fileNamesList.write('\n')      
            #Read current image for processing
            img = cv2.imread(os.path.join(folder,filename))
            scale_percent = 170 # percent of original size
            #Resizing image
            width = int(img.shape[1] * scale_percent / 100)
            height = int(img.shape[0] * scale_percent / 100)
            dim = (width, height)
            img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
            #Some preprocessing
            img = image_smoothening(img)
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            #Call tesseract for text recognition
            d = pytesseract.image_to_data(img, output_type= pytesseract.Output.DICT)
            n_boxes = len(d['level'])
            for i in range(n_boxes):
                (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                r = random.randint(0, 255)
                g = random.randint(0, 255) 
                b = random.randint(0, 255)
                rand_color = (r, g, b)
                cv2.imwrite("resFromOCR.png", img)
                cv2.imshow("img", img)
                cv2.waitKey(10)
            #Getting output string      
            resTextFinal = filename
            resTextFinal = resTextFinal + '\n' +  pytesseract.image_to_string(img, config=custom_config)
            resTextFile.write(resTextFinal)
            resTextFile.write('\n')
            print("wrote last string ")
            print(resTextFinal)
    #Results will be written in res.txt file , in the same directory
    resTextFile.close()


if __name__ == "__main__":
    main()
