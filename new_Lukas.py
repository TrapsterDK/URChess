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
    print("Image Similarity: {:.4f}%".format(score * 100))


    diff = (diff * 255).astype("uint8")
    diff_box = cv2.merge([diff, diff, diff])

    thresh = cv2.threshold(diff, 100, 255, cv2.THRESH_BINARY_INV)[1]
    #print ("Threshold: {}".format(thresh))
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    mask = np.zeros(before.shape, dtype='uint8')
    filled_after = after.copy()
    big_area = []
    for k in contours:
        area = cv2.contourArea(k)
        big_area.append(area)
        #sort with biggest area first
        big_area.sort(reverse=True)
    if big_area[0]*0.8 < big_area[1] < big_area[0]*1.2:
        if big_area[1]*0.7 < big_area[2] < big_area[1]*1.3:
            if big_area[2]*0.8 < big_area[3] < big_area[2]*1.2:
                print("casttle")
        print("two pieces")
    print(big_area)

    for c in contours:
        area = cv2.contourArea(c)
        if area > 2000:
            x,y,w,h = cv2.boundingRect(c)
            cv2.rectangle(before, (x, y), (x + w, y + h), (36,255,12), 2)
            cv2.rectangle(after, (x, y), (x + w, y + h), (36,255,12), 2)
            cv2.rectangle(diff_box, (x, y), (x + w, y + h), (36,255,12), 2)
            cv2.drawContours(mask, [c], 0, (100,100,100), -1)
            cv2.drawContours(filled_after, [c], 0, (0,255,0), -1)
            cx = x + w//2
            cy = y + h//2
            cv2.rectangle(mask, (cx-2, cy-2), (cx+2, cy+2), (255,255,255), 2)
    
    return mask
#take a picture
cam = Camera()
ret, before = cam.get_frame()
cam.save_frame("zero_frame.png")
while True:
    user = input("Press enter to take a picture, or type 'q' to quit: ")
    if user == "q":
        break
    else:
        ret, after = cam.get_frame()
        cam.save_frame("frame.png")
        mask = compare_images(before, after)
        cv2.imshow("before", before)
        cv2.imshow("after", after)
        cv2.imshow("diff", mask)
        cv2.waitKey(0)




