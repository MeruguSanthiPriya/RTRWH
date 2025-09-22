#!/usr/bin/env python3
"""
Script to load raster data (GeoTIFF) into a PostGIS database.
Run this script to import soil depth and soil texture rasters.
"""

import subprocess
import os
import sys

# Database connection parameters
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "rtrwh_gis"
DB_USER = "app_user"
DB_PASSWORD = "password"

# Raster file paths
RASTER_CONFIGS = [
    {
        'path': os.path.join(os.path.dirname(__file__), 'data', 'Soil Depth', 'SOILDEPTH.tif'),
        'table': 'soil_depth',
        'description': 'Soil depth classification raster'
    },
    {
        'path': os.path.join(os.path.dirname(__file__), 'data', 'Soil Texture', 'SOILTEXTURE.tif'),
        'table': 'soil_texture',
        'description': 'Soil texture classification raster'
    }
]


def run_raster2pgsql(raster_path, table_name):
    """Load a raster file into PostGIS using raster2pgsql."""

    if not os.path.exists(raster_path):
        print(f"ERROR: Raster file not found: {raster_path}")
        return False

    print(f"Loading raster: {raster_path}")
    print(f"Target table: {table_name}")

    # Build the raster2pgsql command
    cmd = [
        "raster2pgsql",
        "-s", "4326",  # SRID
        "-I",  # Create spatial index
        "-C",  # Apply raster constraints
        "-t", "100x100",  # Tile size for better performance
        raster_path,
        "public." + table_name
    ]

    try:
        # Run raster2pgsql and pipe output to psql
        raster_process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Pipe the output to psql
        psql_cmd = [
            "psql",
            "-h", DB_HOST,
            "-p", DB_PORT,
            "-U", DB_USER,
            "-d", DB_NAME
        ]

        psql_process = subprocess.Popen(
            psql_cmd,
            stdin=raster_process.stdout,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env={**os.environ, "PGPASSWORD": DB_PASSWORD}
        )

        # Close the stdout of raster2pgsql so psql gets EOF
        raster_process.stdout.close()

        # Wait for both processes to complete
        raster_stdout, raster_stderr = raster_process.communicate()
        psql_stdout, psql_stderr = psql_process.communicate()

        if raster_process.returncode != 0:
            print(f"ERROR in raster2pgsql: {raster_stderr}")
            return False

        if psql_process.returncode != 0:
            print(f"ERROR in psql: {psql_stderr}")
            return False

        print(f"Successfully loaded {table_name}")
        return True

    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False


def load_raster_data():
    """Load all soil-related raster data."""

    print("Loading soil raster data into PostGIS...")

    success_count = 0
    total_count = len(RASTER_CONFIGS)

    for config in RASTER_CONFIGS:
        print(f"\n{'='*50}")
        print(f"Processing: {config['path']}")
        print(f"Table: {config['table']}")
        print(f"Description: {config['description']}")
        print(f"{'='*50}")

        if run_raster2pgsql(config['path'], config['table']):
            success_count += 1
        else:
            print(f"Failed to load: {config['path']}")

    print(f"\n{'='*50}")
    print(f"Summary: {success_count}/{total_count} rasters loaded successfully")
    print(f"{'='*50}")

    if success_count == total_count:
        print("All soil raster data loaded successfully!")
        return True
    else:
        print("Some rasters failed to load.")
        return False


if __name__ == "__main__":
    success = load_raster_data()
    sys.exit(0 if success else 1)