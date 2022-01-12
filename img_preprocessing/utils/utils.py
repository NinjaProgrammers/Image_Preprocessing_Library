
import numpy as np
import matplotlib.pyplot as plt
import cv2
import math

HEXAGON_KERNEL_5X5 = np.array([[0, 1, 1, 1, 0], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [0, 1, 1, 1, 0]],
                              np.uint8)
RHOMB_KERNEL_3X3 = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], np.uint8)
STAR_KERNEL_3X3 = np.array([[1, 0, 1], [0, 1, 0], [1, 0, 1]], np.uint8)
CIRCLE_KERNEL_3X3 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
CIRCLE_KERNEL_4X4 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4))
CIRCLE_KERNEL_9X9 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
CIRCLE_KERNEL_5X5 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
CIRCLE_KERNEL_7X7 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
CIRCLE_KERNEL_11X11 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
SHARPEN_KERNEL = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])

WEIGTHS = [[0.2, 0.2, 0.6],
           [0.2, 0.6, 0.2],
           [0.6, 0.2, 0.2],
           [0.1, 0.1, 0.8],
           [0.1, 0.8, 0.1],
           [0.8, 0.1, 0.1],
           [0.9, 0.1, 0.0],
           [0.4, 0.3, 0.3],
           [0.3, 0.4, 0.4],
           [0.3, 0.3, 0.4]]


def __image__(image):
    """
    Read image from path to file or matrix
    :param image: path to image file or 3D-matrix representing RGB image
    :return: Original image, channels red, green, blue and gray image
    """
    original_image = image
    if isinstance(image,str):
        original_image = cv2.imread(image)
    gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

    red, green, blue = cv2.split(image)
    red = np.asarray(red)
    green = np.asarray(green)
    blue = np.asarray(blue)

    return original_image, red, green, blue, gray


def __plot_histogram__(hist):
    """
    Plot image histogram.
    :param hist: Image histogram
    :return: Show Histogram plot
    """
    x = [i for i in range(256)]
    plt.bar(x, histogram)
    plt.show()


def histogram(image):
    """
    Compute and plot image histogram
    :param image: String with reference to image file or 2D-matrix representing image.
    :return: Image histogram
    """
    if isinstance(image, str):
        image, *_ = __image__(image)
    hist = cv2.calcHist([image], [0], None, [256], [0, 256])
    hist = [hist[i][0] for i in range(256)]
    __plot_histogram__(hist)
    return hist



