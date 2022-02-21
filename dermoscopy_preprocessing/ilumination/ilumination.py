import numpy as np
import cv2
from ..utils import __image__

M = 256


def __mullog__(f, lambd):
    return np.asarray(M - M * (1 - f / M) ** lambd, np.uint8)


def mul_log_brightness_enhancement(image, factor=5):
    """
    Brightness enhancement with multiplication on logarithm space
    :param image:  Path to Image or 3D Matrix representing RGB image
    :param factor: Multiplication Factor
    :return: Image with brightness enhanced in RGB channels
    """
    _, red, green, blue, _ = __image__(image)
    r = __mullog__(red, factor)
    g = __mullog__(green, factor)
    b = __mullog__(blue, factor)

    img = cv2.merge((b, g, r))
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

def automatic_brightness_and_contrast(image, clip_histogram_percent=25):
    """
    Automatic contrast and image brightness calculated by cumulative function on image histogram
    :param image: Path to Image or 3D Matrix representing RGB image
    :param clip_histogram_percent:
    :return: Image enhanced, alpha and beta parameters
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

