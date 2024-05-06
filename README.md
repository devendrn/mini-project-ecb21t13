# mini-project-ecb21t13

## Setup

Run the setup script. This will set up a python3 venv, download magick binary, and install the necessary pip packages.
```
./setup.sh
```

Activate the venv to use the tool.
```
source venv/bin/activate
```

## Prerequisites:

- Uncompressed PNG images in `reference`

```
├─ reference
│  ├─ dark_scene
│  │  ├─ 1.png
│  │  └─ ...
│  ├─ shapes
│  │  ├─ circles.png
│  │  └─ ...
│  └─ ...
```

Strip these images before using the tool:
```
./strip_ref.sh
```

## Tool usage:

Commands need to be executed in sequential order. The two main phases in order are are compression, and analysis.

### Compression

To make compressed images for various formats, run:
```bash
python3 tool compress
```

The output will be in `compressed`
```yaml
├─ compressed
│  ├─ png
│  │  ├─ dark_scene_-_1_-_10.png
│  │  ├─ dark_scene_-_1_-_20.png
│  │  └─ ...
│  ├─ jpeg
│  │  ├─ dark_scene_-_1_-_10.jpeg
│  │  ├─ dark_scene_-_1_-_20.jpeg
│  │  └─ ...
│  └─ ...
```

If images were already compressed, it will skip and continue where it left on last run. Run `./clean.sh` to clear these images and start over.

### Analysis

To perform analysis on compressed images, run:
```bash
python3 tool analyze
```

Data output will be in `data.json`.
```json
{
  "jpeg": {
    "dark_scene": {
      "1": {
        "10": {
          "size_ratio": 0.09380421791263446,
          "h1_error": 17.111138343811035,
          "ms_error": 15.138230323791504
        },
        "20": {
          "size_ratio": 0.10325018313606045,
          "h1_error": 6.652371406555176,
          "ms_error": 4.37493896484375
        },
```

Diff outputs will be stored in `diff` directory.

To pack `data.json` for plotting, run:
```bash
python3 tool score
```
This will accumulate scores for all quality settings of an image into an array. The output will be stored in `score.json`.

### Clean

To clean all generated files, run:
```bash
./clean.sh
```

## Visualization

Data from `score.json` is visualized through HTML, with the help of `chart.js` library. 
```
cd visualize
python3 -m http.server
```
