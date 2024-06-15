"""
Module for calculating area variables, suca as area, perimeter, and shape index.
"""

import duckdb
import geopandas as gpd



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

            # add the area field to the study area table if not exists
            
            # remove col if exists
            if area_field in conn.table(tbl_name).columns:
                conn.sql(
                    f"""
                    ALTER TABLE {tbl_name}
                    DROP COLUMN {area_field}
                """
                )
            
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


def geom_area_byID(
    db_path: str, tbl_name: str, id_field: str, geom_field: str, area_field: str
) -> None:
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


def geom_peri_byID(
    db_path: str, tbl_name: str, id_field: str, geom_field: str, peri_field: str
) -> None:
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


def geom_index_byID(
    db_path: str, tbl_name: str, id_field: str, geom_field: str, index_field: str
) -> None:
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

# export duckdb table to gdf 
def export_toGDF(db_path: str, tbl_name: str) -> gpd.GeoDataFrame:
    """
    Export a table from a duckdb database to a geopandas dataframe.

    Args:
        db_path (str): Path to the database.
        tbl_name (str): Name of the table.
    """
    from shapely import wkt
    import geopandas as gpd

    try:
        with duckdb.connect(database=db_path, read_only=True) as conn:
            # spatial extension
            conn.sql("INSTALL spatial;")
            conn.sql("LOAD spatial;")
            
            # convert geom to correct format
            df = conn.execute(f"SELECT ST_AsText(geom) as geometry, * FROM {tbl_name}").fetchdf()
            df = df.drop(columns=["geom"])

            # convert to wkt 
            df['geometry'] = df['geometry'].apply(wkt.loads)

            # convert to gdf
            gdf = gpd.GeoDataFrame(df, geometry='geometry')
    except Exception as e:
        print(f"An error occurred: {e}")
        
    return gdf


if __name__ == "__main__":
    
    import os
    
    from py_scripts.my_duckdb import *

    from py_scripts.config import load_catalog
    
    # load paths from catalog
    catalog = load_catalog()
    data_path = catalog["project_data"]["filepath"]

    db_path = os.path.join(data_path, "tmp", "tmp.db")
    gpkg_path = os.path.join(data_path, "processed", "naturvern_per_region_clip.gpkg")
    csv_path = os.path.join(data_path, "processed", "CSV", "region_landareal")

    layer_name = "midt_area"

    # check if gpkg exists
    if not os.path.exists(gpkg_path):
        raise FileNotFoundError(f"File {gpkg_path} not found.")
    
    # gpkg to gdf 
    gdf = gpd.read_file(gpkg_path, layer=layer_name)
    print(gdf.head())
    # check if gdf contains duplicates in naturvernId col
    print(gdf['naturvernId'].duplicated().any())
    
    

    # load gpkg into duckdb
    # remove tabel
    remove_table(db_path, layer_name)
    load.load_gpkg_layers(db_path, gpkg_path, layer_name)
    
    blob_to_geom(
        db_path=db_path,
        tbl_name=layer_name,
        blob_field="geometry",
        geom_field="geom",   
    )
    
    # delete "geometry field"
    
    
    # calculate area
    geom_area(
        db_path=db_path, 
        tbl_name=layer_name,
        geom_field="geom",
        area_field="landareal_m2"
        )

    # export to gpkg
    out_layer = f"{layer_name}"
    
    gdf = export_toGDF(db_path, layer_name)
    #print(gdf.head())
    
    # does gdf contain duplicates in naturvernId col?
    #print(gdf['naturvernId'].duplicated().any())
    
    # export gdf to gpkg 
    gdf.crs = "EPSG:25833"

    
    # Write to existing .geopackage
    out_path = os.path.join(data_path, "processed")
    #gdf.to_file(os.path.join(out_path, 'naturvern_per_region_landarea.gpkg'), driver='GPKG', layer=out_layer, mode='w')

    # export gdf to csv 
    df = gdf.drop(columns=["geometry"])
    out_path = os.path.join(csv_path, f"{layer_name}_naturvern.csv")
    #df.to_csv(out_path)