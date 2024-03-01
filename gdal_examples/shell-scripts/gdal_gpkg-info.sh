#!/bin/bash
# execute permissions: chmod +x reproject.sh
# run: ./reproject.sh

# set variables
LOG_FILE="reproject.log"
METADATA_FILE="metadata.txt"
ROOT="/workspaces/py-linux-template/mnt/data"
INPUT_FILE="bevaring_25833.gpkg"
DRIVER="GPKG"


# Log info
echo "Script execution started at $(date)" > "$LOG_FILE"
echo "Input file: $INPUT_FILE" > $LOG_FILE
echo "Driver: $DRIVER" >> $LOG_FILE

# print file info to metadata file
ogrinfo -al -so "$ROOT/$INPUT_FILE">> $METADATA_FILE


# Get a list of all layers in the GeoPackage
# Ensure that åøæ are readable by setting LOCALE to UTF-8
LAYER_NAMES=$(ogrinfo -al -so "$ROOT/$INPUT_FILE" | grep -oP 'Layer name: \K[^\t]+')
echo "Layers: $LAYER_NAMES" >> $LOG_FILE


# GET "PROJCRS" info for each layer
for LAYER in $LAYER_NAMES; do
    echo "Layer: $LAYER" >> $LOG_FILE
    echo "Feature count: $(ogrinfo -al -so "$ROOT/$INPUT_FILE" $LAYER | grep -oP 'Feature Count: \K\w+')" >> $LOG_FILE
    echo "CRS: $(ogrinfo -al -so "$ROOT/$INPUT_FILE" $LAYER | grep -oP 'PROJCRS\[\K[^,]*')" >> $LOG_FILE
done

# Log script execution end time
echo "Script execution ended at $(date)" >> "$LOG_FILE"

# log to console
echo "Input: $INPUT_FILE"
echo "Process: logging info and writing metadata"
echo "Logfile: $LOG_FILE"
echo "Metadata: $METADATA_FILE"
