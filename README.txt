Those are need packages for environment preparing


Please install python 3.8+  version with pip , then open command line, and install those packages. 

pip install numpy

pip install pytesseract

pip install swtloc==1.0.0.0

pip install opencv-python

pip install pdf2image

pip install pypdf3

pip install glob2

pip install img2pdf

fter packages are installed you can run programs.

python textDetAndSeg.py inputFolderPath


This program is for text detection and recognition from given images.

input - inputFolderPath,  this is input folder path, where is located images, full, for processing. The program will read and process all images
inside of the input folder.

output - for each document, the program will create the folder, with the same, document name, where will place all cropped detected texts, and also txt 
file with the same name, where will be written recognized text, and image_res, which will show detected rectangles.



python textRecognition.py inputFolderPath

This program is for text recognition from given images.

input - inputFolderPath,  this is input folder path, where is located already cropped images, for recognition. The program will read and process all images, and recognition data for all images
will be written in res.txt file, created in the same folder.