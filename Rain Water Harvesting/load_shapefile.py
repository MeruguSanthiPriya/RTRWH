#!/usr/bin/env python3
"""
Script to load shapefile data into PostGIS database using GeoPandas.
Run this script to import the aquifer material data.
"""

import geopandas as gpd
from sqlalchemy import create_engine, text
import os
import sys

# Database connection parameters
DATABASE_URI = 'postgresql://app_user:password@localhost:5432/rtrwh_gis'

# Path to the shapefile
SHAPEFILE_PATH = os.path.join(os.path.dirname(__file__), 'data', 'Aquifer Material', 'Aquif_Mat.shp')

def load_shapefile_to_postgis():
    """Load shapefile data into PostGIS database."""

    print("Loading shapefile data into PostGIS...")

    try:
        # Read the shapefile using GeoPandas
        print(f"Reading shapefile from: {SHAPEFILE_PATH}")
        gdf = gpd.read_file(SHAPEFILE_PATH)

        # Check if shapefile was loaded successfully
        if gdf.empty:
            print("ERROR: Shapefile is empty or could not be read.")
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
        table_name = 'aquifer_materials'
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

        print("Data loading completed successfully!")
        return True

    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    success = load_shapefile_to_postgis()
    sys.exit(0 if success else 1)