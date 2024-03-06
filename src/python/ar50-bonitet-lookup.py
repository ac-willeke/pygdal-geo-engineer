import os
import pandas as pd

def create_lookup_dict(lookup_csv):
    lookup_df = pd.read_csv(lookup_csv)
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
    lookup_dict = {}
    for index, row in lookup_df.iterrows():
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
    return lookup_dict

def reclassify_attribute_values(lyr, lookup_dict):
    for feature in lyr:
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

def main():
    root = "/workspaces/py-linux-template/mnt/data"
    in_gpkg = os.path.join(root, "bevaring_25833.gpkg")
    layer_name = "org_ar_ar50_flate"
    lookup_csv = os.path.join(root, "AR50_bonitet_lookup.csv")
    new_field_name = "ar50_bonitet"
    ds, lyr = import_gpkg(in_gpkg, layer_name, new_field_name)
    print_layer_schema(lyr)
    lookup_dict = create_lookup_dict(lookup_csv)
    reclassify_attribute_values(lyr, lookup_dict)
    ds = None
    print("Done")

if __name__ == "__main__":
    main()