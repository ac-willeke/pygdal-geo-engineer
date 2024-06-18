"""Overlay analyis for nature conservation areas."""

## TODO write to functions and main 
import sys
import os
import duckdb
from pathlib import Path
from tqdm import tqdm  # progressbar
import logging

# add local modules to python path
project_path = Path.cwd()
module_path = os.path.join(project_path, "src")

sys.path.append(module_path)

from py_scripts.config import load_catalog, load_parameters
from py_scripts.logger import setup_logging
from py_scripts import decorators as dec
from py_scripts.my_duckdb import *

# init catalog and params
catalog = load_catalog()
params = load_parameters()


def inject_db(dict_gpkg_lyr, convert_geom=False):
    """Load geopackage layers into DuckDB database.
    Args:
        dict_gpkg_lyr (Dict): dict with geopackage path and layer name.
        convert_geom (bool, optional): Convert BLOB to geom. Defaults to False.
    """
    # load into DuckDB
    for gpkg, layer in tqdm(dict_gpkg_lyr.items(), desc="Loading GPKG Layers"):
        logging.info(f"Loading {layer} from {gpkg}")
        load_gpkg_layers(db_path, gpkg, layer)

    if convert_geom:
    # cast BLOB (Binary Large Object) to geometry for spatial operations
        con = duckdb.connect(db_path)
        con.install_extension('spatial')
        con.load_extension('spatial')

    # duckdb tables names to list
        tables = con.execute("SHOW TABLES;").fetchdf()
        tables = tables["name"].to_list()
        logging.info(tables)

        for table in tables:
            blob_to_geom(
            db_path=db_path,
            tbl_name=table,
            blob_field="geometry",
            geom_field="geom",   
        )


def view_duckdb():
    con = duckdb.connect(db_path)
    tables = con.execute("SHOW TABLES;").fetchdf()
    tables = tables["name"].to_list()
    print(tables)

    for table in tables:
        print(table)
        print(con.execute(f"SELECT * FROM {table} LIMIT 1;").fetchdf())

def create_id(tbl_study_area):
    # add a column "identifikasjon_lokalId" to the table "norge_landareal_n50"
    # fill column 0 - x
    con = duckdb.connect(db_path)
    con.install_extension('spatial')
    con.load_extension('spatial')

    # Get table information
    table_info = con.execute(f"PRAGMA table_info({tbl_study_area})").fetchall()
    column_names = [info[1] for info in table_info]

    # If the column does not exist, add it
    if "identifikasjon_lokalId" not in column_names:
        con.execute(f"ALTER TABLE {tbl_study_area} ADD COLUMN identifikasjon_lokalId INTEGER;")
        con.execute(f"UPDATE {tbl_study_area}  SET identifikasjon_lokalId = rowid;")

    con.close()

def calculate_ar50_overlap(db_path, tbl_study_area, tbl_ar50="ar50_flate", id_field="identifikasjon_lokalId", ar50_field="ar50_bonitet"):
    # Calculate area overlap for each Bonitet class
    for area_class in range(1, 19):  # 1-18
        logging.info(f"Calculating Bonitet class {area_class}")
        new_field = f"ar50_bon{area_class}_m2"
        remove_field(db_path, tbl_study_area, new_field)
        ar50_area_class(db_path, tbl_study_area, id_field, tbl_ar50, ar50_field, area_class, new_field)

    # Set null ar50_bonx fields to 0
    with duckdb.connect(db_path) as con:
        con.install_extension('spatial')
        con.load_extension('spatial')
        for area_class in range(1, 19):  # 1-18
            new_field = f"ar50_bon{area_class}_m2"
            con.execute(f"UPDATE {tbl_study_area} SET {new_field} = 0 WHERE {new_field} IS NULL")


