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

def shadow_remove(img):
    rgb_planes = cv2.split(img)
    result_norm_planes = []
    for plane in rgb_planes:
        dilated_img = cv2.dilate(plane, np.ones((7,7), np.uint8))
        bg_img = cv2.medianBlur(dilated_img, 21)
        diff_img = 255 - cv2.absdiff(plane, bg_img)
        norm_img = cv2.normalize(diff_img,None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        result_norm_planes.append(norm_img)
    shadowremov = cv2.merge(result_norm_planes)
    return shadowremov

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
    camera = FakeCamera("test.jpg", width=400, height=400)

    vals_type = ["int", "int", "float", "float", "float", "float", "float", "float"]
    vals = [2, 3, 0.04, 0.01, 0, 0, 0, 0]

    while True:
        imgs = []
        camera = FakeCamera("test.jpg", width=400, height=400)
        camera2 = FakeCamera("test2.jpeg", width=400, height=400)
        for cam in [camera, camera2]:
            ret, frame = cam.get_frame()
            img = frame.copy()
            empty = frame

            # find Harris corners
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (5, 5), 0)
            dst = cv2.cornerHarris(gray, 2, 3, 0.02)
            #result is dilated for marking the corners, not important
            dst = cv2.dilate(dst, None)

            # find centroids
            ret, dst = cv2.threshold(dst, 0.01 * dst.max(), 255, 0)
            dst = np.uint8(dst)
            ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)

            # draw centroids
            #for i in range(1, len(centroids)):
            #    cv2.circle(img, (int(centroids[i][0]), int(centroids[i][1])), 1, (0, 0, 255), -1)

            # define the criteria to stop and refine the corners
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
            corners = cv2.cornerSubPix(gray, np.float32(centroids), (5, 5), (-1, -1), criteria)

            for i in range(1, len(corners)):
                cv2.circle(img, (int(corners[i][0]), int(corners[i][1])), 1, (0, 0, 255), -1)
            

            # show the images 2 by 2 in same window
            imgs.append(np.hstack((frame, img)))

        # show the images 2 by 2 in same window
        cv2.imshow("img", np.vstack(imgs))

        up = ["w", "e", "r", "t", "y", "u", "i", "o"]
        down = ["s", "d", "f", "g", "h", "j", "k", "l"]

        key = cv2.waitKey(1)

        if key in [ord(x) for x in up]:
            index = up.index(chr(key))
            if index == 1:
                vals[index] += 2
                vals[index] = min(31, vals[index])
            else:
                vals[index] += 1 if vals_type[index] == "int" else 0.01

        if key in [ord(x) for x in down]:
            index = down.index(chr(key))
            if index == 1:
                vals[index] -= 2
                vals[index] = max(1, vals[index])
            else:
                vals[index] -= 1 if vals_type[index] == "int" else 0.01
                vals[index] = max(0, vals[index])

        print(vals)

        if key & 0xFF == ord('q'):
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
