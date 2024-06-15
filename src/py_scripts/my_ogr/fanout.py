import argparse
from osgeo import ogr

def fanout(vector_dataset, region_dataset, output_base_name):
    """Fanout a vector dataset based on a region dataset

    Args:
        vector_dataset (str): path to vector dataset
        region_dataset (str): path to region dataset to fanout the vector dataset
    """
    
    # Load the vector dataset
    vector_ds = ogr.Open(vector_dataset, 0)
    vector_layer = vector_ds.GetLayer()

    # Load the region dataset
    region_ds = ogr.Open(region_dataset, 0)
    region_layer = region_ds.GetLayer()

    # Loop through each region
    for i in range(region_layer.GetFeatureCount()):
        region_feature = region_layer.GetFeature(i)
        region_geom = region_feature.GetGeometryRef()

        # Create a new layer for this region
        driver = ogr.GetDriverByName('ESRI Shapefile')
        output_ds = driver.CreateDataSource(f'{output_base_name}_{i+1}.shp')
        output_layer = output_ds.CreateLayer('', vector_layer.GetSpatialRef(), ogr.wkbPolygon)

        # Loop through each polygon in the vector dataset
        for j in range(vector_layer.GetFeatureCount()):
            vector_feature = vector_layer.GetFeature(j)
            vector_geom = vector_feature.GetGeometryRef()

            # Check if the polygon intersects with the current region
            if vector_geom.Intersects(region_geom):
                # Clip the polygon with the region's outline and add it to the current region's layer
                intersection_geom = vector_geom.Intersection(region_geom)
                intersection_feature = ogr.Feature(output_layer.GetLayerDefn())
                intersection_feature.SetGeometry(intersection_geom)
                output_layer.CreateFeature(intersection_feature)

        # Cleanup
        output_ds = None

    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fanout a vector dataset based on a region dataset')
    parser.add_argument('vector_dataset', type=str, help='Path to vector dataset')
    parser.add_argument('region_dataset', type=str, help='Path to region dataset to fanout the vector dataset')
    parser.add_argument('output_base_name', type=str, help='Base name for output files')
    args = parser.parse_args()

    fanout(args.vector_dataset, args.region_dataset, args.output_base_name)
    
# python fanout.py vector_dataset.shp region_dataset.shp output_base_name

