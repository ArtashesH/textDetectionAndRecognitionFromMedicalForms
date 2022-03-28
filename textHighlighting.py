 # importing modules
import cv2
import random
from numpy.core.numeric import outer
import pytesseract
import csv
import sys
import glob
import shutil
import os
from PIL import Image
import tempfile
from pdf2image import convert_from_path
from PyPDF3 import PdfFileWriter, PdfFileReader
from pytesseract.pytesseract import Output


def generateImagesFromPdfAndHighlightTexts(inputPdfPath, textForHighlight):
    outputImagesDirectory = 'output'
    try:
        shutil.rmtree(outputImagesDirectory)
    except OSError as e:
        print("output folder does not exist")

    pdfname=inputPdfPath
    images = convert_from_path(pdfname, poppler_path='poppler-0.68.0/bin')
    i = 1
    countOfPages=len(images)
    isExist = os.path.exists(outputImagesDirectory)
    #if not(isExist):
    os.mkdir(outputImagesDirectory)
    print("Number of pages in PDF="+str(countOfPages))
    for image in images:
        extractedImageSavePath = outputImagesDirectory + '/' + str(i) + '.jpg'
        image.save( extractedImageSavePath, 'JPEG')
        highlightTextRegions(extractedImageSavePath, textForHighlight)
        i = i + 1

def highlightTextRegions(inputImagePath, textForHighlight):

      #Setting path to tesseract ocr 
    pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
     # reading image using opencv   
    searchTextInImage = textForHighlight
    image = cv2.imread(inputImagePath)

    #converting image into gray scale image

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # converting it to binary image by Thresholding

    # this step is require if you have colored image because if you skip this part

    # then tesseract won't able to detect text correctly and this will give incorrect result

    gray_image = cv2.blur(gray_image, (5,5))
    threshold_img =  gray_image.copy() #cv2.threshold(gray_image, 200, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

     # display image

   # cv2.imshow('threshold image', threshold_img)

     # Maintain output window until user presses a key

   # cv2.waitKey(0)

    # Destroying present windows on screen

   # cv2.destroyAllWindows()


    #configuring parameters for tesseract

    custom_config = r'--oem 3 --psm 6'

    # now feeding image to tesseract

    details = pytesseract.image_to_data(threshold_img, output_type=  Output.DICT, config=custom_config, lang='eng')

   # print(details.keys())

    total_boxes = len(details['text'])
    imageDraw = image.copy()

    threshold_img = cv2.cvtColor(threshold_img, cv2.COLOR_GRAY2RGB)
    for sequence_number in range(total_boxes):
        (x, y, w, h) = (details['left'][sequence_number], details['top'][sequence_number], details['width'][sequence_number],  details['height'][sequence_number])
      #  print(details['text'][sequence_number])
        queryStr = searchTextInImage.lower()
        searchStr = str(details['text'][sequence_number]).lower()
        if queryStr in  searchStr:
            cv2.rectangle(imageDraw, (x, y), (x + w, y + h), (0, 0, 255), -1)
        r = random.randint(0,255)
        g = random.randint(0,255)
        b = random.randint(0,255)
        threshold_img = cv2.rectangle(threshold_img, (x, y), (x + w, y + h), (r, g, b), 2)

   # cv2.destroyAllWindows()
    alpha = 0.5
    imageDrawNew = cv2.addWeighted(imageDraw, alpha, image, 1 - alpha, 0)
    cv2.imwrite(inputImagePath, imageDrawNew)
    #cv2.imwrite("threshImgRes.png",threshold_img)

def writeResultImagesToPdf(resImagesFolderPath, resPdfPath):
    imageList = []
    for filename in os.listdir(resImagesFolderPath):
        image_1 = Image.open(resImagesFolderPath + '/' + filename)
        im_1 = image_1.convert('RGB')
        imageList.append(im_1)
    im_1.save(resPdfPath, save_all=True, append_images=imageList[0:len(imageList)-1])
   


def  main():

    if len(sys.argv[1:]) != 2:
        print("Please call script with input pdf path and  search text like \n");
        print("python  textHighlighting.py  inputPdfFilePath searchText")
        return
    
    inputPdfPath = str(sys.argv[1])
    textForHighlight = str(sys.argv[2])

    generateImagesFromPdfAndHighlightTexts(inputPdfPath, textForHighlight)
    outputPdfPath =  inputPdfPath.split('.pdf')[0]  + '_res.pdf'
    print(outputPdfPath)
    writeResultImagesToPdf('output', outputPdfPath)

   ## parse_text = []

   ### word_list = []

  ###  last_word = ''

   ### for word in details['text']:
    ###    if word!='':
     ###       word_list.append(word)
     ###       last_word = word
     ###   if (last_word!='' and word == '') or (word==details['text'][-1]):
      ###      parse_text.append(word_list)
       ###     word_list = []



###    with open('result_text.txt',  'w', newline="") as file:
  ###      csv.writer(file, delimiter=" ").writerows(parse_text)



if __name__ == "__main__":
    main()