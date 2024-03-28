import glob
import subprocess
import platform

MAGICK_BIN = "bin/magick"
if platform.system() == "Windows":
    MAGICK_BIN += ".exe"


def run(formats: [str], refDir: str, outDir: str):
    """
    Compresses all raw images in refDir into various file formats
    specified in formats, using quality settings from 10% to 90%.

    Compressed images will be inside outDir/formatName/.

    Args:
        formats: Formats to use (Must be supported by magick)
        refDir: Source location
        outDir: Output location
    """

    refImages = glob.glob(f"{refDir}/*.png")

    for format in formats:
        subprocess.run(["mkdir", "-p", f"{outDir}/{format}"])

    print(f"Selected formats: \n - {formats}")
    print("Found source images: ")
    for source in refImages:
        print(f"- {source}")

    print("Compressing source images: ")
    for format in formats:
        print(f"- {format.upper()}:")
        for source in refImages:
            fileName = source[len(refDir) + 1:-4]
            for quality in range(10, 101, 10):
                outFileName = f"{fileName}_{quality}.{format}"
                output = f"{outDir}/{format}/{outFileName}"
                magick_compress(source, output, quality)
                print(f"  - {fileName} - {quality}%", end="\r")
            print(f"  - {fileName}", " " * 7)

    print()


def magick_compress(source: str, output: str, quality: int):
    subprocess.run([
        MAGICK_BIN, source, "-strip", "-quality", f"{quality}%", output
    ])
