#!/bin/bash
# execute permissions: chmod +x reproject.sh
# run: ./reproject.sh

# set variables
ROOT="/workspaces/py-linux-template/mnt/data"
INPUT_FILE="vern_25833.gpkg"
OUTPUT_FILE="vern_25832.gpkg"
DRIVER="GPKG"
OUT_EPSG=25832

# Reproject all layers in GPKG
ogr2ogr -f $DRIVER -t_srs EPSG:$OUT_EPSG "$ROOT/$OUTPUT_FILE" "$ROOT/$INPUT_FILE"

# log to console
echo "Input: $INPUT_FILE"
echo "Process: reproject to EPSG:$OUT_EPSG"
echo "Output: $OUTPUT_FILE."
