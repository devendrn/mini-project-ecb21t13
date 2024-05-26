import glob
import subprocess
import os
import json
from PIL import Image
from config import REF_DIR, OUT_DIR, FORMATS, DATA_JSON, DIFF_DIR
from config import SIZE_RATIO_KEY, GRADE_MSE_KEY, GRADE_H1E_KEY
import stages.util as util
import stages.grading.ms as ms_grade
import stages.grading.h1 as h1_grade
import threading


json_data = {}


def run():
    """
    Iterates through all compressed images in `OUT_DIR` and performs
    various comparision with corresponding image in `REF_DIR`.

    Output data will be stored in root directory as `data.json`
    """
    global json_data

    try:
        json_file = open(DATA_JSON, 'r')
        json_data = json.load(json_file)
        print('data.json loaded. Skipping files already processed.')
    except FileNotFoundError:
        print('data.json not found to resume from.')
    except json.decoder.JSONDecodeError:
        print('data.json found, but is empty.')

    # create folders for diff output
    for format in FORMATS:
        for score_name in [GRADE_MSE_KEY, GRADE_H1E_KEY]:
            subprocess.run(
                ["mkdir", "-p", f"{DIFF_DIR}/{score_name}/{format}"]
            )

    # initialize json data
    for format in FORMATS:
        if format not in json_data:
            json_data[format] = {}

    formats = glob.glob(f"{OUT_DIR}/*/")
    for format in formats:
        compressed_images = glob.glob(f"{format}*")
        print(format[:-1])
        i = 0
        for image in compressed_images:
            i = i + 1
            analyze(image)
            if i % 4 == 0:
                # update data.json after processing 4 images
                with open(DATA_JSON, 'w') as json_file:
                    json.dump(json_data, json_file)

    # sort json data and dump to file
    json_data_sorted = util.sort_dict(json_data)
    with open(DATA_JSON, 'w') as json_file:
        json.dump(json_data_sorted, json_file, indent=2)
        print("Dumped analysis to data.json")


def analyze(compressed_file: str):
    """
    Compares compressed image with reference image and updates jsonData

    Expects 'compressed_file' in the format:
        "compressed/folder/encoded_filename.format"

    Performs various grading analysis and ouputs score for each
    - cr: Compression ratio
    - ms: Mean square error
    - h1: Vision centric error

    Scores are appended to 'json_data'.
    Diff images are saved to `diff/grade/format/` directory
    """
    global json_data

    # get file details
    encoded_filename = '/'.join(compressed_file.split("/")[2:])
    (category, filename, quality, ext) = util.decode_file_details(encoded_filename)

    # get source location
    source_file = f"{REF_DIR}/{category}/{filename}.png"

    # initialize entries if not present
    if category not in json_data[ext]:
        json_data[ext][category] = {}
    if filename not in json_data[ext][category]:
        json_data[ext][category][filename] = {}

    if f"{quality}" in json_data[ext][category][filename]:
        print("-", category, "-", filename, quality, "skipped")
        return

    compressed_img = Image.open(compressed_file)
    source_img = Image.open(source_file)

    if compressed_img.size != source_img.size:
        raise ValueError(f"{compressed_file} and {source_file} don't match in size.")

    # convert both images to same color format
    compressed_img = compressed_img.convert('RGB')
    source_img = source_img.convert('RGB')

    # compare diff error
    # do in two separate threads
    return_from_ms = [None]
    return_from_h1 = [None]
    t1 = threading.Thread(target=msgrade, args=(compressed_img, source_img, return_from_ms))
    t2 = threading.Thread(target=h1grade, args=(compressed_img, source_img, return_from_h1))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    (ms_score, ms_diff) = return_from_ms[0]
    (h1_score, h1_diff) = return_from_h1[0]

    # compare size
    source_file_size = os.stat(source_file).st_size
    compressed_file_size = os.stat(compressed_file).st_size
    cr_score = compressed_file_size/float(source_file_size)

    print("-", category, "-", filename, quality)
    print(f"    cr={cr_score}")
    print(f"    ms={ms_score}")
    print(f"    h1={h1_score}")

    # append results to jsonData
    json_data[ext][category][filename][f"{quality}"] = {
        SIZE_RATIO_KEY: cr_score,
        GRADE_MSE_KEY: ms_score,
        GRADE_H1E_KEY: h1_score,
    }

    # save diff files
    diff_filename = ''.join(compressed_file[len(OUT_DIR):].split(".")[:-1]) + ".jpg"
    ms_diff.save(f"{DIFF_DIR}/{GRADE_MSE_KEY}{diff_filename}")
    h1_diff.save(f"{DIFF_DIR}/{GRADE_H1E_KEY}{diff_filename}")


def h1grade(compressed_img: Image.Image, source_img: Image.Image, return_val: (float, Image.Image)):
    return_val[0] = h1_grade.grade(compressed_img, source_img)


def msgrade(compressed_img: Image.Image, source_img: Image.Image, return_val: (float, Image.Image)):
    return_val[0] = ms_grade.grade(compressed_img, source_img)
