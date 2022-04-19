 # importing modules
import cv2
import numpy as np
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
import fitz
from pdf2image import convert_from_path
from PyPDF3 import PdfFileWriter, PdfFileReader
from pytesseract.pytesseract import Output
from pdfrw import PdfReader


def findingWholeStringFromComp(detailsOfImage, searchString, currentBoxIndex,  sequenceNumberStart,  sequenceNumberEnd):
 
    finalIndexesForDraw = []
    finalIndexesForDraw.append(sequenceNumberStart)
    finalIndexesForDraw.append(sequenceNumberEnd)
    total_boxes = len(detailsOfImage['text'])
    sequenceNumberStart = -1
    sequenceNumberEnd = -1
    for sequence_number in range(currentBoxIndex,total_boxes):
        (x, y, w, h) = (detailsOfImage['left'][sequence_number], detailsOfImage['top'][sequence_number], detailsOfImage['width'][sequence_number],  detailsOfImage['height'][sequence_number])
        queryStr = searchString.lower()
        searchStr = str(detailsOfImage['text'][sequence_number]).lower()        
        if  (  searchStr  in queryStr  and len(searchStr) != 0) :            
            sequenceNumberStart = sequence_number
            sequence_number = sequence_number + 1
            while sequence_number < total_boxes:                
                 searchStr1 = str(detailsOfImage['text'][sequence_number]).lower()                 
                 if  (  searchStr1  in queryStr  and len(searchStr1) != 0) :
                     sequence_number = sequence_number + 1
                     searchStr = searchStr + searchStr1
                 else :
                     sequenceNumberStart = -1
                     sequenceNumberEnd = -1
                     break
                 if queryStr in searchStr:
                     sequenceNumberEnd = sequence_number 
                     finalIndexesForDraw[0] = sequenceNumberStart
                     finalIndexesForDraw[1] = sequenceNumberEnd
                     return finalIndexesForDraw

    return finalIndexesForDraw
            

def generateImagesFromPdfAndHighlightTexts(inputPdfPath, textForHighlight,outputPdfPath):
    outputImagesDirectory = 'output'
   ########## try:
   ########     shutil.rmtree(outputImagesDirectory)
 ###########   except OSError as e:
   ############     print("output folder does not exist")

    isExist = os.path.exists(outputImagesDirectory)
   # os.mkdir(outputImagesDirectory)
    pdfName=inputPdfPath
    #docPdf = fitz.open(pdfname)
    #pageCount = docPdf.page_count
    #for i in range(pageCount):
    #    page = docPdf.load_page(i)  
     #   pix = page.get_pixmap()

      #  extractedImageSavePath = outputImagesDirectory + '/' + str(i) + '.jpg'
      #  pix.save(extractedImageSavePath)
      #  highlightTextRegions(extractedImageSavePath, textForHighlight)



    #return
   
    #pdf = PdfReader(pdfname)
    #firstPage = pdf.pages[0].MediaBox
    #print(firstPage)
    #return

   
    #docPa = fitz.open(pdfname)
   # pagePa = docPa[0]
   # docPa.close()
   # print(pagePa.rect.width, pagePa.rect.height)
    #print(pagePa.mediabox.width, pagePa.mediabox.height)


    images = convert_from_path(pdfName, dpi=250,  use_cropbox=True,  poppler_path='poppler-0.68.0/bin')
    
    #print("image size")
   # print(np.array(images[0]).shape)

    i = 1
    countOfPages=len(images)
    
    if not(isExist):
        os.mkdir(outputImagesDirectory)
    ###########print("Number of pages in PDF="+str(countOfPages))
    for image in images:
       
        fileName = os.path.basename(inputPdfPath)       # saveImagePathFinal = inputPdfPath.split('/')[1]
        extractedImageSavePath = outputImagesDirectory + '/' + fileName.split('/')[-1].split('.pdf')[0] + '_' + str(i) + '.jpg'
      
        image.save( extractedImageSavePath, 'JPEG')
        #return
        highlightTextRegions(extractedImageSavePath, textForHighlight,pdfName,i-1,outputPdfPath)
        i = i + 1
            
