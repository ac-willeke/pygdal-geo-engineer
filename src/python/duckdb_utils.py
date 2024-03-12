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
        return field_name in result["name"].values


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

def bioklima_area_class(
    db_path: str,
    tbl_study_area: str,
    id: str,
    tbl_bioklima: str,
    bioklima_field: str,
    area_class: Union[str, List[str]],
    new_field: str,
) -> None:
    """Calculate the area of overlap between the study area and
    the Bioklima area class. The area of overlap is calculated for each study area polygon defined
    by the id field and area class. The result is stored in the new field.

    Args:
        db_path (str): Path to the database.
        tbl_study_area (str): Name of the study area table.
        id (str): ID field name.
        tbl_bioklima (str): Name of the Bioklima table.
        bioklima_field (str): Bioklima field name.
        area_class (Union[str, List[str]]): Area class or list of area classes.
        new_field (str): Name of the new field to store the result.
    """
    # convert list to string
    area_class_str = (
        ", ".join(f"'{item}'" for item in area_class)
        if isinstance(area_class, list)
        else f"'{area_class}'"
    )

    try:
        with duckdb.connect(database=db_path, read_only=False) as conn:
            # spatial extension
            conn.sql("INSTALL spatial;")
            conn.sql("LOAD spatial;")

            # Create a temp table with the sum of the overlapping areas
            conn.sql(
                f"""
                CREATE TEMPORARY TABLE tbl_sum_bioklima AS
                SELECT
                    study_area.{id},
                    SUM( ST_Area( ST_Intersection( study_area.geom, bioklima_overlap.geom ) ) ) as sum
                FROM
                    {tbl_study_area} as study_area,
                    {tbl_bioklima} as bioklima_overlap
                WHERE
                    bioklima_overlap.{bioklima_field} IN ({area_class_str}) AND
                    ST_Intersects( study_area.geom, bioklima_overlap.geom )
                GROUP BY study_area.{id}
            """
            )

            ## add the new field to the study area table
            conn.sql(
                f"""
                ALTER TABLE {tbl_study_area}
                ADD COLUMN {new_field} REAL
            """
            )

            # Update the field in the original table (study area) with the calculated sums
            # of overlap with the Bioklima area class
            conn.sql(
                f"""
                UPDATE {tbl_study_area} as study_area
                SET {new_field} = tmp_bioklima.sum
                FROM tbl_sum_bioklima as tmp_bioklima
                WHERE study_area.{id} = tmp_bioklima.{id}
            """
            )
    except Exception as e:
        print(f"An error occurred: {e}")

def ar50_area_class(
    db_path: str,
    tbl_study_area: str,
    id: str,
    tbl_ar50: str,
    ar50_field: str,
    area_class: Union[int, List[int]],
    new_field: str,
) -> None:
    """Calculate the area of overlap between the study area (e.g. protected areas) and
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
    area_class_str = (
        ", ".join(map(str, area_class))
        if isinstance(area_class, list)
        else str(area_class)
    )

    try:
        with duckdb.connect(database=db_path, read_only=False) as conn:
            # spatial extension
            conn.sql("INSTALL spatial;")
            conn.sql("LOAD spatial;")

            # Create a temp table with the sum of the overlapping areas
            conn.sql(
                f"""
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
            """
            )

            ## add the new field to the study area table
            conn.sql(
                f"""
                ALTER TABLE {tbl_study_area}
                ADD COLUMN {new_field} REAL
            """
            )

            # Update the field in the original table (study area) with the calculated sums
            # of overlap with the AR50 area class
            conn.sql(
                f"""
                UPDATE {tbl_study_area} as study_area
                SET {new_field} = tmp_ar50.sum
                FROM tbl_sum_ar50 as tmp_ar50
                WHERE study_area.{id} = tmp_ar50.{id}
            """
            )
    except Exception as e:
        print(f"An error occurred: {e}")


def sum_area_cols(
    db_path: str, tbl_name: str, id: str, area_fields: List[str], new_field: str
) -> None:
    """
    Calculate the sum of areas for a list of area fields, and store the result in a new field.
    NaN values are set to "0" before calculating the sum.

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
            conn.sql(
                f"""
                CREATE TEMPORARY TABLE tbl_sum_areas AS
                SELECT
                    {id},
                    {', '.join(area_fields)},
                    {'+'.join([f'COALESCE({field}, 0)' for field in area_fields])} as sum
                FROM
                    {tbl_name}
            """
            )

            ## add the new field to the study area table
            conn.sql(
                f"""
                ALTER TABLE {tbl_name}
                ADD COLUMN {new_field} REAL
            """
            )

            # Update the field in the original table with the sum of the areas
            conn.sql(
                f"""
                UPDATE {tbl_name} as study_area
                SET {new_field} = tmp_areas.sum
                FROM tbl_sum_areas as tmp_areas
                WHERE study_area.{id} = tmp_areas.{id}
            """
            )
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
            conn.sql(
                f"""
                ALTER TABLE {tbl_name}
                ADD COLUMN {area_field} REAL
            """
            )

            # calculate the area
            conn.sql(
                f"""
                UPDATE {tbl_name} as study_area
                SET {area_field} = ST_Area({geom_field})
            """
            )
    except Exception as e:
        print(f"An error occurred: {e}")

