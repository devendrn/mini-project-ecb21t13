#!/bin/bash

MAGICK=bin/magick

for image in reference/*/*.png; do
  echo "Stripping $image"
  $MAGICK convert -strip $image $image
done
