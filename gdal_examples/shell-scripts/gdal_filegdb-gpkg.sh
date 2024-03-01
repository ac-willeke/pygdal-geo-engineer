#!/bin/bash
# execute permissions: chmod +x filename.sh
# run: ./filename.sh

# set variables
ROOT="/workspaces/py-linux-template/mnt/data"
OUT_EPSG=25832

# loop through folder and convert all *.gdb to *.gpkg files
for INPUT_FILE in $ROOT/*.gdb; do
  echo "Processing: $INPUT_FILE"
  OUTPUT_FILE="${INPUT_FILE%.gdb}_$OUT_EPSG.gpkg"

  # reproject and convert to gpkg using ogr2ogr
  ogr2ogr -f "GPKG" -t_srs EPSG:$OUT_EPSG $OUTPUT_FILE $INPUT_FILE

  # log to console
  echo "Input: $INPUT_FILE"
  echo "Process: convert to GPKG and reproject to EPSG:$OUT_EPSG"
  echo "Output: $OUTPUT_FILE."
done
