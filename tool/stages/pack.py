import json
import glob
from config import DATA_JSON, SCORE_JSON, DIFF_JSON
from config import SIZE_RATIO_KEY, GRADE_MSE_KEY, GRADE_H1E_KEY
from config import FORMATS, QUALITY_SETTINGS


def run():
    """
    Accumulates the scores for each quality into array
    """
    f = open(DATA_JSON)
    data = json.load(f)

    used_images = list(map(lambda s: "/".join(s[:-4].split("/")[1:]), glob.glob("reference/*/*.png")))

    scores = {}
    diff = {
        "images": used_images,
        "formats": FORMATS,
        "gradings": [GRADE_MSE_KEY, GRADE_H1E_KEY],
        "qualities": QUALITY_SETTINGS
    }

    for format in data:
        categories = data[format]
        scores[format] = {}

        for category in categories:
            images = categories[category]
            scores[format][category] = {}

            for image in images:
                # to sort errors based on compression ratio
                errors = []
                for q in images[image]:
                    values = images[image][q]
                    errors.append(
                        [
                            values[SIZE_RATIO_KEY],
                            [values[GRADE_MSE_KEY], values[GRADE_H1E_KEY]]
                        ]
                    )
                errors.sort(key=lambda x: x[0])

                cr = []
                ms_error = []
                h1_error = []
                for i in errors:
                    print(i)
                    cr.append(i[0])
                    ms_error.append(i[1][0])
                    h1_error.append(i[1][1])

                scores[format][category][image] = {
                    SIZE_RATIO_KEY: cr,
                    GRADE_MSE_KEY: ms_error,
                    GRADE_H1E_KEY: h1_error,
                }

    with open(SCORE_JSON, 'w') as json_file:
        json.dump(scores, json_file, indent=2)
        print("Dumped score array to score.json")

    with open(DIFF_JSON, 'w') as json_file:
        json.dump(diff, json_file, indent=2)
        print("Dumped diff data to diff.json")
