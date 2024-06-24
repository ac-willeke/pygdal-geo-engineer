"""
Main Script

This script servers as the entry point
for the sub-packages and modules of the project.
"""
import logging
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parents[1]

import decorators as dec  # noqa
from config import load_catalog, load_parameters  # noqa

# setup logging
from logger import setup_logging  # noqa

config_file = os.path.join(project_root, "config/logging.yaml")
setup_logger = setup_logging(config_file)
logger = logging.getLogger(__name__)

# GET CAPABILITIES
# http://urban.nina.no/geoserver/wfs?service=WFS&request=GetCapabilities


# GET FEATURE
def to_geojson(url, layer, output_dir):
    """request data from geonode and save as geojson

    Args:
        url (str): url to geonode endpoint
        layer (str): layer name

    Raises:
        Exception: Failed to download WFS data: {response.status_code}

    Returns:
        _type_: _description_
    """
    import geojson
    import requests

    # Construct the GetFeature request URL
    params = {
        "service": "WFS",
        "request": "GetFeature",
        "typeName": layer,
        "outputFormat": "json",
    }

    response = requests.get(url, params=params)

    # Check the response status code
    if response.status_code != 200:
        raise Exception("Failed to download WFS data: {}".format(response.status_code))
        return None

    try:
        # Parse the JSON response into a GeoJSON object
        geojson_data = geojson.loads(response.content)

        filename = f"{layer}.geojson"
        # replace : with _ in filename
        filename = filename.replace(":", "_")

        path = os.path.join(output_dir, filename)

        # Save the GeoJSON data to a file
        with open(path, "w") as f:
            geojson.dump(geojson_data, f)

        logger.info("Saved geojson file: %s", filename)
        return filename
    except Exception as e:
        logger.error(f"Raised Exception: {e}")
        logger.error(f"{layer} not saved")
        output = None
        logger.info(f"Returned: - End function {output!r}")

        return output


if __name__ == "__main__":
    catalog = load_catalog()
    layers = catalog["urban-geonode"]["layers"]
    # print (layers)
    output_dir = catalog["urban-geonode"]["filepath"]
    wfs = catalog["urban-geonode"]["wfs"]

    for layer in layers:
        layer_str = str(layer)
        to_geojson(wfs, layer_str, output_dir)
