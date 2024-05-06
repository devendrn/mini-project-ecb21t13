#!/bin/bash

if [ ! -f venv/bin/activate ]; then
  echo "Creating virtual env"
  python3 -m venv venv
  source venv/bin/activate

  echo "Installing dependencies"
  pip3 install numpy matplotlib pillow
fi

if [ ! -f venv/bin/magick ]; then
  echo "Downloading Magick Appimage"
  wget -P venv/bin https://imagemagick.org/archive/binaries/magick
  chmod +x venv/bin/magick
fi


if [ ! -f visualize/chart.umd.min.js ]; then
  echo "Downloading Chart.js"
  wget -P visualize https://cdn.jsdelivr.net/npm/chart.js@4.4.2/dist/chart.umd.min.js
fi
