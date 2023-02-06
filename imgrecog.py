import numpy as np
import cv2
from camera import Camera, FakeCamera
from prettytable import PrettyTable
import matplotlib.pyplot as plt

qualityLevel = 0.01
minDistance = 10

def lin_equ(l1, l2):
    m = ((l2[1] - l1[1])) / (l2[0] - l1[0])
    c = (l2[1] - (m * l2[0]))
    return m, c

def image_remove_shadow(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv[:,:,2] = cv2.equalizeHist(hsv[:,:,2])
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

def image_addaptive_guassian_threshold(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    return cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

def image_addaptive_mean_threshold(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    return cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

def image_otsu_threshold(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    return cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

def gray_to_bgr(img):
    return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

if __name__ == '__main__':
    camera = FakeCamera("test2.jpeg", width=400, height=400)

    while True:
        ret, frame = camera.get_frame()
        empty = frame

        otsu = gray_to_bgr(image_otsu_threshold(frame))

        for img in [frame, otsu]:
            # find Harris corners
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (5, 5), 0)
            dst = cv2.cornerHarris(gray, 2, 3, 0.04)
            #result is dilated for marking the corners, not important
            dst = cv2.dilate(dst, None)
            # Threshold for an optimal value, it may vary depending on the image.
            img[dst > 0.01 * dst.max()] = [0, 0, 255]


        # show the images 2 by 2 in same window
        cv2.imshow('frame', np.hstack((frame, otsu)))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break



    if False:
        while True:
            ret, frame = camera.get_frame()
            empty = frame

            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            gray[128 < gray] = [255]
            gray[gray < 128] = [0]

            blur = cv2.GaussianBlur(gray, (5, 5), 0)

            maxCorners = 90

            # image increase contrast
            #clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            #blur = clahe.apply(blur)

            #dst = cv2.cornerHarris(blur, 2, 3, 0.04)
            #dst = cv2.dilate(dst, None)
            #empty[dst > 0.01 * dst.max()] = [0, 0, 255]

            corners = cv2.goodFeaturesToTrack(blur, maxCorners=maxCorners, qualityLevel=0.18, minDistance=12)
            corners = np.intp(corners)

            # sort corners by x + y to get closest to top left
            #corners = sorted(corners, key=lambda x: x[0][0] + x[0][1])

            
            for i in corners:
                x, y = i.ravel()
                cv2.circle(empty, (x, y), 3, 255, -1)
            
            cv2.imshow('frame', gray)

            '''
            len_corners = len(corners)
            corner_lines_a = np.zeros((len_corners, len_corners), dtype=np.float32)
            corner_lines_b = np.zeros((len_corners, len_corners), dtype=np.float32)

            for i in range(len_corners):
                for j in range(len_corners):
                    if i != j:
                        corner_lines_a[i][j], corner_lines_b[i][j] = lin_equ(corners[i][0], corners[j][0])

            for line in [corner_lines_a, corner_lines_b]:
                table = PrettyTable()
                for i in range(len_corners):
                    table.add_column(str(i), ([0] * i) + [round(it, 2) for it in list(line[i][i:len_corners])])
                print(table)
        
            lines = []

            for i in range(len_corners):
                for j in range(i, len_corners):
                    if i == j:
                        continue
            '''

            
            # create matplot graph using the algebraic equations of the lines
            '''
            x = np.linspace(0, 1000, 1000)
            for i in range(len_corners):
                for j in range(len_corners):
                    if i != j:
                        plt.plot(x, corner_lines_a[i][j] * x + corner_lines_b[i][j], color='black', linewidth=0.5)
            '''

            '''
            for a_line, b_line in zip(corner_lines_a, corner_lines_b):
                for i in range(len_corners):
                    for j in range(len_corners):
                        x = 0
                        plt.plot(x, a_line[i] * x + b_line[i], color='black', linewidth=2)
            plt.show()
            '''



            '''
            for i in lines:
                cv2.line(empty, tuple(corners[i[0]][0]), tuple(corners[i[1]][0]), (0, 255, 0), 2)

            for i in corners:
                x, y = i.ravel()
                cv2.circle(empty, (x, y), 3, 255, -1)

            # multiply size of image by 4
            empty = cv2.resize(empty, (empty.shape[1] * 4, empty.shape[0] * 4))
            '''

            key = cv2.waitKey(1)

            if key & 0xFF == ord('q'):
                break
