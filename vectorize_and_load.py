#!/usr/bin/env python3
"""
Script to vectorize raster data and load it into the PostGIS database.
This script converts a raster file into a vector format (polygons) and
then loads the vectorized data into a specified table.
"""

import subprocess
import os
import geopandas as gpd
from sqlalchemy import create_engine
import tempfile
import shutil

# --- Configuration ---
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "rtrwh_gis"
DB_USER = "app_user"
DB_PASSWORD = "password"

 # List of raster files to process
RASTER_CONFIGS = [
    # {
    #     'path': os.path.join(os.path.dirname(__file__), 'data', 'Soil Depth', 'SOILDEPTH.tif'),
    #     'table': 'soil_depth_vector',
    #     'value_column': 'depth_class',
    #     'description': 'Vectorized soil depth classification'
    # },
    # {
    #     'path': os.path.join(os.path.dirname(__file__), 'data', 'Soil Texture', 'SOILTEXTURE.tif'),
    #     'table': 'soil_texture_vector',
    #     'value_column': 'texture_class',
    #     'description': 'Vectorized soil texture classification'
    # },
    {
        'path': os.path.join(os.path.dirname(__file__), 'data', 'Soil Slope', 'Soil Slope', 'SOILSLOPE.tif'),
        'table': 'soil_slope_vector',
        'value_column': 'slope_class',
        'description': 'Vectorized soil slope classification'
    }
]

# --- Main Functions ---

def check_gdal_polygonize():
    """Check if gdal_polygonize.py is available in the system's PATH."""
    return shutil.which("gdal_polygonize.py") is not None

def vectorize_raster(raster_path, output_shp, value_column):
    """
    Converts a raster file to a vector shapefile using gdal_polygonize.
    """
    print(f"Vectorizing {os.path.basename(raster_path)}...")
    if not os.path.exists(raster_path):
        print(f"ERROR: Raster file not found: {raster_path}")
        return False

    # Command to run gdal_polygonize.py
    # It creates a shapefile where each polygon has a value field.
    # The field name is passed as the last argument.
    layer_name = os.path.splitext(os.path.basename(output_shp))[0]
    cmd = [
        "gdal_polygonize.py",
        raster_path,
        output_shp,
        layer_name,
        value_column
    ]

    try:
        process = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True
        )
        print("Vectorization successful.")
        return True
    except subprocess.CalledProcessError as e:
        print("ERROR during vectorization:")
        print(f"Command: {' '.join(e.cmd)}")
        print(f"Return Code: {e.returncode}")
        print(f"Output: {e.stdout}")
        print(f"Error Output: {e.stderr}")
        return False
    except FileNotFoundError:
        print("ERROR: `gdal_polygonize.py` not found.")
        print("Please ensure GDAL is installed and the script is in your PATH.")
        return False


def load_shapefile_to_postgis(shapefile_path, table_name, db_connection_str):
    """
    Loads a shapefile into a PostGIS table using GeoPandas.
    """
    print(f"Loading {os.path.basename(shapefile_path)} into table '{table_name}'...")
    try:
        # Read shapefile
        gdf = gpd.read_file(shapefile_path)

        # Ensure projection is WGS84 (EPSG:4326)
        if gdf.crs.to_epsg() != 4326:
            print("Reprojecting to EPSG:4326...")
            gdf = gdf.to_crs(epsg=4326)

        # Create SQLAlchemy engine
        engine = create_engine(db_connection_str)

        # Load data into PostGIS
        gdf.to_postgis(
            name=table_name,
            con=engine,
            if_exists='replace',
            index=True,
            index_label='id'
        )
        print(f"Successfully loaded data into '{table_name}'.")
        return True
    except Exception as e:
        print(f"ERROR: Failed to load shapefile to PostGIS: {e}")
        return False

def main():
    """
    Main execution function to process all configured rasters.
    """
    if not check_gdal_polygonize():
        print("FATAL: `gdal_polygonize.py` is required but not found in PATH.")
        print("Please install GDAL/OGR utilities.")
        return

    db_connection_str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    for config in RASTER_CONFIGS:
        print("\n" + "="*50)
        print(f"Processing: {config['description']}")
        print("="*50)

        # Create a temporary directory to store the intermediate shapefile
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_shp_path = os.path.join(temp_dir, "temp_vector.shp")

            # Step 1: Vectorize the raster to a shapefile
            if not vectorize_raster(config['path'], temp_shp_path, config['value_column']):
                print("Skipping this raster due to vectorization failure.")
                continue

            # Step 2: Load the resulting shapefile into PostGIS
            if not load_shapefile_to_postgis(temp_shp_path, config['table'], db_connection_str):
                print("Skipping this raster due to database loading failure.")
                continue
        
        print(f"Successfully processed and loaded {config['description']}.")

if __name__ == "__main__":
    main()
