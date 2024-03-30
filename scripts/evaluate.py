import json
import matplotlib.pyplot as plt
from config import DATA_JSON, QUALITY_SETTINGS
from config import SIZE_RATIO_KEY, GRADE_GMSE_KEY


def run():
    f = open(DATA_JSON)
    data = json.load(f)

    for format in data:
        pics = data[format]
        if format == "png":
            continue
        for image in pics:
            compressionRatio = []
            gmsError = []
            for q in pics[image]:
                compressionRatio.append(pics[image][q][SIZE_RATIO_KEY])
                gmsError.append(pics[image][q][GRADE_GMSE_KEY])
            plt.plot(QUALITY_SETTINGS, gmsError)
    plt.legend(data)
    plt.show()
