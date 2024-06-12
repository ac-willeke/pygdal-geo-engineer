#!/bin/bash
# generate_hillshade_cog
# Gonverts a DEM/DTM to a hillshade
# Compresses to JPEG and converts to COG
# Arguments:
#   $1: input raster file with elevation data
# Usage:
#   generate_hillshade_cog raster.tif 25833
generate_hillshade_cog() {
    local filename="${1%.*}"
    local epsg=${2:-25833}
    local HILLSHADE_TMP=$(mktemp .hillshade.XXXXXX.tif -p .)  

    gdaldem hillshade $1 $HILLSHADE_TMP
    gdal_translate $HILLSHADE_TMP $filename.hillshade.cog -ot Byte -a_srs EPSG:$epsg -of COG -scale -co BLOCKSIZE=512 -co OVERVIEW_RESAMPLING=BILINEAR -co COMPRESS=JPEG -co QUALITY=75 -co NUM_THREADS=6 -co BIGTIFF=YES
    rm $HILLSHADE_TMP
}

# generate_rgb_cog  
# resample ortofoto to $variable
# Compresses to DEFLATE and converts to COG
# Arguments:
#   $1: input raster file with RGB data
#   $2: resample value (optional)
#   $3: epsg (default: 3857)
# Usage:
#   generate_rgb_cog raster.tif 1 25833
generate_rgb_cog() {
    local filename="${1%.*}"
    local epsg=${3:-25833}
    local RGB_TMP=$(mktemp .rgb.XXXXXX.tif -p .)  

    if [ -z "$2" ]; then
        gdal_translate $1 $filename.cog -a_srs EPSG:$epsg -of COG -co BLOCKSIZE=512 -co OVERVIEW_RESAMPLING=BILINEAR -co COMPRESS=DEFLATE -co NUM_THREADS=6 -co BIGTIFF=YES
    else
        gdalwarp -tr $2 $2 -r bilinear $1 $RGB_TMP
        gdal_translate $RGB_TMP $filename.cog -a_srs EPSG:$epsg -of COG -co BLOCKSIZE=512 -co OVERVIEW_RESAMPLING=BILINEAR -co COMPRESS=DEFLATE -co NUM_THREADS=6 -co BIGTIFF=YES
    fi
    rm $RGB_TMP
}

# generate_singleband_cog
# Generates a COG from a GeoTIFF file
# Arguments:
#   $1: Path to input GeoTIFF file
# Usage: generate_cog /path/to/input.tif
generate_singleband_cog () {
    local MASK=$(mktemp .cog.XXXXXXX.tif -p .)
    local NORMALIZED=$(mktemp .cog.XXXXXXX.tif -p .)
    local RGBA=$(mktemp .cog.XXXXXXX.tif -p .)

    gdal_translate -co NUM_THREADS=ALL_CPUS -scale 1 4 255 255 $1 $MASK
    gdal_translate -co NUM_THREADS=ALL_CPUS -scale 1 4 0 255 $1 $NORMALIZED
    gdal_merge.py -separate -o $RGBA -of GTiff -co NUM_THREADS=ALL_CPUS $NORMALIZED $NORMALIZED $NORMALIZED $MASK
    gdal_translate $RGBA $1.cog -of COG -co NUM_THREADS=ALL_CPUS -co TARGET_SRS=EPSG:3857 -co ADD_ALPHA=NO -co COMPRESS=LZW -co LEVEL=9
    rm $MASK $NORMALIZED $RGBA
}

# set_color_relief
# Sets a color relief to the COG file 
# Arguments:
#   $1: Path to input COG file
#   $2: Path to txt file with color relief
#   $3: Path to output COG file
# Usage: generate_color_cog /path/to/input.cog /path/to/color-relief.txt /path/to/output.cog

set_color_relief () {
    local RGBA=$(mktemp .cog.XXXXXXX.tif -p .)

    gdaldem color-relief $1 $2 $RGBA -alpha
    gdal_translate $RGBA $1.cog -of COG -co TARGET_SRS=EPSG:3857 -co ADD_ALPHA=NO -co COMPRESS=LZW -co LEVEL=9
    rm $RGBA
}
