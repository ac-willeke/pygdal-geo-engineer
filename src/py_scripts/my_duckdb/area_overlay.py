"""
Module for calculating the area of overlap between two spatial datasets.
"""

import duckdb
from typing import Union, List


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


def extract_overlap_geom(
    db_path, id, input_a, group_field, group, input_b, output_a, output_b
):
    try:
        with duckdb.connect(database=db_path, read_only=False) as conn:
            # spatial extension
            conn.execute("INSTALL spatial;")
            conn.execute("LOAD spatial;")

            # extract the part of the study area that OVERLAPS with the area class X
            conn.execute(
                f"""
                CREATE TABLE {output_a} AS
                SELECT 
                    b.{id}, 
                    ST_Intersection(a.geom, b.geom) as geom
                FROM 
                    {input_a} a, {input_b} b
                WHERE 
                    a.{group_field} = {group} AND ST_Intersects(a.geom, b.geom);
            """
            )

            # extract the part of the study area that OVERLAPS with the area class X
            conn.execute(
                f"""
                CREATE TABLE {output_b} AS
                SELECT 
                    b.{id}, 
                    ST_Intersection(a.geom, b.geom) as geom
                FROM 
                    {input_a} a, {input_b} b
                WHERE 
                    a.{group_field} != {group} AND ST_Intersects(a.geom, b.geom);
            """
            )

    except Exception as e:
        print(f"An error occurred: {e}")
