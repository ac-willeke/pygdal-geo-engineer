from src.filegdb_to_gpkg.nodes import fc_to_gdf, gdf_to_gpkg


def pipeline(filegdb_path, gpkg_path):
    dict_gdf = fc_to_gdf(filegdb_path)
    gdf_to_gpkg(dict_gdf, gpkg_path)

    return


if __name__ == "__main__":
    filegdb_path = input("path/to/gdb:")
    gpkg_path = input("path/to/gpkg:")
    pipeline(filegdb_path, gpkg_path)
