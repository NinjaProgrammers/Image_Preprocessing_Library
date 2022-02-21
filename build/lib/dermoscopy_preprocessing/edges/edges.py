import numpy as np
import cv2
from ..utils import __image__


def sharpen(image, kernel):
    """
    RGB channels filtering with edge sharpening kernel
    :param image: Path to Image or 3D Matrix representing RGB image
    :param kernel: Edge sharpening kernel
    :return: Resulting image from merging RGB filtered channels
    """
    _, red, green, blue, _ = __image__(image)

    r_sharp = cv2.filter2D(red, -1, kernel)
    g_sharp = cv2.filter2D(green, -1, kernel)
    b_sharp = cv2.filter2D(blue, -1, kernel)

    return cv2.merge((r_sharp, g_sharp, b_sharp))


def laplacian(image):
    """
    Edge sharpening subtracting laplacian of RGB channels from original channels
    :param image: Path to Image or 3D Matrix representing RGB image
    :return: Resulting image from merging RGB filtered channels
    """
    _, red, green, blue, _ = __image__(image)

    abbsLaplace_red = cv2.Laplacian(red, -2)
    abbsLaplace_green = cv2.Laplacian(green, -2)
    abbsLaplace_blue = cv2.Laplacian(blue, -2)

    r = cv2.subtract(red, abbsLaplace_red)
    g = cv2.subtract(green, abbsLaplace_green)
    b = cv2.subtract(blue, abbsLaplace_blue)
    return cv2.merge((r, g, b))


def unsharp_filter(image, k):
    """
    Edge enhancement with unsharp method
    :param image: Path to Image or 3D Matrix representing RGB image
    :param k: Multiplication factor
    :return: Original image plus image with edge enhanced
    """
    original, *_ = __image__(image)
    gauss = cv2.getGaussianKernel(5, 1.5)
    blurred = cv2.filter2D(original, -1, gauss)
    sub = cv2.subtract(original, blurred)

    x = original + np.array(k * sub, dtype=np.uint8)
    return np.array(x, dtype=np.uint8)
