






#!/bin/bash
# execute permissions: chmod +x reproject.sh
# run: ./reproject.sh

# set variables
INPUT_FILE=$1     # "input.gpkg"
OUTPUT_FILE=$2
XMIN=$3
YMIN=$4
XMAX=$5
YMAX=$6
DRIVER="GPKG"


# Log info
echo "Script execution started at $(date)"
echo "Input file: $INPUT_FILE"
echo "Driver: $DRIVER"

# Get a list of all layers in the GeoPackage
# Ensure that åøæ are readable by setting LOCALE to UTF-8
LAYER_NAMES=$(ogrinfo -al -so $INPUT_FILE | grep -oP 'Layer name: \K[^\t]+')
echo "Layers: $LAYER_NAMES"
echo "Process: cutting layers by bounding box"

# loop trhough layers and cut by bounding box
for LAYER in $LAYER_NAMES; do
    echo "Layer: $LAYER"
    ogr2ogr -spat $XMIN $YMIN $XMAX $YMAX -append $OUTPUT_FILE $INPUT_FILE $LAYER
done

# Log script execution end time
echo "Script execution ended at $(date)"


