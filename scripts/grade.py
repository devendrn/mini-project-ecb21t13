import numpy as np
from PIL import Image, ImageChops
from config import OUT_DIR, DIFF_DIR
from config import GRADE_MSE_KEY, GRADE_H1E_KEY


def run_grading(source: str, compressed: str) -> (float):
    """
    Performs various grading analysis and ouputs score for each
    - ms: Mean square error
    - h1: Vision centric error

    Returns:
        (ms, h1)
    """
    compressed_img = Image.open(compressed)
    source_img = Image.open(source)

    if compressed_img.size != source_img.size:
        raise ValueError(f"{compressed} and {source} don't match in size.")

    # Convert both images to same color format
    compressed_img = compressed_img.convert('RGB')
    source_img = source_img.convert('RGB')

    (ms_score, ms_diff) = ms_grade(compressed_img, source_img)
    (h1_score, h1_diff) = h1_grade(compressed_img, source_img)

    filename = ''.join(compressed[len(OUT_DIR):].split(".")[:-1]) + ".jpg"
    ms_diff.save(f"{DIFF_DIR}/{GRADE_MSE_KEY}{filename}")
    h1_diff.save(f"{DIFF_DIR}/{GRADE_H1E_KEY}{filename}")

    print(f"    ms={ms_score}\n    h1={h1_score}")
    return (ms_score, h1_score)


def normalize(val, mean):
    if mean == 0.0:
        return 0.0
    else:
        return 20.0 * abs(val * val) / mean


def ms_grade(compressed_img: Image.Image, source_img: Image.Image) -> (float, Image.Image):
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
    diffScore = np.mean(sq_diff_array)

    diffSaturated = diff.point(lambda i: normalize(i, diffScore))
    return (diffScore, diffSaturated)


def h1_grade(compressed_img: Image.Image, source_img: Image.Image) -> (float, Image.Image):
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
