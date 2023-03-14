import cv2
import numpy as np
import math
from camera import FakeCamera, Camera

#helper functions

def draw_rects_with_index(img, rects):
    for i, rect in enumerate(rects):
        cv2.polylines(img, [np.array(rect, dtype=np.int32)], True, (0, 255, 0), 2)
        cv2.putText(img, str(i), (rect[0][0], rect[0][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

def draw_lines(img, lines, color=(0, 0, 255), thickness=2):
    for line in lines:
        rho, theta = line
        a = math.cos(theta)
        b = math.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))

        cv2.line(img, (x1, y1), (x2, y2), color, thickness)

def show_lines_split(img, lines_1, lines_2, common_angle=None):
    new_img = img.copy()
    if common_angle is not None:
        draw_common_angle(new_img, common_angle)
    draw_lines(new_img, lines_1, (0, 255, 0))
    draw_lines(new_img, lines_2, (0, 0, 255))
    cv2.imshow("lines", new_img)
    cv2.waitKey(0)

def draw_line_at_angle(img, angle_degrees):
    # draw line at angle from center of image all 4 directions
    center = (img.shape[1]//2, img.shape[0]//2)
    cv2.line(img, center, (center[0] + int(1000*math.cos(math.radians(angle_degrees))), center[1] + int(1000*math.sin(math.radians(angle_degrees)))), (255, 0, 0), 2)

def draw_common_angle(img, angle_degrees):
    # draw line at angle from center of image all 4 directions
    center = (img.shape[1]//2, img.shape[0]//2)
    for i in range(4):
        angle_degrees += 90
        cv2.line(img, center, (center[0] + int(1000*math.cos(math.radians(angle_degrees))), center[1] + int(1000*math.sin(math.radians(angle_degrees)))), (255, 0, 0), 2)

# actual functions

def canny_edges(gray_img):
    return cv2.Canny(gray_img, 40, 255)

def hough_lines(canny_img):
    lines = cv2.HoughLines(canny_img, 1, math.pi/180.0, 100, np.array([]), 0, 0)
    if lines is None:
        return None
    return [line[0] for line in lines]

def get_hough_line_degree_angles(lines):
    return [math.degrees(math.atan2(math.sin(line[1]), math.cos(line[1]))) for line in lines]

def get_most_common_angle_90_degrees(angles, angle_threshold = 5):
    angles = sorted([angle % 90 for angle in angles])

    # get range including the most angles
    # the range is any angle +- the threshold
    # the angle does not have to be in the list
    lower_angle = angles[0]
    upper_angle = angles[-1]
    max_count = 0
    for i, a in enumerate(angles):
        count = 0
        for j in range(i, i + len(angles)):
            add = j//len(angles) * 90
            if angles[j % len(angles)] + add - a > angle_threshold*2:
                break

            upper_angle = angles[j % len(angles)] + add
            count = j - i + 1

        if count > max_count:
            max_count = count
            lower_angle = a
        
        if count == len(angles):
            break

    return  90 - (lower_angle + upper_angle) / 2 % 90

def split_lines_orthogonal(lines, angle):
    # split lines into two groups
    # one group is orthogonal almost orthogonal to the angle +- 45 degrees
    orthogonal = []
    other = []
    for line in lines:
        if 45-angle < math.degrees(math.atan2(math.sin(line[1]), math.cos(line[1]))) < 135-angle:
            orthogonal.append(line)
        else:
            other.append(line)

    return orthogonal, other

# find intersections between lines
def intersection(line1, line2, img_shape):
    rho1, theta1 = line1
    rho2, theta2 = line2
    A = np.array([
        [math.cos(theta1), math.sin(theta1)],
        [math.cos(theta2), math.sin(theta2)]
    ])
    b = np.array([[rho1], [rho2]])
    try:
        x0, y0 = np.linalg.solve(A, b)
        x0, y0 = int(x0), int(y0)
        if x0 < 0 or x0 >= img_shape[1] or y0 < 0 or y0 >= img_shape[0]:
            return None
        return (x0, y0)
    except np.linalg.LinAlgError:
        return None
    
def get_closer_line_angle(line1, line2, common_angle):
    angle1 = abs(90 - (math.degrees(math.atan2(math.sin(line1[1]), math.cos(line1[1]))) % 90))
    angle2 = abs(90 - (math.degrees(math.atan2(math.sin(line2[1]), math.cos(line2[1]))) % 90))

    if angle1 == angle2:
        return 0
    
    return 0 if abs(angle1 - common_angle) < abs(angle2 - common_angle) else 1

def remove_intersecting_lines(lines, img_shape, common_angle):
    # remove lines that are intersecting with other lines within the image shape
    new_lines = [lines[0]]
    for line in lines:
        for i, new_line in enumerate(new_lines):
            intersection_point = intersection(line, new_line, img_shape)
            if intersection_point is not None:
                # check which line is closer to the common angle
                # if the line is closer to the common angle, remove the other line
                # if the line is not closer to the common angle, remove the line
                new_lines[i] = new_line if get_closer_line_angle(line, new_line, common_angle) else line

                # check it does not intersect with any other lines
                for j, check_line in enumerate(new_lines):
                    if j == i:
                        continue

                    if intersection(check_line, new_lines[i], img_shape) is not None:
                        if get_closer_line_angle(check_line, new_lines[i], common_angle):
                            del new_lines[j]
                        else:
                            del new_lines[i]
                            
                break
        else:
            new_lines.append(line)

    return new_lines

def remove_close_lines(lines, threshold = 10):
    # remove lines that are close to each other
    new_lines = [lines[0]]
    for line in lines:
        rho = line[0]
        for new_line in new_lines:
            if abs(new_line[0] - rho) < threshold:
                break
        else:
            new_lines.append(line)
                
    return new_lines

def lines_equal_distance_both_ways(sorted_lines, threshold = 15):
    new_lines_indexes = []
    for i, (line_before, line, line_after) in enumerate(zip(sorted_lines, sorted_lines[1:], sorted_lines[2:])):
        line_before_rho, line_rho, line_after_rho = line_before[0], line[0], line_after[0]

        diff1 = abs(line_before_rho - line_rho)
        diff2 = abs(line_after_rho - line_rho)

        if abs(diff1 - diff2) > threshold:
            continue

        new_lines_indexes.append(i+1)

    return new_lines_indexes

def count_from_index(list_of_numbers, index, reverse = False):
    count = 1
    index_number = list_of_numbers[index]
    multiplier = -1 if reverse else 1
    for next_number in list_of_numbers[index+1:] if not reverse else list_of_numbers[index-1::-1]:
        if next_number != index_number + count * multiplier:
            break
        count += 1

    return count

def longest_count(list_of_numbers):
    # return the longest count of consecutive numbers starting from any number index and length
    # if there are multiple longest counts, return the first one
    longest_count = 0
    longest_count_index = 0
    for i in range(len(list_of_numbers)):
        count = count_from_index(list_of_numbers, i)
        if count > longest_count:
            longest_count = count
            longest_count_index = i

    return longest_count_index, longest_count

def get_chessboard_lines(sorted_lines, lines_indexes):
    first_index, count  = longest_count(lines_indexes)

    if count != 7:
        correct_index = None

        # max one space before and after

        if first_index - 1 < 0:
            before = count_from_index(lines_indexes, first_index - 1, reverse=True)
            if before + count + 1 == 7:
                correct_index == first_index - before - 1


        if first_index + count > len(lines_indexes):
            after = count_from_index(lines_indexes, first_index + count, reverse=False)
            if after + count + 1 == 7:
                # both options are valid choices so unable to determine
                if correct_index is not None:
                    return None
                # set to show that the after option is valid
                correct_index = first_index

        if correct_index is None:
            return None
        
        first_index = correct_index
        
    return sorted_lines[lines_indexes[first_index]-1:lines_indexes[first_index] + 8]

def find_intersections(lines_direction_1, lines_direction_2, img_shape):
    intersections = []
    for line1 in lines_direction_1:
        for line2 in lines_direction_2:
            intersection_point = intersection(line1, line2, img_shape)
            if intersection_point is not None:
                intersections.append(np.array(intersection_point, dtype=np.int32))
    return intersections

def chessboard_points_to_rectangles(points):
    rectangles = []
    for i in range(8):
        for j in range(8):
            rectangles.append([points[i*9 + j], points[i*9 + j + 1], points[(i+1)*9 + j + 1], points[(i+1)*9 + j]])

    return rectangles

def find_chess_board_rects(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = canny_edges(blur)

    lines = hough_lines(canny)
    if lines is None:
        return None
        raise Exception("No lines found")

    angles = get_hough_line_degree_angles(lines)
    common_angle = get_most_common_angle_90_degrees(angles)
    lines_1, lines_2 = split_lines_orthogonal(lines, common_angle)
    
    if len(lines_1) < 10 or len(lines_2) < 10:
        return None
        raise Exception("Not enough lines found")

    lines_1 = remove_intersecting_lines(lines_1, img.shape, common_angle)
    lines_2 = remove_intersecting_lines(lines_2, img.shape, common_angle)

    if len(lines_1) < 10 or len(lines_2) < 10:
        return None
        raise Exception("Not enough lines found")

    lines_1 = remove_close_lines(lines_1)
    lines_2 = remove_close_lines(lines_2)

    if len(lines_1) < 10 or len(lines_2) < 10:
        return None
        raise Exception("Not enough lines found")
    
    lines_1 = sorted(lines_1, key = lambda line: line[0])
    lines_2 = sorted(lines_2, key = lambda line: line[0])

    lines_1_indexes = lines_equal_distance_both_ways(lines_1)
    lines_2_indexes = lines_equal_distance_both_ways(lines_2)

    chessboard_lines_1 = get_chessboard_lines(lines_1, lines_1_indexes)
    if chessboard_lines_1 is None:
        return None
        raise Exception("Chessboard board lines not found 1")
    
    chessboard_lines_2 = get_chessboard_lines(lines_2, lines_2_indexes)

    if chessboard_lines_2 is None:
        return None
        raise Exception("Chessboard board lines not found 2")

    intersections = find_intersections(chessboard_lines_1, chessboard_lines_2, img.shape)

    if len(intersections) != 81:
        return None
        raise Exception("Chessboard not found")

    rectangles = chessboard_points_to_rectangles(intersections)

    return rectangles

#https://math.stackexchange.com/questions/190111/how-to-check-if-a-point-is-inside-a-rectangle
def point_in_rectangle(point, rectangle):
    M = point
    A = rectangle[0]
    B = rectangle[1]
    C = rectangle[2]
    D = rectangle[3]

    return (
            (0 < np.dot(M-A, B-A) < np.dot(B-A, B-A) 
        and  0 < np.dot(M-A, D-A) < np.dot(D-A, D-A)) 
        or  (0 < np.dot(M-C, B-C) < np.dot(B-C, B-C) 
        and  0 < np.dot(M-C, D-C) < np.dot(D-C, D-C)))

def get_square_with_point(point, rectangles):
    for i, rectangle in enumerate(rectangles):
        if point_in_rectangle(point, rectangle):
            return i
        
    return None

def square_to_chessboard_square(square):
    x = square % 8
    y = square // 8
    return f"{'abcdefgh'[7-x]}{8-y}"

def chessboard_to_square(chessboard_square):
    x = "abcdefgh".index(chessboard_square[0])
    y = 8 - int(chessboard_square[1])
    return y * 8 + x

def square_to_xy(square):
    x = square % 8
    y = square // 8
    return x+1, y+1

'''
print(square_to_chessboard_square(0))
print(square_to_chessboard_square(1))
print(square_to_chessboard_square(2))
print(square_to_chessboard_square(3))
print(square_to_chessboard_square(4))
print(square_to_chessboard_square(5))
print(square_to_chessboard_square(6))
print(square_to_chessboard_square(7))
print(square_to_chessboard_square(8))
print(square_to_chessboard_square(63))
'''

from scipy import ndimage

# show rotation detection
if __name__ == "__main__":
    img = FakeCamera("images/up_1.png").get_frame()[1]

    rotation = 0

    while True:
        imgr = ndimage.rotate(img, rotation, reshape=True)
        rectangles = find_chess_board_rects(imgr)
        if rectangles:
            draw_rects_with_index(imgr, rectangles)
            cv2.imshow("img", imgr)
        else:
            cv2.imshow("img", imgr)
        
        key = cv2.waitKey(0)

        if key == ord('q'):
            break

        if key == ord('a'):
            rotation += 5

        if key == ord('d'):
            rotation -= 5

'''
if __name__ == "__main__":
    camera = Camera(0)

    while True:
        img = camera.get_frame()[1]
        try:
            rectangles = find_chess_board_rects(img)
            draw_rects_with_index(img, rectangles)
        except Exception as e:
            print(e)
            pass
        cv2.imshow("img", img)
        if cv2.waitKey(1) == ord('q'):
            break
'''