#!/bin/bash
# execute permissions: chmod +x reproject.sh
# run: ./reproject.sh

# set variables
#DATA_PATH=$1          # "path/to/file"
INPUT_FILE=$2      # "input.gpkg"
OUTPUT_FILE=$1     # "output.gpkg"
LAYER=$3            # "layer_name"
OUT_EPSG=$4        # "EPSG:25833"

# check if GeoPackage exists
if [ ! -f "$OUTPUT_FILE" ]; then
    # if GeoPackage does not exist, create new GeoPackage
    ogr2ogr -f "GPKG" $OUTPUT_FILE $INPUT_FILE -nln $LAYER -t_srs $OUT_EPSG
else
    # if GeoPackage exists, append layer to GeoPackage
    ogr2ogr -update -append $OUTPUT_FILE $INPUT_FILE -nln $LAYER -t_srs $OUT_EPSG
fi

# print all layers in the GeoPackage
ogrinfo -al -so $INPUT_FILE

# log to console
echo "Input: $INPUT_FILE"
echo "Layer: $LAYER"
echo "Output: $OUTPUT_FILE"