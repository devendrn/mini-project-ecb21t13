import glob
from config import REF_DIR, OUT_DIR, FORMATS, DATA_JSON
from config import SIZE_RATIO_KEY, GRADE_GMSE_KEY

import os
import json
from scripts import grade

jsonData = {}


def initJsonData():
    for format in FORMATS:
        jsonData[format] = {}


def run():
    """
    Iterates through all compressed images in OUT_DIR and performs
    various comparision with corresponding image in REF_DIR. Output
    data will be in JSON format and stored in root directory as
    data.json
    """
    initJsonData()
    formats = glob.glob(f"{OUT_DIR}/*/")
    for format in formats:
        compressedImages = glob.glob(f"{format}*")
        print(format[:-1])
        for image in compressedImages:
            analyze(image)

    jsonDataSorted = sortDict(jsonData)
    with open(DATA_JSON, 'w') as jsonFile:
        json.dump(jsonDataSorted, jsonFile, indent=2)
        print("Dumped analysis to data.json")


def decodeFileDetails(encodedFileName: str) -> (str, str, str):
    tmp = encodedFileName.split(".")
    sourceFile = ''.join(tmp[:-1])
    tmp2 = sourceFile.split("_")
    fileName = '_'.join(tmp2[:-1])
    quality = int(tmp2[-1])
    format = tmp[-1]
    return (fileName, quality, format)


def analyze(compressedImage: str):
    encodedFileName = '/'.join(compressedImage.split("/")[2:])
    (fileName, quality, ext) = decodeFileDetails(encodedFileName)

    sourceImage = f"{REF_DIR}/{fileName}.png"
    sourceImageSize = os.stat(sourceImage).st_size
    compressedImageSize = os.stat(compressedImage).st_size

    if fileName not in jsonData[ext]:
        jsonData[ext][fileName] = {}

    (gmsScore) = grade.runGrading(sourceImage, compressedImage)

    jsonData[ext][fileName][f"{quality}"] = {
        SIZE_RATIO_KEY: compressedImageSize/float(sourceImageSize),
        GRADE_GMSE_KEY: gmsScore,
    }

    print("-", fileName, quality)


def sortDict(data: dict):
    def getKey(item):
        return f"{len(item)}{item}"

    if isinstance(data, dict):
        return {key: sortDict(data[key]) for key in sorted(data, key=getKey)}
    else:
        return data
