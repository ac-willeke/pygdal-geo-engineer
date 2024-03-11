import os
import duckdb
import geopandas as gpd
from typing import List, Union



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

def remove_database(db_path):
    if os.path.exists(db_path):
        os.remove(db_path)
    else:
        print(f"The file {db_path} does not exist")
    return

def remove_table(db_path, table_name):
    with duckdb.connect(database=db_path, read_only=False) as con:
    
        # if the table exists, drop it
        con.sql(f"DROP TABLE {table_name}")
    return

def field_exists(db_path, table_name, field_name):
    with duckdb.connect(database=db_path, read_only=False) as con:
        result = con.execute(f"PRAGMA table_info({table_name})").fetchdf()
        return field_name in result['name'].values

def remove_field(db_path, table_name, field_name):
    with duckdb.connect(database=db_path, read_only=False) as con:
        
        # if the field exists, drop it
        if field_exists(db_path, table_name, field_name):
            con.sql(f"ALTER TABLE {table_name} DROP COLUMN {field_name}")
    return

def print_duckdb_info(db_path):
    with duckdb.connect(database=db_path, read_only=False) as con:
        # load spatial extension
        con.install_extension("spatial")
        con.load_extension("spatial")

        # Get table names
        tables = con.sql(
            "SELECT name FROM sqlite_master WHERE type='table';"
        ).fetchall()
        print("Tables:", tables)
        
    return

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
            conn.sql("INSTALL spatial;")
            conn.sql("LOAD spatial;")
            
            
            # Create a temp table with the sum of the overlapping areas
            conn.sql(f"""
                CREATE TEMPORARY TABLE tbl_sum_ar50 AS
                SELECT
                    study_area.{id},
                    SUM( ST_Area( ST_Intersection( study_area.geom, ar50_overlap.geom ) ) ) as sum
                FROM
                    {tbl_study_area} as study_area,
                    {tbl_ar50} as ar50_overlap
                WHERE
                    ar50_overlap.{ar50_field} IN ({area_class_str}) AND
                    ST_Intersects( study_area.geom, ar50_overlap.geom )
                GROUP BY study_area.{id}
            """)
            
            ## add the new field to the study area table
            conn.sql(f"""
                ALTER TABLE {tbl_study_area}
                ADD COLUMN {new_field} REAL
            """)

            # Update the field in the original table (study area) with the calculated sums 
            # of overlap with the AR50 area class
            conn.sql(f"""
                UPDATE {tbl_study_area} as study_area
                SET {new_field} = tmp_ar50.sum
                FROM tbl_sum_ar50 as tmp_ar50
                WHERE study_area.{id} = tmp_ar50.{id}
            """)
    except Exception as e:
        print(f"An error occurred: {e}")
    
def sum_area_cols(db_path: str, tbl_name: str, id: str, area_fields: List[str], new_field: str) -> None:
    """ 
    Calculate the sum of areas for a list of area fields, and store the result in a new field.
    
    Args:
        db_path (str): Path to the database.
        tbl_name (str): Name of the table.
        id (str): ID field name.
        area_fields (List[str]): List of area fields.
        new_field (str): Name of the new field to store the result.
    """
    
    try: 
        with duckdb.connect(database=db_path, read_only=False) as conn:
            # spatial extension
            conn.sql("INSTALL spatial;")
            conn.sql("LOAD spatial;")
            
            # Create a temp table with the sum of the areas
            conn.sql(f"""
                CREATE TEMPORARY TABLE tbl_sum_areas AS
                SELECT
                    {id},
                    {', '.join(area_fields)},
                    {'+'.join(area_fields)} as sum
                FROM
                    {tbl_name}
            """)
            
            ## add the new field to the study area table
            conn.sql(f"""
                ALTER TABLE {tbl_name}
                ADD COLUMN {new_field} REAL
            """)

            # Update the field in the original table with the sum of the areas
            conn.sql(f"""
                UPDATE {tbl_name} as study_area
                SET {new_field} = tmp_areas.sum
                FROM tbl_sum_areas as tmp_areas
                WHERE study_area.{id} = tmp_areas.{id}
            """)
    except Exception as e:
        print(f"An error occurred: {e}")
        
def geom_area(db_path: str, tbl_name: str, geom_field: str, area_field: str) -> None:
    """
    Calculate the area of the geometry field and store the result in a new field.

    Args:
        db_path (str): Path to the database.
        tbl_name (str): Name of the table.
        geom_field (str): Name of the geometry field.
        new_field (str): Name of the new field to store the result.
    """
    
    try: 
        with duckdb.connect(database=db_path, read_only=False) as conn:
            # spatial extension
            conn.sql("INSTALL spatial;")
            conn.sql("LOAD spatial;")
            
            # add the area field to the study area table
            conn.sql(f"""
                ALTER TABLE {tbl_name}
                ADD COLUMN {area_field} REAL
            """)

            # calculate the area    
            conn.sql(f"""
                UPDATE {tbl_name} as study_area
                SET {area_field} = ST_Area({geom_field})
            """)
    except Exception as e:
        print(f"An error occurred: {e}")

def area_difference(db_path: str, tbl_name: str, field_a: str, field_b: str, area_diff_field: str) -> None:
    """
    Calculate the area difference between two area fields and store the result in a new field.
    
    Args:
        db_path (str): Path to the database.
        tbl_name (str): Name of the table.
        field_a (str): Name of the first area field.
        field_b (str): Name of the second area field.
        area_diff_field (str): Name of the new field to store the result.
    """
    
    try: 
        with duckdb.connect(database=db_path, read_only=False) as conn:
            # spatial extension
            conn.sql("INSTALL spatial;")
            conn.sql("LOAD spatial;")
            
            # add the area field to the study area table
            conn.sql(f"""
                ALTER TABLE {tbl_name}
                ADD COLUMN {area_diff_field} REAL
            """)

            # calculate the area difference    
            conn.sql(f"""
                UPDATE {tbl_name} as study_area
                SET {area_diff_field} = {field_a} - {field_b}
            """)
    except Exception as e:
        print(f"An error occurred: {e}")       
        
def blob_to_geom(db_path, tbl_name, blob_field, geom_field):
    """ Convert a BLOB field to a geometry field.

    Args:
        db_path (str): Path to the database.
        tbl_name (str): Name of the table.
        blob_field (str): Name of the BLOB field.
        geom_field (str): Name of the geometry field.
    """ 
    try:
        with duckdb.connect(database=db_path, read_only=False) as conn:
            # spatial extension
            conn.sql("INSTALL spatial;")
            conn.sql("LOAD spatial;")

            # Create a tmp table with the geometry field
            # duckdb does not support direct updating of columns
            conn.sql(f"""
                CREATE TABLE {tbl_name}_tmp AS 
                SELECT *, ST_GeomFromWKB({blob_field}) AS {geom_field}
                FROM {tbl_name}
            """)
            
            # drop the blob field
            conn.sql(f"""
                ALTER TABLE {tbl_name}_tmp
                DROP COLUMN {blob_field}
            """
            )
            
            # drop the original table
            conn.sql(f"DROP TABLE {tbl_name}")
            
            # rename the tmp table
            conn.sql(f"ALTER TABLE {tbl_name}_tmp RENAME TO {tbl_name}")
            
            return 
            
    except Exception as e:
        print(f"An error occurred: {e}")
        
        
        
