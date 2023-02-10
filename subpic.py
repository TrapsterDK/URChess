#This is a function that takes 2 pictures and compares them and returns the difference
import cv2
import numpy as np

def compare_images(imageA, imageB):
    diff = cv2.absdiff(imageA, imageB)
    
    #color
    ConvHsv_Gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(ConvHsv_Gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    diff[mask != 255] = [0, 0, 255]

    return mask