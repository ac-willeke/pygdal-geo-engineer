import os
import pandas as pd


def create_lookup_dict(
    lookup_df,
    keys=("artype", "artreslag", "arskogbon", "arjordbr", "ardyrkning", "arveget"),
    value="ar50_bonitet",
):
    """
    Convert a lookup DF to a lookup DICT

    Parameters
    ----------
    lookup_df : pandas dataframe
        lookup table loaded into a dataframe
    keys : tuple, optional
        lookup key(s), by default ("artype", "artreslag", "arskogbon", "arjordbr", "ardyrkning", "arveget")
    value : str, optional
        lookup value, by default "ar50_bonitet"

    Returns
    -------
    dict:
        lookup_dict {keys:value}
    """

    lookup_dict = {}
    for index, row in lookup_df.iterrows():
        lookup_dict[
            (
                row[keys(1)],
                row[keys(2)],
                row[keys(3)],
                row[keys(4)],
                row[keys(5)],
                row[keys(6)],
            )
        ] = row[value]
    return lookup_dict


def lookup_value(
    lyr,
    lookup_dict,
    keys=("artype", "artreslag", "arskogbon", "arjordbr", "ardyrkning", "arveget"),
    value="ar50_bonitet",
):
    """
    Reclassify an attribute value using ogr lyr object
    and a lookup DICT.

    Parameters
    ----------
    lyr : ogr lyr object
        output from ogr_utils.import_gpkg
    lookup_dict : dictionairy
        lookup dict {keys:value}
    field_names : tuple
        tuple with field names
    """

    for feature, keys in lyr:

        key = (
            feature.GetField(keys(1)),
            feature.GetField(keys(2)),
            feature.GetField(keys(3)),
            feature.GetField(keys(4)),
            feature.GetField(keys(5)),
            feature.GetField(keys(6)),
        )
        if key in lookup_dict:
            new_value = lookup_dict[key]
            feature.SetField(value, int(new_value))
            lyr.SetFeature(feature)


def main():
    from ogr_utils import import_gpkg, print_layer_schema

    # Import GPKG lyr to ogr lyr-object
    in_gpkg = input("Enter filepath to GPKG:")
    layer_name = input("Enter layer name:")
    new_field_name = input("Enter new_field_name:")
    ds, lyr = import_gpkg(in_gpkg, layer_name, new_field_name)
    print_layer_schema(lyr)

    # import lookup CSV
    lookup_csv = input("Enter path to CSV file:")
    keys = input("Enter keys as tuple:")
    value = input("Enter value as 'str':")
    lookup_df = pd.read_csv(lookup_csv)

    lookup_dict = create_lookup_dict(lookup_df, keys=keys, value=value)

    # lookup value
    lookup_value(lyr, lookup_dict, keys=keys, value=value)

    # close ogr object
    ds = None
    print("Done")


if __name__ == "__main__":
    main()