def highlightTextRegions(inputImagePath, textForHighlight, pdfName, pageIndex,outputPdfPath):

    #Setting path to tesseract ocr 
    pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
     # reading image using opencv   
    searchTextInImage = textForHighlight

    docPa = fitz.open(pdfName)
    pagePa = docPa[pageIndex]
    pdfPageWidth = pagePa.rect.width
    pdfPageHeight = pagePa.rect.height
  
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
    (x,y,w,h) = (0,0,0,0)
    for sequence_number in range(total_boxes):
        (x, y, w, h) = (details['left'][sequence_number], details['top'][sequence_number], details['width'][sequence_number],  details['height'][sequence_number])
      #  print(details['text'][sequence_number])
        queryStr = searchTextInImage.lower()
        searchStr = str(details['text'][sequence_number]).lower()
        if  (  queryStr  in searchStr  and len(searchStr) != 0) :  #  searchStr in  queryStr:                      
            cv2.rectangle(imageDraw, (x, y), (x + w, y + h), (0, 0, 255), -1)
         #   print("Rect info ")
          #  print(x)
          #  print(y)
          #  print(x+w)
         #   print(y+h)
          #  print("img draw size ")
         #   print(imageDraw.shape)

            xInPdf = x * pdfPageWidth / imageDraw.shape[1]
            yInPdf = y * pdfPageHeight / imageDraw.shape[0]
            xMaxInPdf =  (x + w) * pdfPageWidth / imageDraw.shape[1]
            yMaxInPdf =  ( y + h ) * pdfPageHeight / imageDraw.shape[0]
           # print("Final results ")
           # print(xInPdf)
           # print(yInPdf)
           # print(xMaxInPdf)
           # print(yMaxInPdf)
            pagePa.draw_rect([xInPdf,yInPdf,xMaxInPdf,yMaxInPdf],  color = (1, 0, 0), stroke_opacity= 0.3, width = 1, fill=(1,0,0), fill_opacity = 0.3)
            docPa.save(outputPdfPath)
        sequenceNumberStart = -1
        sequenceNumberEnd = -1
        if  (  searchStr  in queryStr  and len(searchStr) != 0) :
                indexesForColor  =  findingWholeStringFromComp(details, queryStr, sequence_number, sequenceNumberStart,  sequenceNumberEnd)
                if indexesForColor[0] != -1 and indexesForColor[1] != -1:                    
                    for colorInd in range(indexesForColor[0], indexesForColor[1]):
                        (x, y, w, h) = (details['left'][colorInd], details['top'][colorInd], details['width'][colorInd],  details['height'][colorInd])
                        cv2.rectangle(imageDraw, (x, y), (x + w, y + h), (0, 0, 255), -1)
                      #  print("Rect info1 ")
                       # print(x)
                       # print(y)
                       # print(x+w)
                       # print(y+h)
                       

                        xInPdf = x * pdfPageWidth / imageDraw.shape[1]
                        yInPdf = y * pdfPageHeight / imageDraw.shape[0]
                        xMaxInPdf =  (x + w) * pdfPageWidth / imageDraw.shape[1]
                        yMaxInPdf =  ( y + h ) * pdfPageHeight / imageDraw.shape[0]
                       # print("Final results ")
                      #  print(xInPdf)
                      #  print(yInPdf)
                      #  print(xMaxInPdf)
                      #  print(yMaxInPdf)
                        pagePa.draw_rect([xInPdf,yInPdf,xMaxInPdf,yMaxInPdf],  color = (1, 0, 0), stroke_opacity= 0.3, width = 1, fill=(1,0,0), fill_opacity = 0.3)
                        docPa.save(outputPdfPath)
        
        
        r = random.randint(0,255)
        g = random.randint(0,255)
        b = random.randint(0,255)
       # threshold_img = cv2.rectangle(threshold_img, (x, y), (x + w, y + h), (r, g, b), 2)
       
       
   # cv2.destroyAllWindows()
    alpha = 0.5
    docPa.close()
    imageDrawNew = cv2.addWeighted(imageDraw, alpha, image, 1 - alpha, 0)
  

   # cv2.imwrite(inputImagePath, imageDrawNew)
    #cv2.imwrite("threshImgRes.png",threshold_img)

def writeResultImagesToPdf(resImagesFolderPath, resPdfPath):
    print("call writing")
    imageList = []
    for filename in os.listdir(resImagesFolderPath):

        fileNameImage = os.path.basename(filename)  
        fileNamePdf = os.path.basename(resPdfPath)
        fileNameImgComp = fileNameImage.rsplit('_',1)[0]
        fileNamePdfComp = fileNamePdf.rsplit('_',1)[0]
        if fileNameImgComp == fileNamePdfComp:
            #print('Pdf file path')
            #print(fileNamePdfComp)
            #print('currentImage path')
            #print(fileNameImgComp)
        #extractedImageSavePath = outputImagesDirectory + '/' + fileName.split('/')[-1].split('.pdf')[0] + '_' + str(i) + '.jpg'
            image_1 = Image.open(resImagesFolderPath + '/' + filename)
            
            im_1 = image_1.convert('RGB')
            imageList.append(im_1)
    im_1.save(resPdfPath, save_all=True, append_images=imageList[0:len(imageList)-1])
   



def readAndHighlightPdf(inputPdfPath, textForHighlight):
    outputPdfPath =  inputPdfPath.split('.pdf')[0]  + '_res.pdf'
    generateImagesFromPdfAndHighlightTexts(inputPdfPath, textForHighlight,outputPdfPath)   
   ##### print(outputPdfPath)
   ################ writeResultImagesToPdf('output', outputPdfPath)

def  main():

    if len(sys.argv[1:]) != 2:
        print("Please call script with input pdf path and  search text like \n");
        print("python  textHighlighting.py  inputPdfFilePath searchText")
        return
    
    inputPdfPath = str(sys.argv[1])
    textForHighlight = str(sys.argv[2])
    readAndHighlightPdf(inputPdfPath,textForHighlight)

    

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