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

    # sort json data and dump to file
    jsonDataSorted = sortDict(jsonData)
    with open(DATA_JSON, 'w') as jsonFile:
        json.dump(jsonDataSorted, jsonFile, indent=2)
        print("Dumped analysis to data.json")


def decodeFileDetails(encodedFileName: str) -> (str, str, str, str):
    """
    Decodes file details from compressed file name

    Input:
        format: "category%file_name%quality.format"

    Outputs:
        (catergory, file_name, quality, format)
    """

    tmp = encodedFileName.split(".")
    fileNameArray = ''.join(tmp[:-1]).split("%")

    category = fileNameArray[0]
    fileName = fileNameArray[1]
    quality = fileNameArray[2]
    format = tmp[-1]

    return (category, fileName, quality, format)


def analyze(compressedImage: str):
    """
    Compares compressed image with reference image and updates jsonData
    """

    # get file details
    encodedFileName = '/'.join(compressedImage.split("/")[2:])
    (category, fileName, quality, ext) = decodeFileDetails(encodedFileName)

    # get source location
    sourceImage = f"{REF_DIR}/{category}/{fileName}.png"

    # compare size
    sourceImageSize = os.stat(sourceImage).st_size
    compressedImageSize = os.stat(compressedImage).st_size

    # initialize entries if not present
    if category not in jsonData[ext]:
        jsonData[ext][category] = {}

    if fileName not in jsonData[ext][category]:
        jsonData[ext][category][fileName] = {}

    # calcuate quality scores
    (gmsScore) = grade.runGrading(sourceImage, compressedImage)

    # append results to jsonData
    jsonData[ext][category][fileName][f"{quality}"] = {
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
