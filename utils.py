import cv2
import numpy as np

## TO STACK ALL THE IMAGES IN ONE WINDOW
def stackImages(imgArray,scale,lables=[]):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
            hor_con[x] = np.concatenate(imgArray[x])
        ver = np.vstack(hor)
        ver_con = np.concatenate(hor)
    else:
        for x in range(0, rows):
            imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        hor_con= np.concatenate(imgArray)
        ver = hor
    if len(lables) != 0:
        eachImgWidth= int(ver.shape[1] / cols)
        eachImgHeight = int(ver.shape[0] / rows)
        #print(eachImgHeight)
        for d in range(0, rows):
            for c in range (0,cols):
                cv2.rectangle(ver,(c*eachImgWidth,eachImgHeight*d),(c*eachImgWidth+len(lables[d][c])*13+27,30+eachImgHeight*d),(255,255,255),cv2.FILLED)
                cv2.putText(ver,lables[d][c],(eachImgWidth*c+10,eachImgHeight*d+20),cv2.FONT_HERSHEY_COMPLEX,0.7,(255,0,255),2)
    return ver

def reorder(myPoints): #ORIGINAL

    myPoints = myPoints.reshape((4, 2)) # REMOVE EXTRA BRACKET
    # print(myPoints)
    myPointsNew = np.zeros((4, 1, 2), np.int32) # NEW MATRIX WITH ARRANGED POINTS
    add = myPoints.sum(1)
    # print(add)
    # print(np.argmax(add))
    myPointsNew[0] = myPoints[np.argmin(add)]  #[0,0]
    myPointsNew[3] =myPoints[np.argmax(add)]   #[w,h]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] =myPoints[np.argmin(diff)]  #[w,0]
    myPointsNew[2] = myPoints[np.argmax(diff)] #[h,0]
    # print(diff)

    return myPointsNew

def reorder(myPoints):
    # Ensure the contour has exactly 4 points
    if len(myPoints) != 4:
        return myPoints  # Return the original contour if it doesn't have 4 points

    myPoints = myPoints.reshape((4, 2))  # REMOVE EXTRA BRACKET
    myPointsNew = np.zeros((4, 1, 2), np.int32)  # NEW MATRIX WITH ARRANGED POINTS
    add = myPoints.sum(1)
    myPointsNew[0] = myPoints[np.argmin(add)]  # [0,0]
    myPointsNew[3] = myPoints[np.argmax(add)]  # [w,h]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] = myPoints[np.argmin(diff)]  # [w,0]
    myPointsNew[2] = myPoints[np.argmax(diff)]  # [h,0]

    return myPointsNew

def sort_contours(contour_points, questions_per_column=5):
    # Get bounding rectangles for each contour
    bounding_rects = [cv2.boundingRect(pts) for pts in contour_points]

    # Sort the bounding rectangles by x-coordinate first to divide into columns
    contour_points_sorted_by_x = sorted(zip(bounding_rects, contour_points), key=lambda b: b[0][0])

    # Divide the sorted contours into columns
    columns = []
    current_column = []
    current_x = contour_points_sorted_by_x[0][0][0]
    for rect, pts in contour_points_sorted_by_x:
        x = rect[0]
        if x - current_x < 100:  # Assuming a small threshold to determine columns, adjust as needed
            current_column.append((rect, pts))
        else:
            columns.append(current_column)
            current_column = [(rect, pts)]
            current_x = x
    if current_column:
        columns.append(current_column)

    # Sort each column by y-coordinate and then combine
    sorted_contours = []
    for column in columns:
        column_sorted_by_y = sorted(column, key=lambda b: b[0][1])
        sorted_contours.extend([pts for _, pts in column_sorted_by_y])

    # Only keep the top `questions_per_column` sorted contours
    sorted_contours = sorted_contours[:questions_per_column]

    return sorted_contours


# def sort_contours(contours, num_contours=None, tolerance = 5):
#     # contours = [
#     # [[[441, 468]], [[441, 623]], [[640, 622]], [[639, 467]]],  # 3th answer box (Blue) | Biggest Contour [in blue] kiri atas | kiri bawah | kanan bawah | kanan atas |
#     # [[[441, 139]], [[441, 294]], [[640, 293]], [[639, 138]]],  # 1st answer box (Green) | 2nd biggest contour [in green] |
#     # [[[441, 797]], [[441, 952]], [[640, 951]], [[638, 796]]],  # 5th answer box (Red) | 3rd biggest contour [in red] |
#     # [[[441, 304]], [[442, 459]], [[640, 458]], [[639, 303]]],  # 2nd answer box (Gray) | 4th biggest contour [in gray] |
#     # [[[441, 633]], [[442, 788]], [[640, 787]], [[639, 632]]],  # 4th answer box (Blue ish gray) | 5th biggest contour [in blue-ish gray] |
#     # [[[722, 138]], [[722, 294]], [[919, 294]], [[919, 138]]],  # 6nd answer box (Blue ish gray) | 6th biggest contour [in blue-ish gray] | 
#     # [[[722, 467]], [[722, 623]], [[919, 623]], [[918, 467]]],  # 8th answer box (Gray) | 7th biggest contour [in gray] |
#     # [[[721, 633]], [[722, 788]], [[919, 788]], [[919, 632]]],  # 9th answer box (Yellow) | 8th biggest contour [in yellow] |
#     # [[[722, 303]], [[722, 459]], [[919, 459]], [[919, 303]]],  # 7th answer box (Pink) | 9th biggest contour [in pink] |
#     # [[[722, 797]], [[722, 952]], [[919, 952]], [[919, 797]]]   # 10th answer box (Purple) | 10th biggest contour [in purple] |
#     # ]

