from loguru import logger
import time
from PIL import Image
import pytesseract
from pytesseract import pytesseract
import cv2
import csv
import numpy as np
from dotenv import load_dotenv


def teste_01_tesseract() -> None:

    # ---------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------

    # img00 = cv2.imread('image.png')
    # img01 = cv2.imread('image1.png')

    # gray_image = cv2.cvtColor(img00, cv2.COLOR_BGR2GRAY) 
    # ret, threshimg = cv2.threshold(gray_image, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV) 
    # rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
    # dilation = cv2.dilate(threshimg, rect_kernel, iterations = 1)
    # img_contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # gray_image = cv2.cvtColor(img00, cv2.COLOR_BGR2GRAY)
    # threshold_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1] 

    # cv2.imshow("Faces", threshold_img) # img00 # img01
    # cv2.waitKey()
    # cv2.destroyAllWindows()

    # ---------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------

    # img = cv2.imread('image.png')

    # gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # thresh_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # cnts = cv2.findContours(thresh_img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    # for cnt in cnts:
    #     approx = cv2.contourArea(cnt)
    #     # print(approx)

    # cv2.imshow('image', img)
    # cv2.imshow('Binary',thresh_img)
    # cv2.waitKey()


    # ---------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------

    # # Read the images from the file
    # # small_image = cv2.imread('image4.png')  # image3
    # small_image_2 = cv2.imread('image5.png')  # image5
    # large_image = cv2.imread('image.png')  # image1
    # # w, h = small_image.shape[:-1]
    # w2, h2 = small_image_2.shape[:-1]

    # # result = cv2.matchTemplate(small_image, large_image, cv2.TM_SQDIFF_NORMED) #  cv2.TM_SQDIFF_NORMED # cv2.TM_SQDIFF
    # # result = cv2.matchTemplate(large_image, small_image, cv2.TM_CCOEFF_NORMED)
    # result2 = cv2.matchTemplate(small_image_2, large_image, cv2.TM_CCOEFF_NORMED)

    # # threshold = .8
    # # loc = np.where(result >= threshold)
    # # for pt in zip(*loc[::-1]): 
    # #     cv2.rectangle(large_image, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
    # # cv2.imwrite('result1.png', large_image)

    # threshold = .8
    # loc = np.where(result2 >= threshold)
    # for pt in zip(*loc[::-1]): 
    #     cv2.rectangle(large_image, pt, (pt[0] + w2, pt[1] + h2), (0, 0, 255), 2)
    # # cv2.imwrite('result2.png', large_image)


    # # mn,_,mnLoc,_ = cv2.minMaxLoc(result) # We want the minimum squared difference
    # # MPx,MPy = mnLoc # Draw the rectangle:  Extract the coordinates of our best match
    # # trows,tcols = small_image.shape[:2]  # Step 2: Get the size of the template. This is the same size as the match.
    # # cv2.rectangle(large_image, (MPx,MPy),(MPx+tcols,MPy+trows),(0,0,255),2) # Step 3: Draw the rectangle on large_image
    # cv2.imshow('output', large_image) # Display the original image with the rectangle around the match.
    # cv2.waitKey(0) # The image is only displayed if we call this

    # ---------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------

    #### 1 - Preprocessing Image
    def preProcess(img):
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # CONVERT IMAGE TO GRAY SCALE
        imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)  # ADD GAUSSIAN BLUR
        imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, 1, 1, 11, 2)  # APPLY ADAPTIVE THRESHOLD
        return imgThreshold

    #### 3 - Reorder points for Warp Perspective
    def reorder(myPoints):
        myPoints = myPoints.reshape((4, 2))
        myPointsNew = np.zeros((4, 1, 2), dtype=np.int32)
        add = myPoints.sum(1)
        myPointsNew[0] = myPoints[np.argmin(add)]
        myPointsNew[3] =myPoints[np.argmax(add)]
        diff = np.diff(myPoints, axis=1)
        myPointsNew[1] =myPoints[np.argmin(diff)]
        myPointsNew[2] = myPoints[np.argmax(diff)]
        return myPointsNew
        
    #### 3 - FINDING THE BIGGEST COUNTOUR ASSUING THAT IS THE SUDUKO PUZZLE
    def biggestContour(contours):
        biggest = np.array([])
        max_area = 0
        for i in contours:
            area = cv2.contourArea(i)
            if area > 50:
                peri = cv2.arcLength(i, True)
                approx = cv2.approxPolyDP(i, 0.02 * peri, True)
                if area > max_area and len(approx) == 4:
                    biggest = approx
                    max_area = area
        return biggest,max_area
        
                
    #### 4 - TO SPLIT THE IMAGE INTO 81 DIFFRENT IMAGES
    def splitBoxes(img):
        rows = np.vsplit(img,9)
        boxes=[]
        for r in rows:
            cols= np.hsplit(r,9)
            for box in cols:
                boxes.append(box)
        return boxes
        
    heightImg = 450
    widthImg = 450
    img = cv2.imread('image.png')
    img = cv2.resize(img, (widthImg, heightImg))  # RESIZE IMAGE TO MAKE IT A SQUARE IMAGE
    imgBlank = np.zeros((heightImg, widthImg, 3), np.uint8)  # CREATE A BLANK IMAGE FOR TESTING DEBUGING IF REQUIRED
    imgThreshold = preProcess(img)

    # #### 2. FIND ALL COUNTOURS
    imgContours = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
    imgBigContour = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
    contours, hierarchy = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # FIND ALL CONTOURS
    cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 3) # DRAW ALL DETECTED CONTOURS

    #### 3. FIND THE BIGGEST COUNTOUR AND USE IT AS SUDOKU
    biggest, maxArea = biggestContour(contours) # FIND THE BIGGEST CONTOUR
    # print(biggest)
    if biggest.size != 0:
        biggest = reorder(biggest)
        # print(biggest)
        cv2.drawContours(imgBigContour, biggest, -1, (0, 0, 255), 25) # DRAW THE BIGGEST CONTOUR
        pts1 = np.float32(biggest) # PREPARE POINTS FOR WARP
        pts2 = np.float32([[0, 0],[widthImg, 0], [0, heightImg],[widthImg, heightImg]]) # PREPARE POINTS FOR WARP
        matrix = cv2.getPerspectiveTransform(pts1, pts2) # GER
        imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg))
        print(imgWarpColored)
        #imgDetectedDigits = imgBlank.copy()
        #imgWarpColored = cv2.cvtColor(imgWarpColored,cv2.COLOR_BGR2GRAY)
        #print(imgDetectedDigits)

        #### 4. SPLIT THE IMAGE AND FIND EACH DIGIT AVAILABLE
        imgSolvedDigits = imgBlank.copy()
        boxes = splitBoxes(imgWarpColored)
        # print(len(boxes))
        # print(boxes)
        # cv2.imshow("Sample",boxes[65])

        
    cv2.imshow('output', imgWarpColored) # Display the original image with the rectangle around the match.
    cv2.waitKey(0) # The image is only displayed if we call this

    # python main.py
    return



    # ---------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------





    image_path  = 'image2.png'  # 'image.png'  # r'D:\examplepdf2image.png'
    pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    # img = Image.open(fp=image_path)
    # text = pytesseract.image_to_string(image=img)
    # logger.info("#1:", text[:-1])

    # img = cv2.imread(filename=image_path)
    # config = ('-l eng --oem 1 --psm 3')
    # text = pytesseract.image_to_string(image=img, config=config)
    # logger.info("#2:", text.split('\n'))

    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert the image to gray scale 
    # ret, threshimg = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)  # OTSU threshold performing
    # rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))  # Specifying kernel size and structure shape.  
    # dilation = cv2.dilate(threshimg, rect_kernel, iterations = 1) # Appplying dilation on the threshold image
    # img_contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) # getting contours 
    # for cnt in img_contours: # Loop over contours and crop and extract the text file
    #     x, y, w, h = cv2.boundingRect(cnt) 
    #     rect = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2) # Drawing a rectangle
    #     cropped_img = img[y:y + h, x:x + w] # Cropping the text block  
    #     text = pytesseract.image_to_string(cropped_img) # Applying tesseract OCR on the cropped image 
    #     file = open("recognized.txt", "a") # Open the text file in append mode 
    #     file.write(text + "\n")  # Appending the text into file 
    #     file.close # Close the file 

    image = cv2.imread(filename=image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #converting image into gray scale image
    threshold_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]  # this step is require if you have colored image because if you skip this part then tesseract won't able to detect text correctly and this will give incorrect result

    custom_config = r'--oem 3 --psm 6'  #configuring parameters for tesseract
    details = pytesseract.image_to_data(threshold_img, output_type=pytesseract.Output.DICT, config=custom_config, lang='eng') # now feeding image to tesseract

    # logger.info(f"#3: {details.keys()}")
    # total_boxes = len(details['text'])
    # #logger.info(f"#4: {total_boxes}")
    # for sequence_number in range(total_boxes):
    #     # print("conf", int(str(details['conf'][sequence_number]).replace('.','').strip()))
    #     if int(str(details['conf'][sequence_number]).replace('.','').strip()) > 30:  # if int(details['conf'][sequence_number]) > 30:
    #         (x, y, w, h) = (details['left'][sequence_number], details['top'][sequence_number], details['width'][sequence_number],  details['height'][sequence_number])
    #         threshold_img = cv2.rectangle(threshold_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    # cv2.imshow('captured text', threshold_img) # display image
    # cv2.waitKey(0)# Maintain output window until user presses a key
    # cv2.destroyAllWindows()# Destroying present windows on screen

    parse_text = []
    word_list = []
    last_word = ''
    for word in details['text']:
        if word!='':
            word = str(word).strip() # .replace('/','').replace(')','').replace(';','').replace('|','').strip()
            word = ''.join([str(s) for s in word if s.isdigit()])
            # logger.info(f"word-antes: '{word} -- word-depois: '{word_new}'")
            word_list.append(word)
            last_word = word
        if (last_word != '' and word == '') or (word==details['text'][-1]):
            parse_text.append(word_list)
            word_list = []
    # logger.info(f"#5: {parse_text}")

    # logger.info(f"Antes")
    for idx, row in enumerate(parse_text):
        #logger.info(f"row: '{row}' - idx: '{parse_text[idx]}'")
        parse_text[idx] = ''.join(row)
    # logger.info(f"Depois")
    for idx, row in enumerate(parse_text):
        #logger.info(f"row: '{row}' - idx: '{parse_text[idx]}'")
        logger.info(f"'{row}'")

    with open(file='result_text2.txt', mode='w', newline="") as file:
        csv.writer(file, delimiter=" ").writerows(parse_text)


