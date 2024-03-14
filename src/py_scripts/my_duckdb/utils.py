""" 
Module for common DuckDB operations.
"""

import os
import duckdb


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


def remove_database(db_path):
    if os.path.exists(db_path):
        os.remove(db_path)
    else:
        print(f"The file {db_path} does not exist")
    return


def remove_table(db_path, table_name):
    with duckdb.connect(database=db_path, read_only=False) as con:
        # if the table exists, drop it
        con.sql(f"DROP TABLE IF EXISTS {table_name}")
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
