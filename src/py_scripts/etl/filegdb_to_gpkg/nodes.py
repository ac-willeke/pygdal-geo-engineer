import os

import fiona
import geopandas as gpd

# TODO add optional multithreading


def fc_to_gdf(filegdb_path):
    """Copies data from a FileGDB to a Geopackage.

    Args:
      filegdb_path: The path to the FileGDB.
      gpkg_path: The path to the Geopackage.
    """

    # check if file exits
    print(f"Path exists {os.path.exists(filegdb_path)}")
    gdb_name = os.path.basename(filegdb_path)

    # Open the FileGDB and Geopackage.
    layers = fiona.listlayers(filegdb_path)
    print(f"FileGDB <{gdb_name}> contains n={len(layers)} layers.")
    dict_gdf = {}
    for layer in layers:
        print(f"Adding {layer} to dict.")
        gdf = gpd.read_file(filegdb_path, layer=layer)[:5]
        dict_gdf[layer] = gdf
        # dict_gdf[layer] = gdf[["TREE_ID"]]
        break

    return dict_gdf


def gdf_to_gpkg(dict_gdf, gpkg_path, spatial_reference="EPSG"):
    if not os.path.exists(gpkg_path):
        from pygeopkg.core.geopkg import GeoPackage

        GeoPackage.create(gpkg_path, flavor=spatial_reference)
        gpkg_name = os.path.basename(gpkg_path)
        print(f"Created GPKG: {gpkg_name}")

    for key, gdf in dict_gdf:
        gdf.to_file(gpkg_path, layer=gdf, driver="GPKG")
    return


if __name__ == "__main__":
    filegdb_path = input("path/to/gdb:")
    gpkg_path = input("path/to/gpkg:")
    dict_gdf = fc_to_gdf(filegdb_path)
    gdf_to_gpkg(dict_gdf, gpkg_path)
