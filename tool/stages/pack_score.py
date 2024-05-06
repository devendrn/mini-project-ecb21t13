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

                compression_ratio = []
                ms_error = []
                h1_error = []

                for q in images[image]:
                    compression_ratio.append(images[image][q][SIZE_RATIO_KEY])
                    ms_error.append(images[image][q][GRADE_MSE_KEY])
                    h1_error.append(images[image][q][GRADE_H1E_KEY])

                scores[format][category][image] = {
                    SIZE_RATIO_KEY: compression_ratio,
                    GRADE_MSE_KEY: ms_error,
                    GRADE_H1E_KEY: h1_error,
                }

    with open(SCORE_JSON, 'w') as json_file:
        json.dump(scores, json_file, indent=2)
        print("Dumped score array to score.json")
