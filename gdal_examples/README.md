# Example scripts for using GDAL

## Data
Norwegian nature protection areas are used as an example dataset. The data
can be downloaded from
[Miljødirektoratet Kartkatalog](https://kartkatalog.miljodirektoratet.no/Dataset/Details/0).

## Shell-scripts

Table of scripts and their purposes:

| Script | Task |
| ------ | ---- |
| `gdal_gdb-gpkg.sh` | Convert a FileGDB to GPKG. |
| `gdal_gpkg-info.sh` | Log information about a GPKG to file. |
| `gdal_reproject.sh` | Reproject a GPKG to a new CRS. |

## Python scripts (with gdal bindings)

Table of scripts and their purposes:

| Script | Task |
| ------ | ---- |
| `gdal_attribute-lookup.py` | Reclassify an attribute value based on a lookup table. |
