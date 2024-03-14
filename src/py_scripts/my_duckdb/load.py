"""
Module for importing data into DuckDB
"""

import os
import geopandas as gpd
import duckdb


def load_gpkg_layers(db_path, gpkg_path, layer_name):
    # Convert the geopackage layer to a Parquet file

    # basename of db_path
    db_basename = os.path.basename(db_path)

    # create parquet folder if it does not exist
    parquet_folder = os.path.join(os.path.dirname(db_path), "parquet")
    if not os.path.exists(parquet_folder):
        os.makedirs(parquet_folder)

    parquet_path = os.path.join(parquet_folder, f"{layer_name}.parquet")
    gdf = gpd.read_file(gpkg_path, layer=layer_name)
    # if parquet does not exist, create it
    if not os.path.exists(parquet_path):
        gdf.to_parquet(parquet_path)

    with duckdb.connect(database=db_path, read_only=False) as con:
        # load spatial extension
        con.install_extension("spatial")
        con.load_extension("spatial")

        # check if table exists
        table_exists = con.sql(
            f"SELECT name FROM sqlite_master WHERE type='table' AND name='{layer_name}';"
        ).fetchone()
        if table_exists:
            print(f"Table {layer_name} already exists in DuckDB database. Skipping.")
            return

        # add table
        if os.path.exists(parquet_path):
            con.sql(
                f"""
                CREATE TABLE {layer_name} AS 
                SELECT * 
                FROM parquet_scan('{parquet_path}')
                """
            )
            print(f"Loaded table: {layer_name}")

        else:
            print(f"File {parquet_path} does not exist. Skipping.")
    return
