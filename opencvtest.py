import cv2
import numpy as np


def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'

    class K:
        def __init__(self, obj, *args):
            self.obj = obj

        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0

        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0

        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0

        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0

        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0

        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0

    return K


def sort_grid_points(points):
    """
    Given a flat list of points (x, y), this function returns the list of
    points sorted from top to bottom, then groupwise from left to right.
    We assume that the points are nearly equidistant and have the form of a
    square.
    """
    w, _ = points.shape
    sqrt_w = int(np.sqrt(w))
    # sort by y
    points = points[np.argsort(points[:, 1])]
    # put the points in groups (rows)
    points = np.reshape(points, (sqrt_w, sqrt_w, 2))
    # sort rows by x
    points = np.vstack([row[np.argsort(row[:, 0])] for row in points])
    # undo shape transformation
    points = np.reshape(points, (w, 1, 2))
    return points


def cmp_height(x, y):
    """used for sorting by height"""
    _, _, _, hx = cv2.boundingRect(x)
    _, _, _, hy = cv2.boundingRect(y)
    return hy - hx


def cmp_width(x, y):
    """used for sorting by width"""
    _, _, wx, _ = cv2.boundingRect(x)
    _, _, wy, _ = cv2.boundingRect(y)
    return wy - wx


def draw_str(dst, x, y, s):
    """
    Draw a string with a dark contour
    """
    cv2.putText(dst, s, (int(x) + 1, int(y) + 1),
                cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 0),
                thickness=2, lineType=cv2.LINE_AA)
    cv2.putText(dst, s, (int(x), int(y)),
                cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255),
                lineType=cv2.LINE_AA)


filename = r'C:\Users\Michael\Desktop\schraeg.png'
pic = cv2.imread(filename)
if pic is not None:
    gray = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
    binary = cv2.adaptiveThreshold(
        src=gray, maxValue=255,
        adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        thresholdType=cv2.THRESH_BINARY, blockSize=11, C=2)
    blurred = cv2.medianBlur(binary, ksize=3)
    image, contours, hierarchy = cv2.findContours(image=cv2.bitwise_not(blurred), mode=cv2.RETR_LIST,
                                                  method=cv2.CHAIN_APPROX_SIMPLE)
    cv2.imshow('blurred', blurred)
    sudoku_area = 0
    sudoku_contour = None
    for cnt in contours:
        area = cv2.contourArea(cnt)
        x, y, w, h = cv2.boundingRect(cnt)
        if (0.7 < float(w) / h < 1.3  # aspect ratio
            and area > 150 * 150  # minimal area
            and area > sudoku_area  # biggest area on screen
            and area > .5 * w * h):  # fills bounding rect
            sudoku_area = area
            sudoku_contour = cnt

        if sudoku_contour is not None:
            # approximate the contour with connected lines
            perimeter = cv2.arcLength(curve=sudoku_contour, closed=True)
            approx = cv2.approxPolyDP(curve=sudoku_contour,
                                      epsilon=0.1 * perimeter,
                                      closed=True)
            if len(approx) == 4:
                mask = np.zeros(gray.shape, np.uint8)
                # fill a the sudoku-contour with white
                cv2.drawContours(mask, [sudoku_contour], 0, 255, -1)
                # invert the mask
                mask_inv = cv2.bitwise_not(mask)
                # the blurred picture is already thresholded so this step shows
                # only the black areas in the sudoku
                separated = cv2.bitwise_or(mask_inv, blurred)

                square = np.float32([[50, 50], [500, 50], [50, 500], [500, 500]])
                approx = np.float32([i[0] for i in approx])  # api needs conversion
                # sort the approx points to match the points defined in square
                approx = sort_grid_points(approx)

                m = cv2.getPerspectiveTransform(approx, square)
                transformed = cv2.warpPerspective(separated, m, (550, 550))



                sobel_x = cv2.Sobel(transformed, ddepth=-1, dx=1, dy=0)
                cv2.imshow('sobel_x', sobel_x)
                # closing x-axis
                kernel_x = np.array([[1]] * 20, dtype='uint8')  # vertical kernel
                dilated_x = cv2.dilate(sobel_x, kernel_x)
                closed_x = cv2.erode(dilated_x, kernel_x)
                _, threshed_x = cv2.threshold(closed_x, thresh=250, maxval=255,
                                              type=cv2.THRESH_BINARY)

                # generate mask for x
                image, contours, _ = cv2.findContours(image=threshed_x,
                                                      mode=cv2.RETR_LIST,
                                                      method=cv2.CHAIN_APPROX_SIMPLE)
                # sort contours by height
                sorted_contours = sorted(contours, key=cmp_to_key(cmp_height))

                # fill biggest 10 contours on mask (white)
                mask_x = np.zeros(transformed.shape, np.uint8)
                cv2.drawContours(mask_x, sorted_contours[:10], -1, 255, -1)
                cv2.imshow('mask_x', mask_x)
                sobel_y = cv2.Sobel(transformed, ddepth=-1, dx=0, dy=1)

                # closing y-axis
                kernel_y = np.array([[[1]] * 20], dtype='uint8')  # horizontal krnl
                dilated_y = cv2.dilate(sobel_y, kernel_y)
                closed_y = cv2.erode(dilated_y, kernel_y)
                _, threshed_y = cv2.threshold(closed_y, 250, 255,
                                              cv2.THRESH_BINARY)

                # generate mask for y
                image, contours, _ = cv2.findContours(image=threshed_y,
                                                      mode=cv2.RETR_LIST,
                                                      method=cv2.CHAIN_APPROX_SIMPLE)
                sorted_contours = sorted(contours, key=cmp_to_key(cmp_width))

                # fill biggest 10 on mask
                mask_y = np.zeros(transformed.shape, np.uint8)
                cv2.drawContours(mask_y, sorted_contours[:10], -1, 255, -1)

                dilated_ver = cv2.dilate(mask_x, kernel_x)
                dilated_hor = cv2.dilate(mask_y, kernel_y)
                # now we have the single crossing points as well as the complete
                # grid
                grid = cv2.bitwise_or(dilated_hor, dilated_ver)
                crossing = cv2.bitwise_and(dilated_hor, dilated_ver)

                #
                # 5. sort crossing points
                #
                image, contours, _ = cv2.findContours(image=crossing,
                                                      mode=cv2.RETR_LIST,
                                                      method=cv2.CHAIN_APPROX_SIMPLE)
                # a complete sudoku must have exactly 100 crossing points
                if len(contours) > 1:
                    # take the center points of the bounding rects of the crossing
                    # points. This should be precise enough, calculating the
                    # moments is not necessary.
                    crossing_points = np.empty(shape=(100, 2))
                    for n, cnt in enumerate(contours):
                        x, y, w, h = cv2.boundingRect(cnt)
                        cx, cy = (x + .5 * w, y + .5 * h)
                        crossing_points[n] = [int(cx), int(cy)]
                    sorted_cross_points = sort_grid_points(crossing_points)

                    for n, p in enumerate(sorted_cross_points):
                        px, py = p[0]
                        # draw_str(grid, px, py, str(n))
                    cv2.imshow('sorted grid', grid)

        cv2.drawContours(pic, [sudoku_contour], 0, 255)
        cv2.imshow('Input', pic)

    cv2.waitKey(0)
else:
    raise IOError('Cannot open file')

cv2.destroyAllWindows()
