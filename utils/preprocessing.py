import numpy
# import matplotlib
# matplotlib.use("TkAgg")
# import matplotlib.pyplot as plt
import cv2
def mask_2_hole(image, mask):
    """
    Process the input image and the mask into one image with hole.
    When the whole denoted by -1
    and the pixels are iin range of [0,1]
    :param image:  [H,W] grayscale image
    :param mask:   [H,W] grayscale mask image with the same size
    :return:
    """
    image = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY).astype('float32') / 255.
    mask = cv2.cvtColor(mask,cv2.COLOR_RGB2GRAY).astype('float32') / 255.
    out_image = image  * 1.
    out_image[~mask.astype(bool)] = -1.
    return out_image