def geom_area_byID(db_path: str, tbl_name: str, id_field: str, geom_field: str, area_field: str) -> None:
    """
    Calculate the sum of the areas of the geometries with the same ID and store the result in a new field.

    Args:
        db_path (str): Path to the database.
        tbl_name (str): Name of the table.
        geom_field (str): Name of the geometry field.
        area_field (str): Name of the new field to store the result.
        id_field (str): Name of the ID field to group by.
    """

    try:
        with duckdb.connect(database=db_path, read_only=False) as conn:
            # spatial extension
            conn.sql("INSTALL spatial;")
            conn.sql("LOAD spatial;")

            # add the area field to the table
            conn.sql(
                f"""
                ALTER TABLE {tbl_name}
                ADD COLUMN {area_field} REAL
            """
            )

            # calculate the sum of the areas for each ID
            conn.sql(
                f"""
                UPDATE {tbl_name} as study_area
                SET {area_field} = subquery.area
                FROM (
                    SELECT {id_field}, SUM(ST_Area({geom_field})) as area
                    FROM {tbl_name}
                    GROUP BY {id_field}
                ) as subquery
                WHERE study_area.{id_field} = subquery.{id_field}
            """
            )
    except Exception as e:
        print(f"An error occurred: {e}")

def geom_peri(db_path: str, tbl_name: str, geom_field: str, peri_field: str) -> None:
    """
    Calculate the perimeter of the geometry field and store the result in a new field.

    Args:
        db_path (str): Path to the database.
        tbl_name (str): Name of the table.
        geom_field (str): Name of the geometry field.
        peri_field (str): Name of the new field to store the result.
    """

    try:
        with duckdb.connect(database=db_path, read_only=False) as conn:
            # spatial extension
            conn.sql("INSTALL spatial;")
            conn.sql("LOAD spatial;")

            # add the area field to the study area table
            conn.sql(
                f"""
                ALTER TABLE {tbl_name}
                ADD COLUMN {peri_field} REAL
            """
            )

            # calculate the perimeter
            conn.sql(
                f"""
                UPDATE {tbl_name} as study_area
                SET {peri_field} = ST_Perimeter({geom_field})
            """
            )
    except Exception as e:
        print(f"An error occurred: {e}")


def geom_peri_byID(db_path: str, tbl_name: str, id_field: str, geom_field: str, peri_field: str) -> None:
    """
    Calculate the sum of the perimeters of the geometries with the same ID and store the result in a new field.

    Args:
        db_path (str): Path to the database.
        tbl_name (str): Name of the table.
        geom_field (str): Name of the geometry field.
        peri_field (str): Name of the new field to store the result.
        id_field (str): Name of the ID field to group by.
    """

    try:
        with duckdb.connect(database=db_path, read_only=False) as conn:
            # spatial extension
            conn.sql("INSTALL spatial;")
            conn.sql("LOAD spatial;")

            # add the perimeter field to the table
            conn.sql(
                f"""
                ALTER TABLE {tbl_name}
                ADD COLUMN {peri_field} REAL
            """
            )

            # calculate the sum of the perimeters for each ID
            conn.sql(
                f"""
                UPDATE {tbl_name} as study_area
                SET {peri_field} = subquery.perimeter
                FROM (
                    SELECT {id_field}, SUM(ST_Perimeter({geom_field})) as perimeter
                    FROM {tbl_name}
                    GROUP BY {id_field}
                ) as subquery
                WHERE study_area.{id_field} = subquery.{id_field}
            """
            )
    except Exception as e:
        print(f"An error occurred: {e}")

