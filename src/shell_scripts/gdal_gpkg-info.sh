#!/bin/bash
# execute permissions: chmod +x reproject.sh
# run: ./reproject.sh

# set variables
DATA_PATH=$1          # "path/to/file"
INPUT_FILE=$2   # "input.gpkg"
BASE_INPUT_FILE=$(basename $INPUT_FILE .gpkg)  
LOG_FILE="log/gdal_gpkg-info.log"
METADATA_FILE="$DATA_PATH/metadata_$BASE_INPUT_FILE.txt"
DRIVER="GPKG"



# Log info
echo "Script execution started at $(date)" > "$LOG_FILE"
echo "Input file: $INPUT_FILE" > $LOG_FILE
echo "Driver: $DRIVER" >> $LOG_FILE

# print file info to metadata file
ogrinfo -al -so "$DATA_PATH/$INPUT_FILE">> $METADATA_FILE

# Get a list of all layers in the GeoPackage
# Ensure that åøæ are readable by setting LOCALE to UTF-8
LAYER_NAMES=$(ogrinfo -al -so "$DATA_PATH/$INPUT_FILE" | grep -oP 'Layer name: \K[^\t]+')
echo "Layers: $LAYER_NAMES" >> $LOG_FILE


# GET "PROJCRS" info for each layer
for LAYER in $LAYER_NAMES; do
    echo "Layer: $LAYER" >> $LOG_FILE
    echo "Feature count: $(ogrinfo -al -so "$DATA_PATH/$INPUT_FILE" $LAYER | grep -oP 'Feature Count: \K\w+')" >> $LOG_FILE
    echo "CRS: $(ogrinfo -al -so "$DATA_PATH/$INPUT_FILE" $LAYER | grep -oP 'PROJCRS\[\K[^,]*')" >> $LOG_FILE
done

# Log script execution end time
echo "Script execution ended at $(date)" >> "$LOG_FILE"

# log to console
echo "Input: $INPUT_FILE"
echo "Process: logging info and writing metadata"
echo "Logfile: $LOG_FILE"
echo "Metadata: $METADATA_FILE"
