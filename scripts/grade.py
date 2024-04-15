from PIL import Image, ImageChops
import numpy as np
from config import OUT_DIR, DIFF_DIR


def runGrading(source: str, compressed: str) -> (float):
    """
    Performs various grading analysis and ouputs score for each
    """

    compressedImg = Image.open(compressed)
    sourceImg = Image.open(source)

    if compressedImg.size != sourceImg.size:
        raise ValueError("Images must have the same size")

    # gray mean square score
    # 1. Convert image to grayscale
    # 2. Find difference square between images
    # 3. Find mean value of the diff image (gms score)
    # 4. Normalize diff image using mean value and store output
    aGray = compressedImg.convert('L')
    bGray = sourceImg.convert('L')
    diff = ImageChops.difference(aGray, bGray)
    diff_array = np.asarray(diff)
    sq_diff_array = np.square(diff_array)
    diffScore = np.mean(sq_diff_array)
    diffFile = ''.join((DIFF_DIR + compressed[len(OUT_DIR):]).split(".")[:-1])
    diffSaturated = diff.point(lambda i: normalize(i, diffScore))
    diffSaturated.save(diffFile + ".jpg", )

    print(f"    gms={diffScore}")
    return (diffScore)


def normalize(val, mean):
    if mean == 0.0:
        return 0.0
    else:
        return 20.0 * abs(val * val) / mean
