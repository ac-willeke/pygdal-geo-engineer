"""
Module for geometry operations.
"""

import duckdb


def group_to_multipolygon(db_path, input_table, output_table, id_field):
    try:
        with duckdb.connect(database=db_path, read_only=False) as conn:
            # spatial extension
            conn.execute("INSTALL spatial;")
            conn.execute("LOAD spatial;")

            conn.execute(
                f"""
                CREATE TABLE {output_table} AS
                SELECT 
                    {id_field},
                    ST_Union_Agg(geom) as geom
                FROM 
                    {input_table}
                GROUP BY 
                    {id_field};
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
            conn.execute(
                f"""
                CREATE TABLE {output_table} AS
                SELECT 
                    *,
                    ST_MakeValid(geom) as clean_geom
                FROM 
                    {input_table}
                WHERE ST_GeometryType(geom) NOT IN ('POINT', 'LINESTRING');
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
