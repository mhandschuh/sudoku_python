import cv2
import numpy as np


def cv_rgb(r, g, b):
    return cv2.scalar(b, g, r, 0)


def preprocess(pic):
    gray = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, ksize=(11, 11), sigmaX=0)
    threshold = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 2)
    bitwise_not = cv2.bitwise_not(threshold)
    dilate_kernel = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], dtype='uint8')
    dilated = cv2.dilate(bitwise_not, dilate_kernel)
    cv2.imshow('dilated', dilated)
    return dilated


def findbigestblob(img):
    height = np.size(img, 0)
    width = np.size(img, 1)

    count = 0
    max = None
    maxPt = None

    mask = np.zeros((height + 2, width + 2), np.uint8)

    for y in range(height):
        for x in range(width):
            value = img[y]
            if value[x] >= 128:
                mask[:] = 0
                r, i, m, area = cv2.floodFill(img, mask, (x, y), (255, 0, 0))

                if max is None or area > max:
                    maxPt = (x, y)
                    max = area

    mask[:] = 0
    cv2.floodFill(img, mask, maxPt, (255, 255, 255))
    cv2.imshow('flooded', img)
    return None


def findSudoku():
    filename = r'C:\Users\Michael\Desktop\sudoku3.jpg'
    # filename = r'C:\Users\Michael\Desktop\sudoku.png'
    # filename = r'C:\Users\Michael\Desktop\schraeg.png'
    img = cv2.imread(filename)
    if img is not None:
        img_preprocessed = preprocess(img)
        img_biggestblob = findbigestblob(img_preprocessed)
        cv2.waitKey(0)
    else:
        raise IOError('Cannot open file')

    cv2.destroyAllWindows()


findSudoku()
