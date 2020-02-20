import cv2
import numpy as np
import helpful_functions as hf

file_name = 'images/example3.jpg'

imgColour = cv2.imread(str(file_name))
img = cv2.imread(str(file_name), 0)


# Try with absolute difference
def get_kind(card_to_check):
    card_kind = cv2.resize(card_to_check, (17, 24))
    # card_kind = cv2.bitwise_not(card_kind)
    # card_to_check = cv2.bitwise_not(card_to_check)
    cv2.imshow('Card ' + str(result + 1), card_to_check)
    cv2.waitKey(3000)

    best_diff = 1001
    best_card = 2
    card_number = 2

    for c in imgCard:
        diff_img = cv2.absdiff(card_kind, c)
        rank_diff = int(np.sum(diff_img) / 255)
        print(str(card_number) + "dif: " + str(rank_diff))

        if rank_diff < best_diff:
            best_diff = rank_diff
            best_card = card_number

        card_number = card_number + 1

    if best_card == 11:
        return 'J'
    elif best_card == 12:
        return 'Q'
    elif best_card == 13:
        return 'K'
    elif best_card == 14:
        return 'A'
    else:
        return best_card


imgCard = []

# Read card patterns
for i in range(0, 13):
    image_to_read = cv2.imread('images/' + str(i + 2) + '.jpg', 0)
    imgCard.append(image_to_read)

# Threshold
img2 = cv2.adaptiveThreshold(img, 200, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,101, -10)
cv2.imshow('image', img2)
cv2.waitKey(1000)

# Finding contours
contours, hierarchy = cv2.findContours(img2, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

# Number of cards
result = 0
cardsNumber = 0
resultColor = "dupa"

for contour in contours:
    if cv2.contourArea(contour) > 45000:
        print(cv2.contourArea(contour))
        (x, y, cardWidth, cardHeight) = cv2.boundingRect(contour)

        rightXCorner, rightYCorner = hf.choose_corner(x, y, cardWidth, cardHeight)
        # print("X: " + str(rightXCorner) + " ; Y: " + str(rightYCorner))

        # Frame corners - from green rectangles that makes frame for each card
        frameCardCorners = np.array([[x, y], [x + cardWidth, y],
                                     [x + cardWidth, y + cardHeight], [x, y + cardHeight]])
        # print(frameCardCorners)

        # Card corners - real corners of each card (blue colour)
        cardCorners = np.array([[0, 0], [0, 0], [0, 0], [0, 0]])

        rect = cv2.minAreaRect(contour)
        points = cv2.boxPoints(rect)
        points = np.array(points, np.float32)
        #
        height, width = img2.shape
        points, h, w = hf.get_right_points_order(points)
        # print("points")
        # print(points)

        points = np.array([points[0], points[1], points[2], points[3]], np.float32)

        dst = np.array([[w - 1, 0], [w - 1, h - 1],
                        [0, h - 1], [0, 0]], np.float32)
        M = cv2.getPerspectiveTransform(points, dst)

        card = cv2.warpPerspective(imgColour, M, (w, h))

        height, width, i = card.shape
        colorCard = card
        # cv2.imshow('Card ' + str(result + 1), card)
        # cv2.waitKey(3000)

        #Canny
        edges = cv2.Canny(card, 100, 200)
        # print(edges)

        # load the image, convert it to grayscale, and blur it slightly
        gray = cv2.cvtColor(card, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(card, (3, 3), 0)

        # apply Canny edge detection using a wide threshold, tight
        # threshold, and automatically determined threshold
        wide = cv2.Canny(blurred, 10, 200)
        tight = cv2.Canny(blurred, 225, 250)

        # show the images
        # cv2.imshow("Original", card)
        # cv2.imshow("Edges", np.hstack([wide, tight]))
        # cv2.waitKey(0)

        card = cv2.adaptiveThreshold(gray, 200, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                              cv2.THRESH_BINARY, 51, -10)
        kind_contours, kind_hierarchy = cv2.findContours(card, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        result = 0
        cardsNumber = cardsNumber + 1
        h, w = card.shape

        for kind_contour in kind_contours:
            # print(cv2.contourArea(kind_contour))
            if 3000 > cv2.contourArea(kind_contour) > 1100:
                # (x, y, cardWidth, cardHeight) = cv2.boundingRect(contour)
                # print(cv2.contourArea(kind_contour))
                # cv2.drawContours(card, kind_contour, -1, (255, 255, 255), 3)
                result = result + 1

                (x, y, cardWidth, cardHeight) = cv2.boundingRect(kind_contour)
                # img_color = card[y : y + cardHeight, x : x + cardWidth]
                color_shape = colorCard[y : y + cardHeight, x: x + cardWidth]

        # cv2.imshow("kolor" + str(cardsNumber + 1), color_shape)
        # cv2.waitKey(3000)

        color_h, color_w, i = color_shape.shape

        is_black = hf.check_card_shape_if_is_black(color_shape)
        print(is_black)

        if is_black:
            resultColor = hf.check_if_card_is_spades_or_clubs(color_shape)
        else:
            resultColor = hf.check_if_card_is_heart_or_diamond(color_shape)

        print("kolor:" + resultColor)

        # cv2.imshow("kolor" + str(cardsNumber + 1), colorCard)
        # cv2.waitKey(3000)

        if result > 10:
            result = 10
        # if card[int(w / 2), int(h / 2)] < 100 and result > 1:
        #     result = result - 1

        cv2.imshow("tight" + str(cardsNumber + 1), card)
        cv2.waitKey(3000)
        print(result)

        x, y = hf.get_center_point(points)
        x = int(x)
        y = int(y)

        # Type text with cards
        font = cv2.FONT_HERSHEY_SIMPLEX
        bottomLeftCornerOfText = (x, y)
        fontScale = 0.75
        fontColor = (0, 0, 255)
        lineType = 2

        if result == 1:
            result = 'Ace '

        cv2.putText(imgColour, str(result) + str(resultColor),
                    bottomLeftCornerOfText,
                    font,
                    fontScale,
                    fontColor,
                    lineType)

# Type text with number of cards detected
font = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (50, 50)
fontScale = 0.75
fontColor = (0, 0, 255)
lineType = 2

cv2.putText(imgColour, 'Number of cards: ' + str(cardsNumber),
            bottomLeftCornerOfText,
            font,
            fontScale,
            fontColor,
            lineType)

cv2.imshow('Results', imgColour)
cv2.waitKey(100000)
