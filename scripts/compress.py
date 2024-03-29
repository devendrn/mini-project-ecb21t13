import glob
import subprocess
import platform
from config import FORMATS, OUT_DIR, REF_DIR

MAGICK_BIN = "bin/magick"
if platform.system() == "Windows":
    MAGICK_BIN += ".exe"


def run():
    """
    Compresses all raw images in refDir into various file formats
    specified in formats, using quality settings from 10% to 90%.

    Compressed images will be inside outDir/formatName/.
    """

    refImages = glob.glob(f"{REF_DIR}/*.png")

    for format in FORMATS:
        subprocess.run(["mkdir", "-p", f"{OUT_DIR}/{format}"])

    print(f"Selected formats: \n - {FORMATS}")
    print("Found source images: ")
    for source in refImages:
        print(f"- {source}")

    print("Compressing source images: ")
    for format in FORMATS:
        print(f"- {format.upper()}:")
        for source in refImages:
            fileName = source[len(REF_DIR) + 1:-4]
            for quality in range(10, 101, 10):
                outFileName = f"{fileName}_{quality}.{format}"
                output = f"{OUT_DIR}/{format}/{outFileName}"
                magick_compress(source, output, quality)
                print(f"  - {fileName} - {quality}%", end="\r")
            print(f"  - {fileName}", " " * 7)

    print()


def magick_compress(source: str, output: str, quality: int):
    subprocess.run([
        MAGICK_BIN, source, "-strip", "-quality", f"{quality}%", output
    ])
