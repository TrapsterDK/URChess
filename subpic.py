#This is a function that takes 2 pictures and compares them and returns the difference
import cv2
import numpy as np

def compare_images(imageA, imageB):
    diff = cv2.absdiff(imageA, imageB)
    