#     # Extract the first sub-array from each contour
#     first_sub_arrays = [contour[0][0] for contour in contours]

#     # Split the list into the first 5 elements and the last 5 elements
#     # first_half = first_sub_arrays[:5]
#     # second_half = first_sub_arrays[5:]

#     # Sort each half by the y-coordinate
#     # first_half_sorted = sorted(first_half, key=lambda point: point[0][1])
#     # second_half_sorted = sorted(second_half, key=lambda point: point[0][1])

#     def sorting_key(point):
#         x, y = point
#         # Apply tolerance to x-coordinate
#         x_adjusted = x // tolerance * tolerance
#         return (x_adjusted, y)
    
#     sorted_first_sub_arrays = sorted(first_sub_arrays, key=sorting_key
#                             #  lambda point: (point[0] if len(point) > 0 else float('inf'), point[1] if len(point) > 1 else float('inf'))
#                              )
#     sorted_contours = []
#     for point in sorted_first_sub_arrays:
#         for contour in contours:
#             if np.array_equal(contour[0][0], point):
#                 sorted_contours.append(contour)
#                 break

#     # print("This is sorted_contours: ", sorted_contours)

#     # Combine the sorted halves
#     # sorted_first_sub_arrays = first_half_sorted + second_half_sorted

#     if num_contours is None:
#         return sorted_contours
#     else:
#         return sorted_contours[:num_contours]

#     # print("The sorted array of the first sub-arrays based on y-coordinate is:")
#     # print(sorted_first_sub_arrays)

#     # return sorted_first_sub_arrays

def rectContour(contours): #ORIGINAL
    #Finding outer edges
    rectCon = []
    max_area = 0
    for i in contours:
        area = cv2.contourArea(i)
        # print(area)
        if area > 50: #Area min
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            # print("Corner Points", len(approx))
            if len(approx) == 4:
                rectCon.append(i)
    rectCon = sorted(rectCon, key=cv2.contourArea,reverse=True)
    # print(len(rectCon))
    return rectCon

# def rectContour(contours):
#     rectCon = []
#     for i in contours:
#         area = cv2.contourArea(i)
#         if area > 50:  # Area min
#             peri = cv2.arcLength(i, True)
#             approx = cv2.approxPolyDP(i, 0.02 * peri, True)
#             if len(approx) == 4:  # Check if the contour has exactly 4 points
#                 rectCon.append(approx)  # Append the contour with 4 points
#     return rectCon

def getCornerPoints(cont):
    peri = cv2.arcLength(cont, True) # LENGTH OF CONTOUR
    approx = cv2.approxPolyDP(cont, 0.02 * peri, True) # APPROXIMATE THE POLY TO GET CORNER POINTS
    return approx

def splitBoxes(img, choices):
    rows = np.vsplit(img, 5) #Get A B C D E as one row
    boxes=[]
    for r in rows:
        cols= np.hsplit(r,choices)
        for box in cols:
            boxes.append(box)
            # cv2.imshow("Split", box)
    return boxes #Get Options A B C D E one by one

def drawGrid(img,questions=5,choices=5):
    secW = int(img.shape[1]/questions)
    secH = int(img.shape[0]/choices)
    for i in range (0,9):
        pt1 = (0,secH*i)
        pt2 = (img.shape[1],secH*i)
        pt3 = (secW * i, 0)
        pt4 = (secW*i,img.shape[0])
        cv2.line(img, pt1, pt2, (255, 255, 0),2)
        cv2.line(img, pt3, pt4, (255, 255, 0),2)

    return img

def showAnswers(img,myIndex,grading,ans,questions=5,choices=5):
     secW = int(img.shape[1]/questions)
     secH = int(img.shape[0]/choices)

     for x in range(0,questions):
         myAns= myIndex[x]
         cX = (myAns * secW) + secW // 2
         cY = (x * secH) + secH // 2
         if grading[x]==1:
            myColor = (0,255,0)
            #cv2.rectangle(img,(myAns*secW,x*secH),((myAns*secW)+secW,(x*secH)+secH),myColor,cv2.FILLED)
            cv2.circle(img,(cX,cY),50,myColor,cv2.FILLED)
         else:
            myColor = (0,0,255)
            #cv2.rectangle(img, (myAns * secW, x * secH), ((myAns * secW) + secW, (x * secH) + secH), myColor, cv2.FILLED)
            cv2.circle(img, (cX, cY), 50, myColor, cv2.FILLED)

            # CORRECT ANSWER
            myColor = (0, 255, 0)
            correctAns = ans[x]
            cv2.circle(img,((correctAns * secW)+secW//2, (x * secH)+secH//2),
            20,myColor,cv2.FILLED)



