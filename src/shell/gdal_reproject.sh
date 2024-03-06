#!/bin/bash
# execute permissions: chmod +x reproject.sh
# run: ./reproject.sh

# set variables
DATA_PATH=$1
INPUT_FILE=$2   # "vern_25833.gpkg"
OUTPUT_FILE=$3  # "vern_25832.gpkg"
DRIVER="GPKG"
OUT_EPSG=$4     # 25832

# Reproject all layers in GPKG
ogr2ogr -f $DRIVER -t_srs EPSG:$OUT_EPSG "$DATA_PATH/$OUTPUT_FILE" "$ROOT/$INPUT_FILE"

# log to console
echo "Input: $INPUT_FILE"
echo "Process: reproject to EPSG:$OUT_EPSG"
echo "Output: $OUTPUT_FILE."
