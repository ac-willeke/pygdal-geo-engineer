"""
Module for joining tables in a DuckDB database.
"""

import duckdb


def join_tables_create_new(
    db_path: str, tbl1: str, tbl2: str, id_field: str, new_tbl: str
) -> None:
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
