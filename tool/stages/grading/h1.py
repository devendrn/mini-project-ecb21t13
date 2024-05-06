import numpy as np
from PIL import Image, ImageChops


def grade(compressed_img: Image.Image, source_img: Image.Image) -> (float, Image.Image):
    """
        Vision centeric score [INCOMPLETE]

        1. Convert input images to HSV
        2. Find difference
        3. Split diff channels
        4. ...
        5. ...
        6. ...

        Returns:
            (score, normalized diff image)
    """
    compressed_img = compressed_img.convert('HSV')
    source_img = source_img.convert('HSV')

    diff = ImageChops.difference(compressed_img, source_img)

    (diff_h, diff_s, diff_v) = diff.split()

    diff = diff_h

    diff_array = np.asarray(diff)
    sq_diff_array = np.square(diff_array)
    diff_score = np.mean(sq_diff_array)

    diff_saturated = diff.point(lambda i: normalize(i, diff_score))
    return (diff_score, diff_saturated)


def normalize(val, mean):
    if mean == 0.0:
        return 0.0
    return 20.0 * abs(val * val) / mean
