""" 
Script for calculating raster statistics for a given vector layer.
"""

from rasterstats import zonal_stats
import geopandas as gpd
import rasterio


def overlay_stats(raster_path, vector_gdf, buffer_distance) -> gpd.GeoDataFrame:
    
    if buffer_distance > 0:
        gdf = vector_gdf.copy()
        gdf['geometry'] = gdf.buffer(buffer_distance)
    else:
        gdf = vector_gdf.copy()
        
    # calc: min, max, mean, std, median
    stats = zonal_stats(
        gdf, 
        raster_path, 
        stats=['min', 'max', 'mean', 'std', 'median']
        )
    gdf['infra_min'] = [stat['min'] for stat in stats]
    gdf['infra_max'] = [stat['max'] for stat in stats]
    gdf['infra_mean'] = [stat['mean'] for stat in stats]
    gdf['infra_std'] = [stat['std'] for stat in stats]   
    gdf['infra_median'] = [stat['median'] for stat in stats]
    
    # join the results back to the original geodataframe
    vector_gdf = vector_gdf.join(gdf[['infra_min', 'infra_max', 'infra_mean', 'infra_std', 'infra_median']])
    
    return vector_gdf  