def display_ar50_stats(db_path, tbl_study_area, id_field):
    
    # print as dataframe
    con = duckdb.connect(db_path)
    df = con.execute(f"SELECT * FROM {tbl_study_area}").fetchdf()
    # Display initial data
    cols_ar50 = [col for col in df.columns if "ar50_bon" in col and col != "sum_ar50_bon_m2"]
    cols = [id_field] + cols_ar50
    logging.info(df[cols].head(5))
    
    # remove fields
    remove_field(db_path, tbl_study_area, "sum_ar50_bon_m2")
    remove_field(db_path, tbl_study_area, "areal_m2")
    remove_field(db_path, tbl_study_area, "area_diff_m2")
    
    # Sum of all bonitet classes and other calculations
    sum_area_cols(db_path, tbl_study_area, id_field, cols_ar50, "sum_ar50_bon_m2")
    geom_area(db_path, tbl_study_area, "geom", "areal_m2")
    area_difference(db_path, tbl_study_area, "sum_ar50_bon_m2", "areal_m2", "area_diff_m2")

    # Final display of data
    cols = [id_field] + ["sum_ar50_bon_m2", "areal_m2", "area_diff_m2"]
    df_ar50 = df[cols].sort_values(by="area_diff_m2", ascending=True)
    logging.info(df_ar50.head(5))
    logging.info(f"Number of rows: {df_ar50.shape[0]}")
    logging.info(f"Number of unique ids: {df_ar50[id_field].nunique()}")
    
    # close
    con.close()


def export(db_path, db_table, gpkg_path, csv_path, crs = "EPSG:25833"):
    """Export to GPKG and CSV files.

    Args:
        db_path (_type_): _description_
        db_table (_type_): table to be exported
        gpkg_path (_type_): path to geopackage file
        csv_path (_type_): path to csv file
        crs (string): EPSG code. Defaults to "EPSG:25833".
    """
    from shapely import wkt
    con = duckdb.connect(db_path)
    con.install_extension('spatial')
    con.load_extension('spatial')

    # to dataframe  
    df = con.execute(f"SELECT ST_AsText(geom) as geometry, * FROM {db_table}").fetchdf()
    df = df.drop(columns=["geom"])

    # Convert the geom column to gpd GeoDataFrame
    df['geometry'] = df['geometry'].apply(wkt.loads)
    gdf = gpd.GeoDataFrame(df, geometry='geometry')
    gdf.crs = crs
    df_csv = gdf.drop(columns=["geometry"]) 
    
    # Export GDF to file 
    gdf.to_file(gpkg_path, driver='GPKG', layer=tbl_study_area, mode='w')
    df_csv.to_csv(csv_path)


if __name__ == "__main__":
    # setup loggging for standalone use of logger.py
    setup_logging()
    logger = logging.getLogger(__name__)
    logging.info(f"Adding {module_path} to sys.path")
    
    # load paths from catalog
    data_path = catalog["project_data"]["filepath"]
    db_path = os.path.join(data_path, "interim", "verg_og_bevaring.db")
    bevaring_gpkg = os.path.join(data_path, "interim", "bevaring_25833.gpkg")
    mis_gpkg = os.path.join(data_path, "interim", "mis_livsmiljoer_nokkelbiotoper.gpkg")
    plan_gpkg = os.path.join(data_path, "interim", "plan_verneformal_25833.gpkg")
        
    # dict gpkg:lyr
    dict_gpkg_lyr = {
        mis_gpkg: "mis_LM_NB",
        plan_gpkg : "plan_verneformal",
        bevaring_gpkg: "ar50_flate",
    }
    tbl_study_area = "plan_verneformal"
    
    data_injection = False
    data_processing = True
    data_analysis = False
    data_export = False
    
    # DATA INJECTION
    if data_injection:
        inject_db(dict_gpkg_lyr, convert_geom=False)
    
    # DATA PROCESSING
    if data_processing:
        view_duckdb()
        create_id(tbl_study_area)
    
    # DATA ANALYSIS
    if data_analysis:
        calculate_ar50_overlap(
            db_path, 
            tbl_study_area, 
            tbl_ar50="ar50_flate", 
            id_field="identifikasjon_lokalId", 
            ar50_field="ar50_bonitet"
            )
        
        display_ar50_stats(
            db_path, 
            tbl_study_area, 
            id_field="identifikasjon_lokalId",)

    # DATA EXPORT
    if data_export:
        export(
            db_path, 
            db_table = tbl_study_area,
            gpkg_path = os.path.join(data_path, "processed", f"{tbl_study_area}_overlapp.gpkg"),
            csv_path = os.path.join(data_path, "processed", f'{tbl_study_area}_overlapp.csv'),
            crs = "EPSG:25833"
            )
