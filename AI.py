import cv2
import numpy as np
import utils
# import sys
import argparse
import requests

### AI MODULE ###

def main (path, 
          questions,
          choices, 
          answers
          ):

    ### DEFINING
    widthImg = 700
    heightImg = 700
    
    ## Online Path
    resp = requests.get(path, stream=True).raw
    onlineArr = np.asarray(bytearray(resp.read()), dtype=np.uint8)
    imgOnline = cv2.imdecode(onlineArr, cv2.IMREAD_COLOR)

    imgOnline = cv2.resize(imgOnline,(widthImg, heightImg))
    img = imgOnline


    letter_to_number = {
            'A': 0,
            'B': 1,
            'C': 2,
            'D': 3,
            'E': 4}


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
    # print("This is my contours: ", contours)
    
    cv2.drawContours(imgContours, 
                    contours, 
                    -1, 
                    (0, 255, 0), #COLOR CODE
                    10)

    def getbigcontours(i):
        res = utils.getCornerPoints(rectCon[i])
        return res
    
    boxSequence = int(questions / 5)
    # print("This is box sequence: ", boxSequence)

    ## FINDING ALL RECTANGLES
    rectCon = utils.rectContour(contours)
    contour_points = [utils.getCornerPoints(rectCon[i]) for i in range(10)]
    print("This is contour points: ", contour_points)

    sorted_contours = utils.sort_contours(contour_points, boxSequence)
    print("The sorted array of the first sub-arrays based on y-coordinate is:")
    print(sorted_contours)

    # firstContour = sorted_contours[0]
    # print("This is firstContour: ", firstContour)

    # biggestContour = utils.getCornerPoints(rectCon[1])
    # print("This is biggestContour: ", biggestContour)
    # loopContours = firstContour
    # gradePoints = utils.getCornerPoints(rectCon[20]) #Set Grade Area #20


    # print("This is biggest Contour [in blue]: ", getbigcontours(0))
    # print("This is my 2nd biggest contour [in green]: ", getbigcontours(1))
    # print("This is my 3rd biggest contour [in red]: ", getbigcontours(2))
    # print("This is my 4th biggest contour [in gray]: ", getbigcontours(3))
    # print("This is my 5th biggest contour [in blue ish gray]: ", getbigcontours(4))
    # print("This is my 6th biggest contour [in blue ish gray]: ", getbigcontours(5))
    # print("This is my 7th biggest contour [in gray]: ", getbigcontours(6))
    # print("This is my 8th biggest contour [in yellow]: ", getbigcontours(7))
    # print("This is my 9th biggest contour [in pink]: ", getbigcontours(8))
    # print("This is my 10th biggest contour [in purple]: ", getbigcontours(9))



    if questions % 5 == 0:
        o = 0
        all_myIndex = []
        all_grading = []
        numeric_answers = [letter_to_number.get(letter, -1) for letter in answers]
        for o in range(boxSequence):

            loopContour = sorted_contours[o]
            print("This is", o, "contour: ", loopContour)
            
            # cv2.drawContours(imgBiggestContours, gradePoints, -1, (255, 0, 0), 20)
            # cv2.drawContours(imgBiggestContours, getbigcontours(0), -1, (255, 0, 0), 20) # 3th answer box (Blue)
            # cv2.drawContours(imgBiggestContours, getbigcontours(1), -1, (0, 255, 0), 20) # 1st answer box (Green)
            # cv2.drawContours(imgBiggestContours, getbigcontours(2), -1, (0,0,255), 20) # 5th answer box (Red)
            # cv2.drawContours(imgBiggestContours, getbigcontours(3), -1, (150, 150, 150), 20) # 2nd answer box (Gray)
            # cv2.drawContours(imgBiggestContours, getbigcontours(4), -1, (255, 150, 150), 20) # 4th answer box (Blue ish Gray)
            # cv2.drawContours(imgBiggestContours, getbigcontours(5), -1, (255, 150, 150), 20) # 6nd answer box (Blue ish Gray)
            # cv2.drawContours(imgBiggestContours, getbigcontours(6), -1, (150, 150, 150), 20) # 8th answer box (Gray)
            # cv2.drawContours(imgBiggestContours, getbigcontours(7), -1, (0, 255, 255), 20) # 9th answer box (Yellow)
            # cv2.drawContours(imgBiggestContours, getbigcontours(8), -1, (150, 150, 255), 20) # 7th answer box (Pink)
            # cv2.drawContours(imgBiggestContours, getbigcontours(9), -1, (255, 0, 255), 20) # 10th answer box (Purple)
            

            loopContour = utils.reorder(loopContour)
            # print("This is biggest contour with reorder: ", biggestContour)
            # gradePoints = utils.reorder(gradePoints)

            ## Answer Column area
            pt1 = np.float32(loopContour)
            pt2 = np.float32([[0,0],[widthImg, 0], [0, heightImg], [widthImg, heightImg]])
            matrix = cv2.getPerspectiveTransform(pt1, pt2)
            imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg)) #Bird View Perspective.

            ## Grade area
            # ptG1 = np.float32(gradePoints)
            # ptG2 = np.float32([[0,0],[325, 0], [0, 150], [325, 150]]) # 325 (widthImg) 150 (heightImg) [Change accordingly]
            # matrixG = cv2.getPerspectiveTransform(ptG1, ptG2)
            # imgGradeDisplay = cv2.warpPerspective(img, matrixG, (325, 150)) #Bird View Perspective for Grade.
            # # cv2.imshow("Grade", imgGradeDisplay)

            ## Apply answer threshold
            imgWarpGray = cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2GRAY)
            imgThresh = cv2.threshold(imgWarpGray, 130, 255, cv2.THRESH_BINARY_INV)[1]

            boxes = utils.splitBoxes(imgThresh, choices)
            # cv2.imshow("Test", boxes[1]) #Edge
            # print(cv2.countNonZero(boxes[1]), cv2.countNonZero(boxes[2]))

            ## Decide choices minmax value pixels | Getting no zero pixel value of each box
            myPixelval = np.zeros((questions, choices))
            countC = 0 #Count Columns
            countR = 0 #Count Rows

            for image in boxes:
                totalPixels = cv2.countNonZero(image)
                myPixelval[countR][countC] = totalPixels
                countC += 1
                if (countC == choices):
                    countR += 1 ; countC=0
            # print(myPixelval)


            ## See biggest pixel value and get array(choice) value | Finding Index values of the markings
            myIndex = []
            for x in range (0, 5):
                arr = myPixelval[x]
                # print("arr", arr)
                myIndexVal = np.where(arr==np.amax(arr))
                # print(myIndexVal[0])
                myIndex.append(myIndexVal[0][0])
            # print("This is my Index: ", myIndex)

            # letter_to_number = {
            #     'A': 0,
            #     'B': 1,
            #     'C': 2,
            #     'D': 3,
            #     'E': 4
            #     }
            
            ## GRADING (RIGHT/WRONG)
            grading = []
            for x in range (0, 5):
                if numeric_answers[x + o * 5] == myIndex[x]:
                    grading.append(1)
                else:
                    grading.append(0)
            # print("This is grading: ", grading) #prints grading where if the answer and the choice is correct then change to 1. Wrong = 0

            # Accumulate the results
            all_myIndex.extend(myIndex)
            all_grading.extend(grading)

            # score = (sum(grading)/questions)*100 ## FINAL SCORE
            # print(score)

            # imgBlank = np.zeros_like(img) #Decoy Image for imgArray

            # Put into Image Array
            imgArray = ([img, imgGray, imgBlur, imgCanny],
                        [imgContours, imgBiggestContours, imgWarpColored, imgThresh])

            imgStacked = utils.stackImages(imgArray, 0.5)


            ### SHOW
            cv2.imshow("Stacked Images",imgStacked)
            cv2.waitKey(0)

            # return myIndex, grading, score

        # Combine results
        print("All myIndex: ", all_myIndex)
        print("All grading: ", all_grading)
        score = (sum(all_grading) / questions) * 100  # FINAL SCORE
        print(score)

        return all_myIndex, all_grading, score
        
    return None, None, None

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

    # questions = 5
    # choices = 5
    # answers = "B B B B B"

    args = parser.parse_args()

    ## RUN MAIN
    main(args.path, 
         args.questions,
         args.choices, 
         args.answers
         )