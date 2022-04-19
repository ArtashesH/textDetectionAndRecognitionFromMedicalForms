
# Import module
import threading
import time
import textHighlighting

inputPdfPath = str('TextHighlighting/Aadhaar_1.pdf')
textForHighlight = '676559772815'
   
inputPdfPath1 = str('TextHighlighting/Aadhaar2.pdf')
textForHighlight1 = '772480577698'

    
inputPdfPath2 = str('TextHighlighting/sample1-bridge.pdf')
textForHighlight2 = 'bridge'

inputPdfPath3 = str('TextHighlighting/sample2-400280047659.pdf')
textForHighlight3 = '400280047659'

inputPdfPath4 = str('TextHighlighting/sample3-party.pdf')
textForHighlight4 = 'party'
  

  
# Creating 5 threads that execute the same 
# function with different parameters


start_time = time.time()
for f in range(200):
  #  textHighlighting.readAndHighlightPdf(inputPdfPath,textForHighlight)
  #  textHighlighting.readAndHighlightPdf(inputPdfPath1,textForHighlight1)
  #  textHighlighting.readAndHighlightPdf(inputPdfPath2,textForHighlight2)
  #  continue
  #  textHighlighting.readAndHighlightPdf(inputPdfPath3,textForHighlight3)
  #  textHighlighting.readAndHighlightPdf(inputPdfPath4,textForHighlight4)
  #  continue
    thread1 = threading.Thread(target=textHighlighting.readAndHighlightPdf, 
                           args=(inputPdfPath,textForHighlight ))
    time.sleep(0.5)
    thread2 = threading.Thread(target=textHighlighting.readAndHighlightPdf, 
                           args=(inputPdfPath1, textForHighlight1))
    time.sleep(0.5)
    thread3 = threading.Thread(target= textHighlighting.readAndHighlightPdf, 
                           args=(inputPdfPath2, textForHighlight2))
    time.sleep(0.5)
    thread4 = threading.Thread(target=textHighlighting.readAndHighlightPdf, 
                           args=(inputPdfPath3,textForHighlight3 ))
    time.sleep(0.5)
    thread5 = threading.Thread(target=textHighlighting.readAndHighlightPdf, 
                           args=(inputPdfPath4, textForHighlight4))
    time.sleep(0.5)
    # Start the threads
    thread1.start()
    
    thread2.start()
   
    thread3.start()
   
    thread4.start()
   
    thread5.start()
    # Join the threads before 
    # moving further
    
    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
    thread5.join()
   

print ('The script took {0} second !'.format(time.time() - start_time))    


  

