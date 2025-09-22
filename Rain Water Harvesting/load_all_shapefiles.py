#!/usr/bin/env python3
"""
Script to load all available shapefiles into PostGIS database.
This script automatically discovers and loads all shapefiles in the data directory.
"""

import geopandas as gpd
from sqlalchemy import create_engine, text
import os
import sys
from pathlib import Path

# Database connection parameters
DATABASE_URI = 'postgresql://app_user:password@localhost:5432/rtrwh_gis'

# Data directory
DATA_DIR = Path(__file__).parent / 'data'

def load_shapefile_to_postgis(shapefile_path, table_name):
    """Load a single shapefile into PostGIS database."""

    print(f"\nLoading shapefile: {shapefile_path}")
    print(f"Target table: {table_name}")

    try:
        # Read the shapefile using GeoPandas
        gdf = gpd.read_file(str(shapefile_path))

        # Check if shapefile was loaded successfully
        if gdf.empty:
            print(f"ERROR: Shapefile {shapefile_path} is empty or could not be read.")
            return False

        print(f"Loaded {len(gdf)} features from shapefile.")
        print(f"Columns: {list(gdf.columns)}")
        print(f"CRS: {gdf.crs}")

        # Create database engine
        engine = create_engine(DATABASE_URI)

        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            print("Connected to database successfully.")

        # Convert CRS to WGS84 (EPSG:4326) if not already
        if gdf.crs != 'EPSG:4326':
            print("Converting CRS to WGS84 (EPSG:4326)...")
            gdf = gdf.to_crs('EPSG:4326')

        # Load data into PostGIS
        print(f"Loading data into table: {table_name}")

        # Use GeoPandas to_postgis method
        gdf.to_postgis(
            name=table_name,
            con=engine,
            schema='public',
            if_exists='replace',  # Replace table if it exists
            index=False
        )

        # Create spatial index for better query performance
        # Note: GeoPandas creates the geometry column with the name from the GeoDataFrame
        # Let's check what the geometry column is actually named
        geom_col = gdf.geometry.name if hasattr(gdf.geometry, 'name') else 'geometry'
        print(f"Geometry column name: {geom_col}")

        with engine.connect() as conn:
            conn.execute(text(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_{geom_col} ON {table_name} USING GIST ({geom_col});"))
            print("Created spatial index.")

        # Verify the data was loaded
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
            count = result.fetchone()[0]
            print(f"Successfully loaded {count} records into {table_name} table.")

        return True

    except Exception as e:
        print(f"ERROR loading {shapefile_path}: {str(e)}")
        return False

def load_all_shapefiles():
    """Load all shapefiles found in the data directory."""

    print("Discovering shapefiles in data directory...")

    # Find all shapefiles
    shapefiles = list(DATA_DIR.rglob("*.shp"))
    print(f"Found {len(shapefiles)} shapefile(s)")

    if not shapefiles:
        print("No shapefiles found in data directory.")
        return False

    # Define mapping from shapefile names to table names
    shapefile_mapping = {
        'Aquif_Mat.shp': 'aquifer_materials',
        'Major_Aquifers.shp': 'major_aquifers',
        # Add more mappings as needed
    }

    success_count = 0

    for shapefile_path in shapefiles:
        filename = shapefile_path.name

        # Determine table name
        if filename in shapefile_mapping:
            table_name = shapefile_mapping[filename]
        else:
            # Generate table name from filename (remove extension and make lowercase)
            table_name = filename.replace('.shp', '').lower().replace(' ', '_')

        print(f"\n{'='*50}")
        print(f"Processing: {filename}")
        print(f"{'='*50}")

        if load_shapefile_to_postgis(shapefile_path, table_name):
            success_count += 1
        else:
            print(f"Failed to load {filename}")

    print(f"\n{'='*50}")
    print(f"Loading complete: {success_count}/{len(shapefiles)} shapefiles loaded successfully")
    print(f"{'='*50}")

    return success_count == len(shapefiles)

if __name__ == "__main__":
    success = load_all_shapefiles()
    sys.exit(0 if success else 1)