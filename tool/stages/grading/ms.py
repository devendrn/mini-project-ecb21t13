import numpy as np
from PIL import Image, ImageChops


def grade(compressed_img: Image.Image, source_img: Image.Image) -> (float, Image.Image):
    """
        Mean square score

        1. Find RGB difference square between images
        2. Convert difference to luminance
        3. Find mean value of the diff image (gms score)
        4. Normalize diff image using mean value and store output

        Returns:
            (score, normalized diff image)
    """
    diff = ImageChops.difference(compressed_img, source_img)
    diff = diff.convert('L')

    diff_array = np.asarray(diff)
    sq_diff_array = np.square(diff_array)
    diff_score = np.mean(sq_diff_array)

    diff_saturated = diff.point(lambda i: normalize(i, diff_score))
    return (diff_score, diff_saturated)


def normalize(val, mean):
    if mean == 0.0:
        return 0.0
    return 20.0 * abs(val * val) / mean
