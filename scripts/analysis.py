import glob
import subprocess
import os
import json
from config import REF_DIR, OUT_DIR, FORMATS, DATA_JSON, DIFF_DIR
from config import SIZE_RATIO_KEY, GRADE_MSE_KEY, GRADE_H1E_KEY
from scripts import grade

json_data = {}


def init_json_data():
    for format in FORMATS:
        json_data[format] = {}


def run():
    """
    Iterates through all compressed images in OUT_DIR and performs
    various comparision with corresponding image in REF_DIR. Output
    data will be in JSON format and stored in root directory as
    data.json
    """
    for format in FORMATS:
        for score_name in [GRADE_MSE_KEY, GRADE_H1E_KEY]:
            subprocess.run(
                ["mkdir", "-p", f"{DIFF_DIR}/{score_name}/{format}"]
            )

    init_json_data()
    formats = glob.glob(f"{OUT_DIR}/*/")
    for format in formats:
        compressed_images = glob.glob(f"{format}*")
        print(format[:-1])
        for image in compressed_images:
            analyze(image)

    # sort json data and dump to file
    json_data_sorted = sort_dict(json_data)
    with open(DATA_JSON, 'w') as json_file:
        json.dump(json_data_sorted, json_file, indent=2)
        print("Dumped analysis to data.json")


def decode_file_details(encoded_filename: str) -> (str, str, str, str):
    """
    Decodes file details from compressed file name

    Input:
        format: "category%file_name%quality.format"

    Outputs:
        (catergory, file_name, quality, format)
    """

    tmp = encoded_filename.split(".")
    filename_array = ''.join(tmp[:-1]).split("_-_")

    category = filename_array[0]
    filename = filename_array[1]
    quality = filename_array[2]
    format = tmp[-1]

    return (category, filename, quality, format)


def analyze(compressed_image: str):
    """
    Compares compressed image with reference image and updates jsonData
    """

    # get file details
    encoded_filename = '/'.join(compressed_image.split("/")[2:])
    (category, filename, quality, ext) = decode_file_details(encoded_filename)

    # get source location
    source_image = f"{REF_DIR}/{category}/{filename}.png"

    # compare size
    source_image_size = os.stat(source_image).st_size
    compressed_image_size = os.stat(compressed_image).st_size

    # initialize entries if not present
    if category not in json_data[ext]:
        json_data[ext][category] = {}

    if filename not in json_data[ext][category]:
        json_data[ext][category][filename] = {}

    print("-", filename, quality)
    (ms_score, h1Score) = grade.run_grading(source_image, compressed_image)

    # append results to jsonData
    json_data[ext][category][filename][f"{quality}"] = {
        SIZE_RATIO_KEY: compressed_image_size/float(source_image_size),
        GRADE_MSE_KEY: ms_score,
        GRADE_H1E_KEY: h1Score,
    }


def sort_dict(data: dict):
    """
    Sort dictionary including children
    """
    def get_key(item):
        return f"{len(item)}{item}"

    if isinstance(data, dict):
        return {key: sort_dict(data[key]) for key in sorted(data, key=get_key)}
    else:
        return data