def geom_index(db_path: str, tbl_name: str, geom_field: str, index_field: str) -> None:
    """Calculate the shape index and store in a new field. 
    Shape index = perimeter / (2 * pi * sqrt(area/pi))
    
    The shape index is a measure of how compact the shape is compared to a circle with the same area. 
    The shape index is a value between 0 and 1, where 0 is a perfect circle and 1 is a long and narrow shape.

    Args:
        db_path (str): Path to the database.
        tbl_name (str): Name of the table.
        geom_field (str): Name of the geometry field.
        index_field (str): Name of the new field to store the result.
    
    Returns:
        Shape index (float): 
        - SI = 1, shape is a perfect circle
        - SI > 1, shape is less compact than a circle
        - SI < 1, is not possible for a shape to have a shape index less than 1
    """
    
    try:
        with duckdb.connect(database=db_path, read_only=False) as conn:
            # spatial extension
            conn.sql("INSTALL spatial;")
            conn.sql("LOAD spatial;")

            # add the index field to the study area table
            conn.sql(
                f"""
                ALTER TABLE {tbl_name}
                ADD COLUMN {index_field} REAL
            """
            )

            # calculate the shape index
            conn.sql(
                f"""
                UPDATE {tbl_name} as study_area
                SET {index_field} = ST_Perimeter({geom_field}) / (2 * PI() * sqrt(ST_Area({geom_field}) / PI()))
                """
            )
            
    except Exception as e:
        print(f"An error occurred: {e}")

def geom_index_byID(db_path: str, tbl_name: str, id_field: str, geom_field: str, index_field: str) -> None:
    """Calculate the shape index and store in a new field. 
    Shape index = perimeter / (2 * PI() * sqrt(area/pi))
    
    The shape index is a measure of how compact the shape is compared to a circle with the same area. 
    The shape index is a value between 0 and 1, where 0 is a perfect circle and 1 is a long and narrow shape.

    Args:
        db_path (str): Path to the database.
        tbl_name (str): Name of the table.
        geom_field (str): Name of the geometry field.
        index_field (str): Name of the new field to store the result.
        id_field (str): Name of the id field to group by.
    
    Returns:
        Shape index (float): 
        - SI = 1, shape is a perfect circle
        - SI > 1, shape is less compact than a circle
        - SI < 1, is not possible for a shape to have a shape index less than 1
    """
    
    try:
        with duckdb.connect(database=db_path, read_only=False) as conn:
            # spatial extension
            conn.sql("INSTALL spatial;")
            conn.sql("LOAD spatial;")

            # add the index field to the study area table
            conn.sql(
                f"""
                ALTER TABLE {tbl_name}
                ADD COLUMN {index_field} REAL
            """
            )

            # calculate the shape index
            conn.sql(
                f"""
                UPDATE {tbl_name} as study_area
                SET {index_field} = subquery.perimeter / (2 * PI() * sqrt(subquery.area / PI()))
                FROM (
                    SELECT {id_field}, SUM(ST_Perimeter({geom_field})) as perimeter, SUM(ST_Area({geom_field})) as area
                    FROM {tbl_name}
                    GROUP BY {id_field}
                ) as subquery
                WHERE study_area.{id_field} = subquery.{id_field}
                """
            )
            
    except Exception as e:
        print(f"An error occurred: {e}")

