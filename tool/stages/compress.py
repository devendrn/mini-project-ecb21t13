import glob
import subprocess
import os
import stages.util as util
from config import FORMATS, OUT_DIR, REF_DIR, QUALITY_SETTINGS

MAGICK_BIN = "magick"


def run():
    """
    Compresses all raw images in refDir into various file formats
    specified in formats, using quality settings from 10% to 90%.

    Compressed images will be inside outDir/formatName/.
    """

    ref_images = glob.glob(f"{REF_DIR}/*/*.png")

    for format in FORMATS:
        subprocess.run(["mkdir", "-p", f"{OUT_DIR}/{format}"])

    print(f"Selected formats: \n - {FORMATS}")

    print("Found source images: ")
    for source in ref_images:
        print(f"- {source}")

    print("Compressing source images: ")
    for format in FORMATS:
        print(f"- {format.upper()}:")
        for source in ref_images:
            # source is in "reference/category/filename.png" format
            filename_array = source[len(REF_DIR) + 1:-4].split("/")
            category = filename_array[0]
            filename = filename_array[1]

            for quality in QUALITY_SETTINGS:
                out_filename = util.encode_filename(category, filename, quality, format)
                output = f"{OUT_DIR}/{format}/{out_filename}"
                if os.path.exists(output):
                    continue
                magick_compress(source, output, quality)
                print(f"  - {category} - {filename} - {quality}%", end="\r")
            print(f"  - {category} - {filename}", " " * 7)

    print()


def magick_compress(source: str, output: str, quality: int):
    subprocess.run([
        MAGICK_BIN, source, "-strip", "-quality", f"{quality}%", output
    ])
