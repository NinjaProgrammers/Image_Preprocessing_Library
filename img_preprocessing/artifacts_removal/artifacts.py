import cv2
import numpy as np
from ..utils import __image__
from ..utils import CIRCLE_KERNEL_5X5
import math


def morphological_closure_artifact_removal(image, kernel, blur=True):
    """
    Artifact removal using morphological closure
    :param image: Path to Image or 3D Matrix representing RGB image
    :param kernel: Kernel
    :param blur: True or False, indicates if a median blur
    should be applied before morphological closure
    :return: Resulting image of merging RGB channels after morphological closure
    """
    _, red, green, blue, _ = __image__(image)

    if blur:
        red = cv2.medianBlur(red, 5)
        green = cv2.medianBlur(green, 5)
        blue = cv2.medianBlur(blue, 5)

    r1 = cv2.morphologyEx(red, cv2.MORPH_CLOSE, kernel)
    g1 = cv2.morphologyEx(green, cv2.MORPH_CLOSE, kernel)
    b1 = cv2.morphologyEx(blue, cv2.MORPH_CLOSE, kernel)

    return cv2.merge((r1, g1, b1))


def __dull_razor__(image, kernel):
    blackhat = cv2.morphologyEx(image, cv2.MORPH_BLACKHAT, kernel)
    _, binary = cv2.threshold(blackhat, 10, 255, cv2.THRESH_BINARY)
    return cv2.inpaint(image, binary, 1, cv2.INPAINT_TELEA)


def dull_razor_artifact_removal(image, kernel):
    """
    Artifact Removal using Dull Razor method
    :param image: Path to Image or 3D Matrix representing RGB image
    :param kernel: Kernel
    :return: Resulting image of merging RGB channels after dull razor methd on each channel
    """
    _, red, green, blue, _ = __image__(image)
    r = __dull_razor__(red, kernel)
    g = __dull_razor__(green, kernel)
    b = __dull_razor__(blue, kernel)

    return cv2.merge((r, g, b))


def __generate_kernels__():
    kernel1 = np.zeros((9, 9), np.uint8)
    for i in range(9):
        for j in range(9):
            if i == 4:
                kernel1[i][j] = 1
    kernel2 = np.zeros((9, 9), np.uint8)
    for i in range(9):
        for j in range(9):
            if j == 4:
                kernel2[i][j] = 1
    kernel3 = np.zeros((9, 9), np.uint8)
    for i in range(9):
        for j in range(9):
            if i + j == 8:
                kernel3[i][j] = 1
    kernel4 = np.zeros((9, 9), np.uint8)
    for i in range(9):
        for j in range(9):
            if i - j == 0:
                kernel4[i][j] = 1
    return kernel1, kernel2, kernel3, kernel4


def __bothat__(image, kernel, kernel1, kernel2, kernel3, kernel4):
    blur = cv2.medianBlur(image, 3)
    laplacian = cv2.Laplacian(blur, cv2.CV_64F)
    difference = blur - laplacian
    bh1 = cv2.morphologyEx(difference, cv2.MORPH_BLACKHAT, kernel1)
    bh2 = cv2.morphologyEx(difference, cv2.MORPH_BLACKHAT, kernel2)
    bh3 = cv2.morphologyEx(difference, cv2.MORPH_BLACKHAT, kernel3)
    bh4 = cv2.morphologyEx(difference, cv2.MORPH_BLACKHAT, kernel4)

    blackhat = bh1 + bh2 + bh3 + bh4
    blackhat = np.asarray(blackhat, np.uint8)

    th, binary = cv2.threshold(blackhat, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    dilation = cv2.morphologyEx(binary, cv2.MORPH_DILATE, kernel)
    return cv2.inpaint(image, dilation, 1, cv2.INPAINT_TELEA)


def bothat_artifact_removal(image, kernel):
    """
    Artifact Removal using Bothat morphological operations
    :param image: Path to Image or 3D Matrix representing RGB image
    :param kernel: Kernel
    :return: Resulting image of merging RGB channels after bothat method on each channel
    """
    _, red, green, blue, _ = __image__(image)
    kernel1, kernel2, kernel3, kernel4 = __generate_kernels__()

    r = __bothat__(red, kernel, kernel1, kernel2, kernel3, kernel4)
    g = __bothat__(green, kernel, kernel1, kernel2, kernel3, kernel4)
    b = __bothat__(blue, kernel, kernel1, kernel2, kernel3, kernel4)

    return cv2.merge((r, g, b))


def __log_mask__(n, sigma2):
    arr = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            x = i - (n - 1) // 2
            y = j - (n - 1) // 2
            temp = (x ** 2 + y ** 2) / (2 * sigma2)
            arr[i][j] = (-1 / (math.pi * sigma2 ** 2)) * (1 - temp) * math.pow(math.e, -temp)
    return arr


def laplasian_of_gaussian(image):
    """
    Artifact Removal using Laplassian of Gaussian method
    :param image: Path to Image or 3D Matrix representing RGB image
    :return: Resulting image of merging RGB channels after bothat method on each channel
    """
    _, red, green, blue, _ = __image__(image)
    mask = __log_mask__(11,2)
    arrayLOG = cv2.filter2D(red, -1, mask)
    d = cv2.morphologyEx(arrayLOG, cv2.MORPH_DILATE, CIRCLE_KERNEL_5X5)
    e = cv2.morphologyEx(d, cv2.MORPH_ERODE, CIRCLE_KERNEL_5X5)

    r = cv2.inpaint(red, e, 3, cv2.INPAINT_TELEA)

    arrayLOG = cv2.filter2D(green, -1, mask)
    d = cv2.morphologyEx(arrayLOG, cv2.MORPH_DILATE, CIRCLE_KERNEL_5X5)
    e = cv2.morphologyEx(d, cv2.MORPH_ERODE, CIRCLE_KERNEL_5X5)
    g = cv2.inpaint(green, e, 3, cv2.INPAINT_TELEA)

    arrayLOG = cv2.filter2D(blue, -1, mask)
    d = cv2.morphologyEx(arrayLOG, cv2.MORPH_DILATE, CIRCLE_KERNEL_5X5)
    e = cv2.morphologyEx(d, cv2.MORPH_ERODE, CIRCLE_KERNEL_5X5)
    b = cv2.inpaint(blue, e, 3, cv2.INPAINT_TELEA)

    final = cv2.merge((r, g, b))
    return cv2.cvtColor(final, cv2.COLOR_BGR2RGB)


def clean_artifacts_remaining(image):
    """
    Method still on development. Use at own risk!
    Remove artifacts from image
    :param image: Path to Image or 3D Matrix representing RGB image
    :return: Image
    """
    img, *_ = __image__(image)
    blur = cv2.GaussianBlur(img, (3, 3), 0)

    # convert to hsv and get saturation channel
    sat = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)[:, :, 1]

    # threshold saturation channel
    thresh = cv2.threshold(sat, 50, 255, cv2.THRESH_BINARY)[1]

    # apply morphology close and open to make mask
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)
    mask = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel, iterations=1)

    # do OTSU threshold to get melanoma image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    pre_otsu = otsu.copy()

    otsu = cv2.dilate(otsu, kernel)
    otsu = cv2.erode(otsu, kernel)

    inv_otsu = otsu.copy()
    inv_otsu[otsu == 255] = 0
    inv_otsu[otsu == 0] = 255

    inpaint = mask - inv_otsu

    img_result = cv2.inpaint(img, inpaint, 100, cv2.INPAINT_TELEA)
    return cv2.cvtColor(img_result, cv2.COLOR_BGR2RGB), otsu
