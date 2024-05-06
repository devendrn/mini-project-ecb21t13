from PIL import Image, ImageChops
import numpy as np
from config import OUT_DIR, DIFF_DIR
from config import GRADE_MSE_KEY, GRADE_H1E_KEY


def runGrading(source: str, compressed: str) -> (float):
    """
    Performs various grading analysis and ouputs score for each
    - ms: Mean square error
    - h1: Vision centric error

    Returns:
        (ms, h1)
    """
    compressedImg = Image.open(compressed)
    sourceImg = Image.open(source)

    if compressedImg.size != sourceImg.size:
        raise ValueError(f"{compressed} and {source} don't match in size.")

    # Convert both images to same color format
    compressedImg = compressedImg.convert('RGB')
    sourceImg = sourceImg.convert('RGB')

    (msScore, msDiff) = msGrade(compressedImg, sourceImg)
    (h1Score, h1Diff) = h1Grade(compressedImg, sourceImg)

    fileName = ''.join(compressed[len(OUT_DIR):].split(".")[:-1]) + ".jpg"
    msDiff.save(f"{DIFF_DIR}/{GRADE_MSE_KEY}{fileName}")
    h1Diff.save(f"{DIFF_DIR}/{GRADE_H1E_KEY}{fileName}")

    print(f"    ms={msScore}\n    h1={h1Score}")
    return (msScore, h1Score)


def normalize(val, mean):
    if mean == 0.0:
        return 0.0
    else:
        return 20.0 * abs(val * val) / mean


def msGrade(compressedImg: Image.Image, sourceImg: Image.Image) -> (float, Image.Image):
    """
        Mean square score

        1. Find RGB difference square between images
        2. Convert difference to luminance
        3. Find mean value of the diff image (gms score)
        4. Normalize diff image using mean value and store output

        Returns:
            (score, normalized diff image)
    """
    diff = ImageChops.difference(compressedImg, sourceImg)
    diff = diff.convert('L')

    diff_array = np.asarray(diff)
    sq_diff_array = np.square(diff_array)
    diffScore = np.mean(sq_diff_array)

    diffSaturated = diff.point(lambda i: normalize(i, diffScore))
    return (diffScore, diffSaturated)


def h1Grade(compressedImg: Image.Image, sourceImg: Image.Image) -> (float, Image.Image):
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
    compressedImg = compressedImg.convert('HSV')
    sourceImg = sourceImg.convert('HSV')

    diff = ImageChops.difference(compressedImg, sourceImg)

    (diffH, diffS, diffV) = diff.split()

    diff = diffH

    diff_array = np.asarray(diff)
    sq_diff_array = np.square(diff_array)
    diffScore = np.mean(sq_diff_array)

    diffSaturated = diff.point(lambda i: normalize(i, diffScore))
    return (diffScore, diffSaturated)
