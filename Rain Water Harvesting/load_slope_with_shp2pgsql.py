#!/usr/bin/env python3
"""
Script to vectorize the soil slope raster and load it into PostGIS using shp2pgsql.
This is an alternative, more memory-efficient approach for large datasets.
"""

import subprocess
import os
import tempfile
import shutil
import geopandas as gpd

# --- Configuration ---
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "rtrwh_gis"
DB_USER = "app_user"
DB_PASSWORD = "password"

RASTER_CONFIG = {
    'path': os.path.join(os.path.dirname(__file__), 'data', 'Soil Slope', 'SOILSLOPE.tif'),
    'table': 'soil_slope_vector',
    'value_column': 'slope_class',
    'description': 'Vectorized soil slope classification'
}

# --- Helper Functions ---

def check_tool(name):
    """Check if a command-line tool is available in the system's PATH."""
    if shutil.which(name) is None:
        print(f"FATAL ERROR: `{name}` is required but not found in PATH.")
        return False
    return True

def vectorize_raster(raster_path, output_shp, value_column):
    """
    Converts a raster file to a vector shapefile using gdal_polygonize.
    """
    print(f"Vectorizing {os.path.basename(raster_path)}...")
    if not os.path.exists(raster_path):
        print(f"ERROR: Raster file not found: {raster_path}")
        return False

    layer_name = os.path.splitext(os.path.basename(output_shp))[0]
    cmd = [
        "gdal_polygonize.py",
        raster_path,
        output_shp,
        layer_name,
        value_column
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Vectorization successful.")
        
        # Reproject to EPSG:4326
        print("Reprojecting shapefile to EPSG:4326...")
        gdf = gpd.read_file(output_shp)
        if gdf.crs.to_epsg() != 4326:
            gdf = gdf.to_crs(epsg=4326)
            gdf.to_file(output_shp)
        print("Reprojection successful.")

        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR during vectorization: {e.stderr}")
        return False

def load_with_shp2pgsql(shapefile_path, table_name):
    """
    Loads a shapefile into PostGIS using the shp2pgsql command-line tool.
    """
    print(f"Loading {os.path.basename(shapefile_path)} into table '{table_name}' using shp2pgsql...")

    # shp2pgsql command
    # -s 4326: SRID of the input data
    # -I: Create a spatial index on the geometry column
    # -c: Create a new table. Drops the table if it exists.
    shp2pgsql_cmd = [
        "shp2pgsql",
        "-s", "4326",
        "-I",
        "-c", 
        shapefile_path,
        f"public.{table_name}"
    ]

    # psql command
    psql_cmd = [
        "psql",
        "-h", DB_HOST,
        "-p", DB_PORT,
        "-U", DB_USER,
        "-d", DB_NAME
    ]

    try:
        # Start the shp2pgsql process
        shp2pgsql_process = subprocess.Popen(shp2pgsql_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Start the psql process, taking input from shp2pgsql's output
        psql_process = subprocess.Popen(
            psql_cmd,
            stdin=shp2pgsql_process.stdout,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env={**os.environ, "PGPASSWORD": DB_PASSWORD}
        )

        # Allow shp2pgsql_process to receive a SIGPIPE if psql_process exits.
        shp2pgsql_process.stdout.close()

        # Wait for the processes to complete and get their output
        shp2pgsql_stderr = shp2pgsql_process.communicate()[1]
        psql_stdout, psql_stderr = psql_process.communicate()

        if shp2pgsql_process.returncode != 0:
            print(f"ERROR in shp2pgsql: {shp2pgsql_stderr}")
            return False
        
        if psql_process.returncode != 0:
            print(f"ERROR in psql: {psql_stderr}")
            return False

        print(f"Successfully loaded data into '{table_name}'.")
        return True

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

def main():
    """
    Main execution function.
    """
    if not all([check_tool("gdal_polygonize.py"), check_tool("shp2pgsql"), check_tool("psql")]):
        return

    print("\n" + "="*50)
    print(f"Processing: {RASTER_CONFIG['description']}")
    print("="*50)

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_shp_path = os.path.join(temp_dir, "temp_slope_vector.shp")

        # Step 1: Vectorize the raster
        if not vectorize_raster(RASTER_CONFIG['path'], temp_shp_path, RASTER_CONFIG['value_column']):
            print("Aborting due to vectorization failure.")
            return

        # Step 2: Load the shapefile using shp2pgsql
        if not load_with_shp2pgsql(temp_shp_path, RASTER_CONFIG['table']):
            print("Aborting due to database loading failure.")
            return
    
    print("\nProcess completed successfully.")

if __name__ == "__main__":
    main()
