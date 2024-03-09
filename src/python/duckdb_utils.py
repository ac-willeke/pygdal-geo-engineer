import os
import duckdb
import geopandas as gpd


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
        table_exists = con.execute(
            f"SELECT name FROM sqlite_master WHERE type='table' AND name='{layer_name}';"
        ).fetchone()
        if table_exists:
            print(f"Table {layer_name} already exists in DuckDB database. Skipping.")
            return

        # add table
        if os.path.exists(parquet_path):
            con.execute(
                f"""
                CREATE TABLE {layer_name} AS 
                SELECT * 
                FROM parquet_scan('{parquet_path}')
                """
            )
            print(f"Loaded table: {layer_name}")

            # get columns
            columns = (
                con.execute(f"PRAGMA table_info({layer_name})")
                .fetch_df()["name"]
                .tolist()
            )

            print(f"Table columns:\n {columns}")

        else:
            print(f"File {parquet_path} does not exist. Skipping.")
    return

def remove_duckdb_database(db_path):
    if os.path.exists(db_path):
        os.remove(db_path)
    else:
        print(f"The file {db_path} does not exist")
    return


def print_duckdb_info(db_path):
    with duckdb.connect(database=db_path, read_only=False) as con:
        # load spatial extension
        con.install_extension("spatial")
        con.load_extension("spatial")

        # Get table names
        tables = con.execute(
            "SELECT name FROM sqlite_master WHERE type='table';"
        ).fetchall()
        print("Tables:", tables)
        

    return


def ar50_area_class2(db_path, tbl_study_area, id, tbl_ar50, ar50_field, area_class, new_field):
    """ Calculate the area of overlap between the study area (e.g. protected areas) and 
    the AR50 area class. The area of overlap is calculated for each study area polygon defined
    by the id field and area class. The result is stored in the new field.

    Args:
        db_path (_type_): _description_
        tbl_study_area (_type_): _description_
        id (_type_): _description_
        tbl_ar50 (_type_): _description_
        ar50_field (_type_): _description_
        area_class (_type_): _description_
        new_field (_type_): _description_
    """       
    conn = duckdb.connect(database=db_path, read_only=False)

    # Create a temp table with the sum of the overlapping areas
    conn.execute(f"""
        CREATE TEMPORARY TABLE tbl_sum_ar50 AS
        SELECT
            study_area.{id},
            SUM( ST_Area( ST_Intersection( study_area.geom, ar50_overlap.geom ) ) ) as sum
        FROM
            {tbl_study_area} as study_area,
            {tbl_ar50} as ar50_overlap
        WHERE
            overlapp.{ar50_field} = ANY ({area_class}) AND
            ST_Intersects( study_area.geom, ar50_overlap.geom )
        GROUP BY study_area.{id}
    """)

    # Update the field in the original table (study area) with the calculated sums 
    # of overlap with the AR50 area class
    conn.execute(f"""
        UPDATE {tbl_study_area} as study_area
        SET {new_field} = tmp_ar50.sum
        FROM tbl_sum_ar50 as tmp_ar50
        WHERE vern.{id} = tmp_ar50.{id}
    """)

    conn.close()

from typing import List, Union

def ar50_area_class(db_path: str, tbl_study_area: str, id: str, tbl_ar50: str, ar50_field: str, area_class: Union[int, List[int]], new_field: str) -> None:
    """ Calculate the area of overlap between the study area (e.g. protected areas) and 
    the AR50 area class. The area of overlap is calculated for each study area polygon defined
    by the id field and area class. The result is stored in the new field.

    Args:
        db_path (str): Path to the database.
        tbl_study_area (str): Name of the study area table.
        id (str): ID field name.
        tbl_ar50 (str): Name of the AR50 table.
        ar50_field (str): AR50 field name.
        area_class (Union[int, List[int]]): Area class or list of area classes.
        new_field (str): Name of the new field to store the result.
    """ 
    # convert int to string      
    area_class_str = ', '.join(map(str, area_class)) if isinstance(area_class, list) else str(area_class)

    try:
        with duckdb.connect(database=db_path, read_only=False) as conn:
            # spatial extension
            conn.execute("INSTALL spatial;")
            conn.execute("LOAD spatial;")
            
            
            # Create a temp table with the sum of the overlapping areas
            conn.execute(f"""
                CREATE TEMPORARY TABLE tbl_sum_ar50 AS
                SELECT
                    study_area.{id},
                    SUM( ST_Area( ST_Intersection( study_area.geometry, ar50_overlap.geometry ) ) ) as sum
                FROM
                    {tbl_study_area} as study_area,
                    {tbl_ar50} as ar50_overlap
                WHERE
                    ar50_overlap.{ar50_field} IN ({area_class_str}) AND
                    ST_Intersects( study_area.geometry, ar50_overlap.geometry )
                GROUP BY study_area.{id}
            """)

            # Update the field in the original table (study area) with the calculated sums 
            # of overlap with the AR50 area class
            conn.execute(f"""
                UPDATE {tbl_study_area} as study_area
                SET {new_field} = tmp_ar50.sum
                FROM tbl_sum_ar50 as tmp_ar50
                WHERE vern.{id} = tmp_ar50.{id}
            """)
    except Exception as e:
        print(f"An error occurred: {e}")