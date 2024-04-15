# project config

REF_DIR: str = "reference"
OUT_DIR: str = "compressed"
DIFF_DIR: str = "diff"

FORMATS: [str] = [
    "jpeg",
    "webp",
    "jxl",
    "png",
    # "bpg",
]

DATA_JSON: str = "data.json"
SCORE_JSON: str = "score.json"

QUALITY_SETTINGS: [int] = [
    10, 20, 30, 40, 50, 60, 70, 75,  80, 85, 90, 95, 97, 100
]


SIZE_RATIO_KEY: str = "size_ratio"
GRADE_GMSE_KEY: str = "gms_error"
