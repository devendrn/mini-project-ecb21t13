from PIL import Image, ImageChops
import numpy as np


def runGrading(source: str, compressed: str):
    compressedImg = Image.open(compressed)
    sourceImg = Image.open(source)

    if compressedImg.size != sourceImg.size:
        raise ValueError("Images must have the same size")

    # gray mean square score
    aGray = compressedImg.convert('L')
    bGray = sourceImg.convert('L')
    diff = ImageChops.difference(aGray, bGray)
    diff_array = np.asarray(diff)
    sq_diff_array = np.square(diff_array)
    diffScore = np.mean(sq_diff_array)

    print(source, compressed, diffScore)
    return (diffScore)
