import numpy as np
import cv2
from camera import Camera, FakeCamera

qualityLevel = 0.01
minDistance = 10

if __name__ == '__main__':
    camera = FakeCamera("test.jpg")
    
    while True:
        camera.save_frame("test.jpg")
        ret, frame = camera.get_frame()
        empty = np.zeros_like(frame)

        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        maxCorners = 90

        corners = cv2.goodFeaturesToTrack(blur, maxCorners=maxCorners, qualityLevel=0.18, minDistance=12)
        corners = np.int0(corners)

        # sort corners by x + y to get closest to top left
        corners = sorted(corners, key=lambda x: x[0][0] + x[0][1])

        len_corners = len(corners)
        corner_lines_a = np.zeros((len_corners, len_corners), dtype=np.float32)
        corner_lines_b = np.zeros((len_corners, len_corners), dtype=np.float32)

        for i in range(len_corners):
            for j in range(len_corners):
                if i != j:
                    x1, y1 = corners[i][0]
                    x2, y2 = corners[j][0]
                    corner_lines_a[i][j] = (y2 - y1) / (x2 - x1)
                    corner_lines_b[i][j] = y1 - corner_lines_a[i][j] * x1

        print(corner_lines_a[0])
        print(corner_lines_b[0])

        #for a, b in zip(corner_lines_a[12], corner_lines_b[12]):
        #    cv2.line(empty, (0, int(b)), (1000, int(a * 1000 + b)), (0, 255, 0), 1)
            
        #for a, b in zip(corner_lines_a[15], corner_lines_b[15]):
        #    cv2.line(empty, (0, int(b)), (1000, int(a * 1000 + b)), (0, 0, 255), 1)

        lines = []
        

        for i in range(len_corners):
            for j in range(len_corners):
                if i == j:
                    continue

                a, b = corner_lines_a[i][j], corner_lines_b[i][j]

                on_line = 0
                for k in range(len_corners):
                    if i == k or j == k:
                        continue

                    a2, b2 = corner_lines_a[i][k], corner_lines_b[i][k]

                    if abs((100 * a + b) - (100*a2+b2)) < 5:
                        on_line += 1
                
                if on_line > 5:
                    lines.append((i, j))

        for i in lines:
            cv2.line(empty, tuple(corners[i[0]][0]), tuple(corners[i[1]][0]), (0, 255, 0), 2)

        for i in corners:
            x, y = i.ravel()
            cv2.circle(empty, (x, y), 3, 255, -1)

        cv2.imshow('frame', empty)

        key = cv2.waitKey(1)

        if key & 0xFF == ord('q'):
            break
