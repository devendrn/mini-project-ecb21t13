import json
from config import DATA_JSON, SCORE_JSON
from config import SIZE_RATIO_KEY, GRADE_GMSE_KEY


def run():
    """
    Accumulates the scores for each quality into array
    """
    f = open(DATA_JSON)
    data = json.load(f)

    # score dict
    result = {}

    for format in data:
        categories = data[format]
        result[format] = {}

        for category in categories:
            images = categories[category]
            result[format][category] = {}

            for image in images:

                compressionRatio = []
                gmsError = []

                for q in images[image]:
                    compressionRatio.append(images[image][q][SIZE_RATIO_KEY])
                    gmsError.append(images[image][q][GRADE_GMSE_KEY])

                result[format][category][image] = {
                    "compression_ratio": compressionRatio,
                    "gms_error": gmsError,
                }

    with open(SCORE_JSON, 'w') as jsonFile:
        json.dump(result, jsonFile, indent=2)
        print("Dumped score array to score.json")
