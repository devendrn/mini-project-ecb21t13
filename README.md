# mini-project-ecb21t13

#### Expects:

- Uncompressed PNG images in `reference`
- [ImageMagick](https://imagemagick.org/script/download.php) binary in `bin`

```
├─ bin
│  ├─ magick.exe (If on Windows) 
│  └─ magick     (If on Linux)
├─ reference
│  ├─ dark-scene-1.png
│  ├─ dark-scene-2.png
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
│  │  ├─ dark-scene-1_10.png
│  │  ├─ dark-scene-1_20.png
│  │  └─ ...
│  ├─ jpeg
│  │  ├─ dark-scene-1_10.jpeg
│  │  ├─ dark-scene-1_20.jpeg
│  │  └─ ...
│  └─ ...
```

To perform analysis on compressed images, run:
```bash
python3 main.py --analyze
```