def teste_02_tesseract() -> None:

    pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    config = r"--psm 6 --oem 3"
    image = Image.open(fp="introducao.png")
    text = pytesseract.image_to_string(image=image, config=config)
    logger.info(f'{text=}') 

    # https://pyimagesearch.com/2018/09/17/opencv-ocr-and-text-recognition-with-tesseract/
    # https://www.projectpro.io/article/how-to-train-tesseract-ocr-python/561

    # $ tesseract --help-oem
    # OCR Engine modes:
    #   0    Legacy engine only.
    #   1    Neural nets LSTM engine only.
    #   2    Legacy + LSTM engines.
    #   3    Default, based on what is available.
    # We’ll be using --oem 1 to indicate that we wish to use the deep learning LSTM engine only.

    # $ tesseract --help-psm
    # Page segmentation modes:
    #   0    Orientation and script detection (OSD) only.
    #   1    Automatic page segmentation with OSD.
    #   2    Automatic page segmentation, but no OSD, or OCR.
    #   3    Fully automatic page segmentation, but no OSD. (Default)
    #   4    Assume a single column of text of variable sizes.
    #   5    Assume a single uniform block of vertically aligned text.
    #   6    Assume a single uniform block of text.
    #   7    Treat the image as a single text line.
    #   8    Treat the image as a single word.
    #   9    Treat the image as a single word in a circle.
    #  10    Treat the image as a single character.
    #  11    Sparse text. Find as much text as possible in no particular order.
    #  12    Sparse text with OSD.
    #  13    Raw line. Treat the image as a single text line, bypassing hacks that are Tesseract-specific.
    # For OCR’ing text ROIs I’ve found that modes 6 and 7 work well, but if you’re OCR’ing large blocks of text then you may want to try 3 , the default mode.



def main():
    try:

        logger.info(f'Inicio') 
        start_time = time.perf_counter()  # time.time()  # time.perf_counter()  # time.perf_counter_ns()  # time.process_time()

        # teste_01_tesseract()
        teste_02_tesseract()

        # tesseract introducao.png stdout

        # python main.py

        end_time = time.perf_counter() - start_time  # time.time() # time.perf_counter() # time.perf_counter_ns() # time.process_time()
        logger.info(f"Fim - Done in {end_time:.2f}s")

    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.error(f'Falha Geral(main): "{str(e)}"')


if __name__ == '__main__':
    main()

# py -3 -m venv .venv
# python -m pip install --upgrade opencv-python
# python -m pip install --upgrade pytesseract
# python -m pip install --upgrade tesseract
# cd c:/Users/chris/Desktop/CMS Python/xxxxxx
# .venv\scripts\activate
# python main.py