def area_difference(
    db_path: str, tbl_name: str, field_a: str, field_b: str, area_diff_field: str
) -> None:
    """
    Calculate the area difference between two area fields and store the result in a new field.
    Null values are set to 0 before calculating the difference.

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
            conn.sql(
                f"""
                ALTER TABLE {tbl_name}
                ADD COLUMN {area_diff_field} REAL
            """
            )

            # calculate the area difference
            conn.sql(
                f"""
                UPDATE {tbl_name} as study_area
                SET {area_diff_field} = COALESCE({field_a}, 0) - COALESCE({field_b}, 0)
            """
            )
    except Exception as e:
        print(f"An error occurred: {e}")


def blob_to_geom(db_path, tbl_name, blob_field, geom_field):
    """Convert a BLOB field to a geometry field.

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
            conn.sql(
                f"""
                CREATE TABLE {tbl_name}_tmp AS 
                SELECT *, ST_GeomFromWKB({blob_field}) AS {geom_field}
                FROM {tbl_name}
            """
            )

            # drop the blob field
            conn.sql(
                f"""
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

def split_by_polygon(db_path, tbl_study_area, id, tbl_ar50, group_field, group, output_tbl_a, output_tbl_b):
    try: 
        with duckdb.connect(database=db_path, read_only=False) as conn:
            # spatial extension
            conn.execute("INSTALL spatial;")
            conn.execute("LOAD spatial;")

            # extract the part of the study area that OVERLAPS with the AR50 area class X
            conn.execute(f"""
                CREATE TABLE {output_tbl_a} AS
                SELECT 
                    {id}, 
                    ST_Intersection(a.geom, b.geom) as geom
                FROM 
                    {tbl_ar50} a, {tbl_study_area} b
                WHERE a.{group_field} = {group} AND ST_Intersects(a.geom, b.geom);
            """)
            
            # extract the part of the study area that DOES NOT OVERLAP with the AR50 area class X
            conn.execute(f"""
                CREATE TABLE {output_tbl_b} AS
                SELECT 
                    {id}, 
                    ST_Difference(
                        b.geom,
                        a.geom
                    ) as geom
                FROM 
                    {tbl_ar50} a, {tbl_study_area} b
                WHERE a.{group_field} = {group} AND ST_Intersects(a.geom, b.geom);
            """)
    except Exception as e:
        print(f"An error occurred: {e}")
        
def join_tables_create_new(db_path: str, tbl1: str, tbl2: str, id_field: str, new_tbl: str) -> None:
    """
    Join two tables on a common ID field and create a new table from the result.

    Args:
        db_path (str): Path to the database.
        tbl1 (str): Name of the first table.
        tbl2 (str): Name of the second table.
        id_field (str): Name of the ID field to join on.
        new_tbl (str): Name of the new table to create.
    """

    try:
        with duckdb.connect(database=db_path, read_only=False) as conn:
            # join the tables and create a new table
            conn.sql(
                f"""
                CREATE TABLE {new_tbl} AS
                SELECT *
                FROM {tbl1}
                FULL JOIN {tbl2}
                ON {tbl1}.{id_field} = {tbl2}.{id_field}
                """
            )
    except Exception as e:
        print(f"An error occurred: {e}")
        
def remove_duplicates(db_path: str, tbl_name: str, id_field: str) -> None:
    """
    Remove duplicate entries from a table based on a specific field.

    Args:
        db_path (str): Path to the database.
        tbl_name (str): Name of the table.
        id_field (str): Name of the field to check for duplicates.
    """

    try:
        with duckdb.connect(database=db_path, read_only=False) as conn:
            # create a temporary table with distinct records
            conn.sql(
                f"""
                CREATE TABLE temp_table AS
                SELECT DISTINCT *
                FROM {tbl_name}
                """
            )

            # delete all records from the original table
            conn.sql(
                f"""
                DELETE FROM {tbl_name}
                """
            )

            # insert the distinct records back into the original table
            conn.sql(
                f"""
                INSERT INTO {tbl_name}
                SELECT * FROM temp_table
                """
            )
            
            # drop the temporary table
            conn.sql(
                f"""
                DROP TABLE temp_table
                """
            )
    except Exception as e:
        print(f"An error occurred: {e}")
        

def delete_lines_points(db_path, input_table, output_table):
    try: 
        with duckdb.connect(database=db_path, read_only=False) as conn:
            # spatial extension
            conn.execute("INSTALL spatial;")
            conn.execute("LOAD spatial;")

            # Clean the geometry and remove points and lines
            conn.execute(f"""
                CREATE TABLE {output_table} AS
                SELECT 
                    *,
                    ST_MakeValid(geom) as clean_geom
                FROM 
                    {input_table}
                WHERE ST_GeometryType(geom) NOT IN ('POINT', 'LINESTRING');
            """)
    except Exception as e:
        print(f"An error occurred: {e}")