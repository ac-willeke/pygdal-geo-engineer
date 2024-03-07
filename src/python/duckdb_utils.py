import os
import duckdb


def load_tbl_to_duckdb(input_table, output_table, db_path, driver="parquet_scan"):
    """
    Load tables into duckdb.

    Parameters
    ----------
    input_table : str
        "file_name.xxx"
    output_table : str
        name of the output table "table_name
    db_path : str
        path to duckdb
    driver : str, optional
        driver of input table, by default "parquet_scan"
    """

    with duckdb.connect(database=db_path, read_only=False) as con:
        # load spatial extension
        con.install_extension("spatial")
        con.load_extension("spatial")

        # check if table exists
        table_exists = con.execute(
            f"SELECT name FROM sqlite_master WHERE type='table' AND name='{output_table}';"
        ).fetchone()
        if table_exists:
            print(f"Table {output_table} already exists. Skipping.")
            return

        # add table
        if os.path.exists(input_table):
            con.execute(
                f"""
                CREATE TABLE {output_table} AS 
                SELECT * 
                FROM {driver}('{input_table}')
                """
            )
            print(f"Loaded table: {output_table}")

            # get columns
            columns = (
                con.execute(f"PRAGMA table_info({output_table})")
                .fetch_df()["name"]
                .tolist()
            )

            print(f"Table columns:\n {columns}")

        else:
            print(f"File {input_table} does not exist. Skipping.")
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
