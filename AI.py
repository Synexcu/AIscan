import cv2
import numpy as np
import utils
# import sys
import argparse
import requests

### AI MODULE ###

def main (path, 
          questions, choices, 
          answers
          ):

    ### DEFINING
    ## Online Path
    resp = requests.get(path, stream=True).raw
    onlineArr = np.asarray(bytearray(resp.read()), dtype=np.uint8)
    imgOnline = cv2.imdecode(onlineArr, cv2.IMREAD_COLOR)

    widthImg = 700
    heightImg = 700

    letter_to_number = {
            'A': 0,
            'B': 1,
            'C': 2,
            'D': 3,
            'E': 4}

    # imgOnline = cv2.resize(imgOnline,(widthImg, heightImg))
    img = imgOnline

    ## Offline path
    # img = cv2.imread(path)
    # cv2.imshow('path', img)


    ### PRE-PROCESSING
    img = cv2.resize(img,(widthImg, heightImg))
    imgContours = img.copy()
    imgBiggestContours = img.copy()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5,5), 1)
    imgCanny = cv2.Canny(imgBlur, 10,50)

    ### FINDING ALL CONTOURS
    contours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(imgContours, 
                    contours, 
                    -1, 
                    (0, 255, 0), #COLOR CODE
                    10)

    ## FINDING ALL RECTANGLES
    rectCon = utils.rectContour(contours)
    biggestContour = utils.getCornerPoints(rectCon[0])
    gradePoints = utils.getCornerPoints(rectCon[1]) #Set Grade Area by 2nd biggest
    # print (biggestContour)


    if biggestContour.size != 0 and gradePoints.size != 0:
        cv2.drawContours(imgBiggestContours, biggestContour, -1, (0, 255, 0), 20)
        cv2.drawContours(imgBiggestContours, gradePoints, -1, (255, 0, 0), 20)

        biggestContour = utils.reorder(biggestContour)
        gradePoints = utils.reorder(gradePoints)

        ## Answer Column area
        pt1 = np.float32(biggestContour)
        pt2 = np.float32([[0,0],[widthImg, 0], [0, heightImg], [widthImg, heightImg]])
        matrix = cv2.getPerspectiveTransform(pt1, pt2)
        imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg)) #Bird View Perspective.

        ## Grade area
        ptG1 = np.float32(gradePoints)
        ptG2 = np.float32([[0,0],[325, 0], [0, 150], [325, 150]]) # 325 (widthImg) 150 (heightImg) [Change accordingly]
        matrixG = cv2.getPerspectiveTransform(ptG1, ptG2)
        imgGradeDisplay = cv2.warpPerspective(img, matrixG, (325, 150)) #Bird View Perspective for Grade.
        # cv2.imshow("Grade", imgGradeDisplay)

        ## Apply answer threshold
        imgWarpGray = cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2GRAY)
        imgThresh = cv2.threshold(imgWarpGray, 170, 255, cv2.THRESH_BINARY_INV)[1]

        boxes = utils.splitBoxes(imgThresh)
        # cv2.imshow("Test", boxes[1]) #Edge
        # print(cv2.countNonZero(boxes[1]), cv2.countNonZero(boxes[2]))

        ## Decide choices minmax value pixels | Getting no zero pixel value of each box
        myPixelval = np.zeros((questions, choices))
        countC = 0 #Count Columns
        countR = 0 #Count Rows

        for image in boxes:
            totalixels = cv2.countNonZero(image)
            myPixelval[countR][countC] = totalixels
            countC += 1
            if (countC == choices):
                countR += 1 ; countC=0
        # print(myPixelval)

        ## See biggest pixel value and get array(choice) value | Finding Index values of the markings
        myIndex = []
        for x in range (0, questions):
            arr = myPixelval[x]
            # print("arr", arr)
            myIndexVal = np.where(arr==np.amax(arr))
            # print(myIndexVal[0])
            myIndex.append(myIndexVal[0][0])
        print(myIndex)

        # letter_to_number = {
        #     'A': 0,
        #     'B': 1,
        #     'C': 2,
        #     'D': 3,
        #     'E': 4
        #     }
        
        numeric_answers = [letter_to_number.get(letter, -1) for letter in answers]

        ## GRADING (RIGHT/WRONG)
        grading = []
        for x in range (0, questions):
            if numeric_answers[x] == myIndex[x]:
                grading.append(1)
            else:
                grading.append(0)
        print(grading) #prints grading where if the answer and the choice is correct then change to 1. Wrong = 0
        score = (sum(grading)/questions)*100 ## FINAL SCORE
        print(score)

        return myIndex, grading, score
    
    return None, None, None



    imgBlank = np.zeros_like(img) #Decoy Image for imgArray

    # Put into Image Array
    imgArray = ([img, imgGray, imgBlur, imgCanny],
                [imgContours, imgBiggestContours, imgWarpColored, imgThresh])

    imgStacked = utils.stackImages(imgArray, 0.5)


    ### SHOW
    # cv2.imshow("Stacked Images",imgStacked)
    # cv2.waitKey(0)

if __name__ == "__main__":
    ### INIT PATH AND IMAGES
    # path="2.jpg"
    parser = argparse.ArgumentParser(description="Process an image.")
    parser.add_argument("path", type=str, help="Path to the image file") #Image file name (or path)
    parser.add_argument("--questions", type=int, default=5, help="Number of questions") #Number of Questions
    parser.add_argument("--choices", type=int, default=5, help="Number of choices per questions") #Number of choices in a question
    parser.add_argument("--answers", nargs="+", type=str, help="List of all answers (one per question)") #Answer Key
    # [1,2,0,1,4] #ABCDE answer start from 0,1, etc. A=0

    widthImg = 700
    heightImg = 700

    questions = 5
    choices = 5
    # answers = "B B B B B"

    args = parser.parse_args()

    ## RUN MAIN
    main(args.path, 
         args.questions, args.choices, 
         args.answers
         )