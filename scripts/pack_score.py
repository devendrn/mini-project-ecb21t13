import json
from config import DATA_JSON, SCORE_JSON
from config import SIZE_RATIO_KEY, GRADE_MSE_KEY, GRADE_H1E_KEY


def run():
    """
    Accumulates the scores for each quality into array
    """
    f = open(DATA_JSON)
    data = json.load(f)

    scores = {}

    for format in data:
        categories = data[format]
        scores[format] = {}

        for category in categories:
            images = categories[category]
            scores[format][category] = {}

            for image in images:

                compressionRatio = []
                msError = []
                h1Error = []

                for q in images[image]:
                    compressionRatio.append(images[image][q][SIZE_RATIO_KEY])
                    msError.append(images[image][q][GRADE_MSE_KEY])
                    h1Error.append(images[image][q][GRADE_H1E_KEY])

                scores[format][category][image] = {
                    SIZE_RATIO_KEY: compressionRatio,
                    GRADE_MSE_KEY: msError,
                    GRADE_H1E_KEY: h1Error,
                }

    with open(SCORE_JSON, 'w') as jsonFile:
        json.dump(scores, jsonFile, indent=2)
        print("Dumped score array to score.json")
