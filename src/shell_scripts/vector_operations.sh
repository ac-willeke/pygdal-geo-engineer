#!/bin/bash

# clip_vector
# Clips a vector layer to the extent of another vector layer
# Arguments:
#   $1: mask vector file
#   $2: mask layer name
#   $3: source vector file
#   $4: source layer name
#   $5: output vector file
#   $6: output layer name
# Usage:
#   clip_vector mask_vector.gpkg mask_layer source_vector.gpkg source_layer output_vector.gpkg output_layer
clip_vector() {
    local mask_vector=$1
    local mask_layer=$2
    local source_vector=$3
    local source_layer=$4
    local output_vector=$5
    local output_layer=$6

    # Run the ogr2ogr command with the -clipsrc and -nln options
    ogr2ogr -clipsrc $mask_vector -clipsrclayer $mask_layer -nln $output_layer -nlt "MULTIPOLYGON" $output_vector $source_vector $source_layer -f "GPKG"

    # Log info to console
    echo "Clipping complete"
    echo "Output vector: $output_vector"
}