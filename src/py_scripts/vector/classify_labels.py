"""Import gpkg layer into gdf and create a label-column with classification of the data."""

# import gpkg into gdf
def create_labels(gdf, col_value, col_label, ls_labels):
    import pandas as pd
    
    # create label column
    gdf[col_label] = None
    gdf['bins'] = None

    # generate string labels
    ls_labels_str = []
    for i in range(len(ls_labels)-1):
        ls_labels_str.append(f"{ls_labels[i]}-{ls_labels[i+1]}%")
        
    # change first label to start from 0 instead of -0.01
    if ls_labels[0] == -0.01:
        ls_labels_str[0] = f"0-{ls_labels[1]}%"
    
    # change last label to start with ">" sign
    # ls_labels_str[-1] = f">{ls_labels[-2]}%"

    # classify data
    gdf['bins'] = pd.cut(gdf[col_value], bins=ls_labels)

    # create dict
    bin_intervals = gdf['bins'].cat.categories
    label_dict = dict(zip(bin_intervals, ls_labels_str))

    gdf[col_label] = gdf['bins'].map(label_dict)
    
    # set label col to string
    gdf[col_label] = gdf[col_label].astype(str)
    
    # remove bin column     
    gdf = gdf.drop(columns=['bins'])

    return gdf

# group/merge features based on label

def aggr_byLabel(gdf, col_label):
    import pandas as pd
    import geopandas as gpd
    import shapely.wkt as wkt
    
    # Remove or fix invalid geometries
    # gdf = gdf[gdf['geometry'].is_valid]

    #gdf_grouped = gdf.groupby(col_label)['geometry'].apply(lambda x: x.unary_union)
    gdf_grouped = gdf.dissolve(by=col_label)

    gdf_grouped = gdf_grouped[['geometry']]
    
    # create gdf
    gdf_grouped = gpd.GeoDataFrame(gdf_grouped, geometry='geometry')
    
    # remove all cols except for label and geometry

    
    return gdf_grouped

if __name__ == "__main__":
    import os 
    import geopandas as gpd
    
    from py_scripts.config import load_catalog
    
    # load paths from catalog
    catalog = load_catalog()
    data_path = catalog["project_data"]["filepath"]
    gpkg_path = os.path.join(data_path, "processed", "vern_og_bevaring.gpkg")
    
    # set parameters
    layer_name = "norge_ruter_10km"
    ls_labels = [-0.01, 5, 10, 15, 20, 30, 50, 70, 100]
    col_value = "tetthet_naturvern"
    col_label = "label"
    
    # import gpkg 
    gdf = gpd.read_file(gpkg_path, layer=layer_name)
    
    gdf_labelled = create_labels(gdf, col_value, col_label, ls_labels)
    gdf_grouped = aggr_byLabel(gdf_labelled, col_label)
    
    print(gdf_grouped.head())
    
    # export to gpkg 
    out_path = gpkg_path
    out_layer = f"{layer_name}_labelled"
    gdf_labelled.to_file(out_path, layer=out_layer, driver="GPKG")
    gdf_grouped.to_file(out_path, layer=f"{layer_name}_grouped", driver="GPKG")


    
        
    
    
