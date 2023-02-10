from camera import Camera
import time
from skimage.metrics import structural_similarity
import cv2
import numpy as np

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

    for c in contours:
        area = cv2.contourArea(c)
        if area > 40:
            x,y,w,h = cv2.boundingRect(c)
            print(x,y)
            cv2.rectangle(before, (x, y), (x + w, y + h), (36,255,12), 2)
            cv2.rectangle(after, (x, y), (x + w, y + h), (36,255,12), 2)
            cv2.rectangle(diff_box, (x, y), (x + w, y + h), (36,255,12), 2)
            cv2.drawContours(mask, [c], 0, (255,255,255), -1)
            cv2.drawContours(filled_after, [c], 0, (0,255,0), -1)
    
    cv2.imshow('before', before)
    cv2.imshow('after', after)
    cv2.imshow('diff_box', diff_box)
    cv2.imshow('mask', mask)
    cv2.imshow('filled_after', filled_after)
    cv2.waitKey(0)
    
    return mask
while True:
    cam = Camera()
    ret, before = cam.get_frame()
    time.sleep(3)
    ret, after = cam.get_frame()
    mask = compare_images(before, after)
    cv2.imshow("Da_mask!", mask)
    cv2.waitKey(0)
