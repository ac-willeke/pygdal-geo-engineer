"""GDAL: Reclassify an attribute value based on a lookup table."""

import os
import pandas as pd
from osgeo import ogr


# variables
root = "/workspaces/py-linux-template/mnt/data"
in_gpkg = os.path.join(root, "bevaring_25833.gpkg")
layer_name = "org_ar_ar50_flate"
lookup_csv = os.path.join(root, "AR50_bonitet_lookup.csv")

# --- IMPORT GPKG --- #
# get the input layer (read/write)
ds = ogr.Open(in_gpkg, 1)
lyr = ds.GetLayerByName(layer_name)

# add a new field to the layer
new_field_name = "ar50_bonitet"
new_field_defn = ogr.FieldDefn(new_field_name, ogr.OFTInteger)

# if field not exists
if lyr.GetLayerDefn().GetFieldIndex(new_field_name) == -1:
    lyr.CreateField(new_field_defn)

# print the layer's schema
print("Layer schema:")
print("Name, Type, Width, Precision")
for field in lyr.schema:
    print(field.name, field.type, field.width, field.precision)

# --- RECLASSIFY ATTRIBUTE VALUES --- #

# import csv as df
lookup_df = pd.read_csv(lookup_csv)

# rename columns
lookup_df.rename(
    columns={
        "ARTYPE kode": "artype",
        "ARTRESLAG kode": "artreslag",
        "ARSKOGBON kode": "arskogbon",
        "ARJORDBR kode": "arjordbr",
        "Bonitet kode": "ar50_bonitet",
        "ARDYRKING kode": "ardyrking",
        "ARVEGET kode": "arveget",
    },
    inplace=True,
)
print(lookup_df.head())

lookup_dict = {}
for index, row in lookup_df.iterrows():

    # {(x,x,x,x,x): y}
    lookup_dict[
        (
            row["artype"],
            row["artreslag"],
            row["arskogbon"],
            row["arjordbr"],
            row["ardyrking"],
            row["arveget"],
        )
    ] = row["ar50_bonitet"]

print(lookup_dict)

# loop through the features and reclassify the attribute value "ar50_bonitet"
for feature in lyr:
    # get the attribute values
    artype = feature.GetField("artype")
    artreslag = feature.GetField("artreslag")
    arskogbon = feature.GetField("arskogbon")
    arjordbr = feature.GetField("arjordbr")
    ardyrking = feature.GetField("ardyrking")
    arveget = feature.GetField("arveget")

    key = (artype, artreslag, arskogbon, arjordbr, arveget)

    if key in lookup_dict:
        new_value = lookup_dict[key]
        feature.SetField("ar50_bonitet", int(new_value))
        lyr.SetFeature(feature)

ds = None
print("Done")
