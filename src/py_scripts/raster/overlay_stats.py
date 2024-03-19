""" 
Script for calculating raster statistics for a given vector layer.
"""

from rasterstats import zonal_stats
import geopandas as gpd
import rasterio


def overlay_stats(raster_path, vector_gdf, buffer_distance) -> gpd.GeoDataFrame:
    
    if buffer_distance > 0:
        vector_gdf['geometry'] = vector_gdf.buffer(buffer_distance)
    
    # calc: min, max, mean, std, median
    stats = zonal_stats(
        vector_gdf, 
        raster_path, 
        stats=['min', 'max', 'mean', 'std', 'median']
        )
    vector_gdf['infra_min'] = [stat['min'] for stat in stats]
    vector_gdf['infra_max'] = [stat['max'] for stat in stats]
    vector_gdf['infra_mean'] = [stat['mean'] for stat in stats]
    vector_gdf['infra_std'] = [stat['std'] for stat in stats]   
    vector_gdf['infra_median'] = [stat['median'] for stat in stats]

    return vector_gdf  