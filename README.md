# mini-project-ecb21t13

#### Expects:

- Uncompressed PNG images in `reference`
- [ImageMagick](https://imagemagick.org/script/download.php) binary in `bin`
- Python libraries: Matplotlib, Pillow

```
├─ bin
│  ├─ magick.exe (If on Windows) 
│  └─ magick     (If on Linux)
│  
├─ reference
│  ├─ dark_scene
│  │  ├─ 1.png
│  │  └─ ...
│  ├─ shapes
│  │  ├─ circles.png
│  │  └─ ...
│  └─ ...
```

#### Usage:

To make compressed images for various format, run:
```bash
python3 main.py --compress
```

Output will be in `compressed`
```
├─ compressed
│  ├─ png
│  │  ├─ dark_scene%1_10.png
│  │  ├─ dark_scene%1_20.png
│  │  └─ ...
│  ├─ jpeg
│  │  ├─ dark_scene%1_10.jpeg
│  │  ├─ dark_scene%1_20.jpeg
│  │  └─ ...
│  └─ ...
```

To perform analysis on compressed images, run:
```bash
python3 main.py --analyze
```

Output will be in `data.json`
```
{
  "jpeg": {
    "dark-scene-1": {
      "10": {
        "size_ratio": 0.0176361406746537
        "gms_error": 0.8313982347987988
      },
      "20": {
        "size_ratio": 0.0214351615241386
        "gms_error": 0.4203742394398733
      },
...
```

To perform evaluation on `data.json`, run
```bash
python3 main.py --evaluate
```
This will accumulate scores for all quality settings of an image into an array. Output will be stored in `score.json`.

To clean all generated file, run:
```bash
./clean.sh
```
