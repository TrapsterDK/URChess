from camera import Camera
import time
from skimage.metrics import structural_similarity
import cv2
import numpy as np
import matplotlib.pyplot as plt

def compare_images(before, after):
    #Greyscale stuff
    before = cv2.cvtColor(before, cv2.COLOR_BGR2GRAY)
    after = cv2.cvtColor(after, cv2.COLOR_BGR2GRAY)

    #blur stuff
    #before = cv2.GaussianBlur(before, (5, 5), 0)
    #after = cv2.GaussianBlur(after, (5, 5), 0)
    #before = cv2.GaussianBlur(before, (5, 5), 0)
    #after = cv2.GaussianBlur(after, (5, 5), 0)

    #SSIM stuff
    (score, diff) = structural_similarity(before, after, full=True)
    #print("Image Similarity: {:.4f}%".format(score * 100))


    diff = (diff * 255).astype("uint8")
    diff_box = cv2.merge([diff, diff, diff])

    thresh = cv2.threshold(diff, 120, 255, cv2.THRESH_BINARY_INV)[1]
    #print ("Threshold: {}".format(thresh))
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    mask = np.zeros(before.shape, dtype='uint8')
    filled_after = after.copy()
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    #areas = [cv2.contourArea(c) for c in contours]
    #print(areas)
    out = "fail", [(0,0), (0,0), (0,0), (0,0)]
    if len(contours) > 1:
        if cv2.contourArea(contours[0])*0.3 < cv2.contourArea(contours[1]) < cv2.contourArea(contours[0])*1.8 and cv2.contourArea(contours[0]) > 300:
            x,y,w,h = cv2.boundingRect(contours[0])
            x_2,y_2,w_2,h_2 = cv2.boundingRect(contours[1])
            cx_1 = x + w//2
            cy_1 = y + h//2
            cx_2 = x_2 + w_2//2
            cy_2 = y_2 + h_2//2
            out =  "two pieces", [(cx_1, cy_1), (cx_2, cy_2), (0,0), (0,0)]
            if len(contours) > 3 and cv2.contourArea(contours[2])*0.3 < cv2.contourArea(contours[3]) < cv2.contourArea(contours[2])*1.8 and cv2.contourArea(contours[2]) > 300:
                x,y,w,h = cv2.boundingRect(contours[2])
                x_2,y_2,w_2,h_2 = cv2.boundingRect(contours[3])
                cx_3 = x + w//2
                cy_3 = y + h//2
                cx_4 = x_2 + w_2//2
                cy_4 = y_2 + h_2//2
                out =  "four pieces", [(cx_1, cy_1), (cx_2, cy_2), (cx_3, cy_3), (cx_4, cy_4)]
        #one piece
        elif cv2.contourArea(contours[0]) > 300 and cv2.contourArea(contours[1]) < 300:
            x,y,w,h = cv2.boundingRect(contours[0])
            cx = x + w//2
            cy = y + h//2
            out =  "one piece", [(cx, cy), (0,0), (0,0), (0,0)]
        # four pieces
        else:
            out =  "fail", [(0,0), (0,0), (0,0), (0,0)]
    
    for c in contours:
        area = cv2.contourArea(c)
        if area > 300:
            x,y,w,h = cv2.boundingRect(c)
            cv2.rectangle(before, (x, y), (x + w, y + h), (36,255,12), 2)
            cv2.rectangle(after, (x, y), (x + w, y + h), (36,255,12), 2)
            cv2.rectangle(diff_box, (x, y), (x + w, y + h), (36,255,12), 2)
            cv2.drawContours(mask, [c], 0, (100,100,100), -1)
            cv2.drawContours(filled_after, [c], 0, (0,255,0), -1)

            #cv2.rectangle(mask, (cx-2, cy-2), (cx+2, cy+2), (255,255,255), 2)
            #cv2.rectangle(diff_box, (cx-2, cy-2), (cx+2, cy+2), (255,255,255), 2)
            #cv2.rectangle(before, (cx-2, cy-2), (cx+2, cy+2), (255,255,255), 2)
            #cv2.rectangle(after, (cx-2, cy-2), (cx+2, cy+2), (255,255,255), 2)
    for i in range (len(out[1])):
        cv2.rectangle(mask, (out[1][i][0]-2, out[1][i][1]-2), (out[1][i][0]+2, out[1][i][1]+2), (255,255,255), 2)
    return out[0], out[1], mask

def find_move(cam):
    #take a picture
    ret, before = cam.get_frame()
    cam.save_frame("zero_frame.png")
    succes_count = 0
    fail_count = 0
    count = 0
    save_coor = [(0,0), (0,0), (0,0), (0,0)]
    while True:
                
        ret, after = cam.get_frame()
        out, coordinates, mask = compare_images(before, after)
        #cv2.imshow("mask", mask)
        #cv2.imshow("before", before)
        #cv2.imshow("after", after)
        #cv2.waitKey(200)
        count += 1
        if count > 10:
            if succes_count != 0 and fail_count < succes_count and fail_count/ succes_count < 0.2 and out != "fail":
                #cv2.destroyAllWindows()
                return out, save_coor
                ret, before = cam.get_frame()
                count = 0
                succes_count = 0
                fail_count = 0
            else:
                #print("mega fail")
                count = 0
                fail_count = 0
        if out == "two pieces":
            #print("succes")
            if save_coor[0][0]*0.9 < coordinates[0][0] < save_coor[0][0]*1.1 and save_coor[0][1]*0.9 < coordinates[0][1] < save_coor[0][1]*1.1 and save_coor[1][0]*0.9 < coordinates[1][0] < save_coor[1][0]*1.1 and save_coor[1][1]*0.9 < coordinates[1][1] < save_coor[1][1]*1.1:
                succes_count += 1
            else:
                #print("koor fail")
                save_coor = coordinates
                succes_count = 0
        if out == "one piece":
            if save_coor[0][0]*0.9 < coordinates[0][0] < save_coor[0][0]*1.1 and save_coor[0][1]*0.9 < coordinates[0][1] < save_coor[0][1]*1.1:
                succes_count += 1
            else:
                #print("koor fail")
                save_coor = coordinates
                succes_count = 0
        if out == "four pieces":
            if save_coor[0][0]*0.9 < coordinates[0][0] < save_coor[0][0]*1.1 and save_coor[0][1]*0.9 < coordinates[0][1] < save_coor[0][1]*1.1 and save_coor[1][0]*0.9 < coordinates[1][0] < save_coor[1][0]*1.1 and save_coor[1][1]*0.9 < coordinates[1][1] < save_coor[1][1]*1.1 and save_coor[2][0]*0.9 < coordinates[2][0] < save_coor[2][0]*1.1 and save_coor[2][1]*0.9 < coordinates[2][1] < save_coor[2][1]*1.1 and save_coor[3][0]*0.9 < coordinates[3][0] < save_coor[3][0]*1.1 and save_coor[3][1]*0.9 < coordinates[3][1] < save_coor[3][1]*1.1:
                succes_count += 1
            else:
                #print("koor fail")
                save_coor = coordinates
                succes_count = 0
        if out == "fail":
            #print("fail from compare_images")
            fail_count += 1



        
            



