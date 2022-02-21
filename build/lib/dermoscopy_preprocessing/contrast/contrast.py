import numpy as np
import matplotlib.pyplot as plt
import cv2
from ..utils import __image__


def equalize_histogram(image):
    """
    Classical Histogram Equalization.
    Histogram Equalization for each RGB channel and merge the results
    :param image: Path to Image or 3D Matrix representing RGB image
    :return: Image from merging equalized histogram of RGB channels
    """
    original, red, green, blue, _ = __image__(image)

    # Equalize histogram for each channel
    red_equalized = cv2.equalizeHist(red)
    green_equalized = cv2.equalizeHist(green)
    blue_equalized = cv2.equalizeHist(blue)

    return cv2.merge((red_equalized, green_equalized, blue_equalized))


def clahe(image, clip_limit=3, tile_grid_size=(3, 3)):
    """
    Contrast Limited Adaptive Histogram Equalization.
    CLAHE applied to each RGB channel and results merged
    :param image:  Path to Image or 3D Matrix representing RGB image
    :param clip_limit: Threshold for contrast limiting.
    :param tile_grid_size: Size of grid for histogram equalization. Input image will be divided into
    equally sized rectangular tiles. tile_grid_size defines the number of tiles in row and column.
    :return: Image from merging clahe of RGB channels
    """
    original, red, green, blue, _ = __image__(image)

    cl = cv2.createCLAHE(clip_limit, tile_grid_size)
    red_clahe = cl.apply(red)
    green_clahe = cl.apply(green)
    blue_clahe = cl.apply(blue)

    return cv2.merge((red_clahe, green_clahe, blue_clahe))


def automatic_brightness_and_contrast(image, clip_histogram_percent=25):
    """
    Automatic contrast and image brightness calculated by cumulative function on image histogram
    :param image: Path to Image or 3D Matrix representing RGB image
    :param clip_histogram_percent:
    :return: Image with contrast and brightness enhanced
    """

    original, _, _, _, gray = __image__(image)
    # Calculate grayscale histogram
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    hist_size = len(hist)

    # Calculate cumulative distribution from the histogram
    accumulator = [float(hist[0])]
    for index in range(1, hist_size):
        accumulator.append(accumulator[index - 1] + float(hist[index]))

    # Locate points to clip
    maximum = accumulator[-1]
    clip_histogram_percent *= (maximum / 100.0)
    clip_histogram_percent /= 2.0

    # Locate left cut
    minimum_gray = 0
    while accumulator[minimum_gray] < clip_histogram_percent:
        minimum_gray += 1

    # Locate right cut
    maximum_gray = hist_size - 1
    while accumulator[maximum_gray] >= (maximum - clip_histogram_percent):
        maximum_gray -= 1

    # Calculate alpha and beta values
    alpha = 255 / (maximum_gray - minimum_gray)
    beta = -minimum_gray * alpha

    auto_result = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return auto_result, alpha, beta


def window_enhancement(image, window_min, window_max):
    """
    Contrast enhancement of gray image by modifying histogram in a range
    :param image: Path to Image or 3D Matrix representing RGB image
    :param window_min: Minimal range of window
    :param window_max: Maximal range of window
    :return: Image in gray scale with contrast enhanced
    """
    _, _, _, _, gray = __image__(image)
    n, m = len(gray), len(gray[0])
    arr = np.zeros((n, m))

    Imin, Imax = 0, 255
    for i in range(n):
        for j in range(m):
            if gray[i][j] < window_min:
                arr[i][j] = Imin
            elif gray[i][j] > window_max:
                arr[i][j] = Imax
            else:
                arr[i][j] = int((gray[i][j] - window_min) * (Imax - Imin) / (window_max - window_min) + Imin)

    return arr


def __calculate_normalized_bcv__(hist):
    best = 0
    L = 256

    n = sum(hist)
    mut = sum(i * hist[i] / n for i in range(L))
    p1, mu = 0, 0

    sigma2t = sum((i - mut) ** 2 * hist[i] / n for i in range(L))

    for t in range(L):
        p1 += hist[t] / n
        mu += t * hist[t] / n

        if p1 == 0 or p1 == 1:
            continue
        p2 = 1 - p1

        mu1 = mu / p1
        mu2 = (mut - mu) / p2
        sigma2b = p1 * p2 * (mu1 - mu2) ** 2
        curBCV = sigma2b / sigma2t

        if curBCV > best:
            best = curBCV
    return best / sigma2t


def histogram_bimodality(image, weights):
    """
    Contrast enhancement by maximizing histogram bimodality
    :param image: Path to Image or 3D Matrix representing RGB image
    :param weights: Tuple of 3 values or array of tuples for channels RGB.
    The sum of values must be 1. Ex: [(0.6,0.2,0.2),(0.4,0.4,0.2)]
    Avoid zero values for any of the channels
    :return: Image with contrast enhanced and best weight obtained
    """
    original, red, green, blue, _ = __image__(image)

    bestImage = None
    maxBCV = 0
    bestWeight = 0

    for (r, g, b) in weights:
        newImage = red * r + green * g + blue * b
        newImage = np.asarray(newImage, np.uint8)
        hist = cv2.calcHist([newImage], [0], None, [256], [0, 256])
        hist = [hist[i][0] for i in range(256)]

        bcv = __calculate_normalized_bcv__(hist)
        if bcv > maxBCV:
            maxBCV = bcv
            bestImage = newImage
            bestWeight = (r, g, b)

    return cv2.cvtColor(bestImage, cv2.COLOR_BGR2RGB), bestWeight


def __morph_preprocessing__(image, kernel):
    """
    Calculates tophat and bottomhat of image
    :param image: Path to Image or 3D Matrix representing RGB image
    :param kernel: Morphological kernel
    :return: Original Image, Tophat and Bottomhat
    """
    original, *_ = __image__(image)
    tophat = cv2.morphologyEx(original, cv2.MORPH_TOPHAT, kernel)
    bottomhat = cv2.morphologyEx(original, cv2.MORPH_BLACKHAT, kernel)
    return original, tophat, bottomhat


def morphological_contrast_enhancement(image, kernel):
    """
    Contrast enhancement usign morphological operations
    :param image: Path to Image or 3D Matrix representing RGB image
    :param kernel: Morphological kernel
    :return: Original image plus tophat image of original minus bottomhat operation of original image
    """
    original, tophat, bottomhat = __morph_preprocessing__(image, kernel)
    final = original + tophat - bottomhat
    return cv2.cvtColor(final, cv2.COLOR_BGR2RGB)


def reverse_morphological_contrast_enhancement(image, kernel):
    """
    Contrast enhancement usign morphological operations
    :param image:  Path to Image or 3D Matrix representing RGB image
    :param kernel: Morphological kernel
    :return: Original image minus tophat image of original plus bottomhat operation of original image
    """
    original, tophat, bottomhat = __morph_preprocessing__(image, kernel)
    final = original - tophat + bottomhat
    return cv2.cvtColor(final, cv2.COLOR_BGR2RGB)
