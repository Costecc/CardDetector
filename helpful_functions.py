import cv2
import math
import numpy as np
import imutils
import statistics as st


def choose_corner(x, y, w, h):
    if w < h:
        return x, y
    else:
        return x + w, y


def get_center_point(card_corners):
    x = (card_corners[0, 0] + card_corners[1, 0] + card_corners[2, 0] + card_corners[3, 0]) / 4
    y = (card_corners[0, 1] + card_corners[1, 1] + card_corners[2, 1] + card_corners[3, 1]) / 4
    return x, y


def get_right_points_order(points):
    rightPoints = np.array([ [0, 0], [0 , 0], [0, 0], [0, 0]] , np.float32)

    max_x =  max(points[0][0], points[1][0], points[2][0], points[3][0])
    min_x =  min(points[0][0], points[1][0], points[2][0], points[3][0])
    estimated_width = max_x - min_x

    max_y = max(points[0][1], points[1][1], points[2][1], points[3][1])
    min_y = min(points[0][1], points[1][1], points[2][1], points[3][1])
    estimated_height = max_y - min_y

    # print("wymiarki:")
    # print(h)
    # print(w)
    mid = [0, 0]
    mid[0] = (points[0][0] + points[1][0] + points[2][0] + points[3][0]) / 4
    mid[1] = (points[0][1] + points[1][1] + points[2][1] + points[3][1]) / 4

    print(estimated_width)
    print(estimated_height)

    if estimated_width > estimated_height:
        for point in points:
            if point[0] > mid[0] and point[1] > mid[1]:
                rightPoints[0] = point
            elif point[0] < mid[0] and point[1] > mid[1]:
                rightPoints[1] = point
            elif point[0] < mid[0] and point[1] < mid[1]:
                rightPoints[2] = point
            elif point[0] > mid[0] and point[1] < mid[1]:
                rightPoints[3] = point
        return rightPoints, estimated_width, estimated_height
    else:
        for point in points:
            if point[0] > mid[0] and point[1] < mid[1]:
                rightPoints[0] = point
            elif point[0] > mid[0] and point[1] > mid[1]:
                rightPoints[1] = point
            elif point[0] < mid[0] and point[1] > mid[1]:
                rightPoints[2] = point
            elif point[0] < mid[0] and point[1] < mid[1]:
                rightPoints[3] = point
        return rightPoints, estimated_height, estimated_width
    # print("rightttttt")
    # print(rightPoints)



def get_card_kind(con, card_to_check):
    suma = 0
    good_areas = []
    res = 0
    good_con = []

    h, w = card_to_check.shape

    current_leftmost = [w, w]
    current_rightmost = [0, 0]
    current_topmost = [h, h]
    current_bottommost = [0, 0]

    leftmost = [0, 0]
    rightmost = [w, 0]
    topmost = [0, 0]
    bottommost = [h, w]

    max_area = 0

    for cnt in con:
        area = cv2.contourArea(cnt)
        print(area)
        if area > max_area and 100 < area < 1000:
            max_area = cv2.contourArea(cnt)

    for cnt in con:
        area = cv2.contourArea(cnt)
        print(area)

        if area == max_area:
            # cv2.drawContours(card_to_check, cnt, -1, (255, 255, 255), 3)
            res = res + 1
            suma = suma + area
            good_areas.append(area)
            good_con.append(cnt)

            leftmost = tuple(cnt[cnt[:, :, 0].argmin()][0])
            if leftmost[0] < current_leftmost[0]:
                current_leftmost = leftmost

            rightmost = tuple(cnt[cnt[:, :, 0].argmax()][0])
            if rightmost[0] > current_rightmost[0]:
                current_rightmost = rightmost

            topmost = tuple(cnt[cnt[:, :, 1].argmin()][0])
            if topmost[1] < current_topmost[1]:
                current_topmost = topmost

            bottommost = tuple(cnt[cnt[:, :, 1].argmax()][0])
            if bottommost[1] > current_bottommost[1]:
                current_bottommost = bottommost

    # print(leftmost)
    # print(rightmost)
    # print(topmost)
    # print(bottommost)

    card_kind = card_to_check[topmost[1] : bottommost[1], leftmost[0] : rightmost[0]]
    # cv2.imshow('Card ' + str(numberOfCards + 1), card_kind)
    # cv2.waitKey(3000)

    return card_kind


def check_card_shape_if_is_black(color_shape):
    h, w, i = color_shape.shape
    # print(color_shape[int(w/2), int(h/2)])
    if color_shape[int(w/2), int(h/2)][2] > 150:
        return False
    else:
        return True


def check_if_card_is_heart_or_diamond(color_shape):
    h, w, i = color_shape.shape
    color_shape = cv2.cvtColor(color_shape, cv2.COLOR_BGR2GRAY)
    color_shape = cv2.adaptiveThreshold(color_shape, 200, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 101, -10)
    print(str(0.25 * w) + ' ' + str(0.2 * h))
    print(str(0.25 * w) + ' ' + str(0.8 * h))
    print(color_shape[int(0.2*h), int(0.25*w)])
    print(color_shape[int(0.8*h), int(0.25*w)])

    if color_shape[int(0.2*h), int(0.25*w)] > 100 and color_shape[int(0.8*h), int(0.25*w)] > 100:
        return "of Diamonds"
    else:
        return "of Hearts"


def check_if_card_is_spades_or_clubs(color_shape):
    h, w, i = color_shape.shape
    if w / h > 52 / 58:
        return " of Clubs"
    else:
        return " of Spades"
