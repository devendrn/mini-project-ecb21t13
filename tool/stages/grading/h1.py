import numpy as np
from PIL import Image, ImageFilter
from collections.abc import Callable


def grade(compressed_img: Image.Image, source_img: Image.Image) -> (float, Image.Image):
    """
        Vision centeric score [INCOMPLETE]

        1. Convert input images to HSV
        2. Find H1 error for each pixel
        3. Apply 3x3 Min Filter to diff
        4. Find mean value of diff
        5. Normalize the diff output and save image

        Returns:
            (score, normalized diff image)
    """
    compressed_img = compressed_img.convert('HSV')
    source_img = source_img.convert('HSV')
    diff = multiband_point_operation(compressed_img, source_img, h1_pixel_error)
    diff = diff.filter(ImageFilter.MinFilter)

    diff_array = np.asarray(diff)
    sq_diff_array = np.square(diff_array)
    diff_score = np.mean(sq_diff_array)

    if diff_score > 0.0:
        diff = diff.point(lambda i: 20.0 * abs(i * i) / diff_score)

    return (diff_score, diff)


def multiband_point_operation(img_x: Image.Image, img_y: Image.Image, point_operation: Callable[[list[float]], list[float]]) -> Image.Image:
    """
    Performs a point operation on corresponding bands of two multiband images.
    Assumes img_x.mode == img_y.mode and img_x.size == img_y.size.

    Args:
        img_x: The first multiband image.
        img_y: The second multiband image.
        point_operation : The lambda function (x_bands, y_bands) -> z_bands

    Returns:
        PIL.Image: A single band resulting image
    """

    pixels_x = img_x.load()
    pixels_y = img_y.load()

    width, height = img_x.size
    new_image = Image.new('L', (width, height))
    pixels_new = new_image.load()

    for y in range(height):
        for x in range(width):
            pixels_new[x, y] = point_operation(pixels_x[x, y], pixels_y[x, y])

    return new_image


def h1_pixel_error(c: [int], o: [int]) -> int:
    """
    Args:
        c: Compressed pixel (HSV)
        o: Original pixel (HSV)

    Returns:
        Diff pixel (L)
    """
    (ch, cs, cv) = c
    (oh, os, ov) = o

    h_sa = 1.0 - (((oh-57) % 255) / 127.5)
    h_sa *= h_sa
    sensitivity = 1.0 - (h_sa*h_sa*h_sa)
    sensitivity = 1.0 - 0.25*(sensitivity*sensitivity)
    sensitivity *= os / 255.0

    eh = abs(cv - ov)
    es = (abs(cs - cs) * ov) / 255
    ev = (min(abs(ch - oh), ch + (255 - oh)) * ov) / 255

    e = (eh + es + ev) * sensitivity
    return int(e)
