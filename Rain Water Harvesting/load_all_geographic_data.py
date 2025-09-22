#!/usr/bin/env python3
"""
Comprehensive script to load all geographic data into PostGIS database.
Handles both vector (shapefile) and raster (GeoTIFF) data.
"""

import geopandas as gpd
import rasterio
from rasterio.transform import from_bounds
import numpy as np
from sqlalchemy import create_engine, text
from pathlib import Path
import os
import sys

# Database connection parameters
DATABASE_URI = 'postgresql://app_user:password@localhost:5432/rtrwh_gis'

# Data directory
DATA_DIR = Path('data')

def load_shapefile_to_postgis(shp_path, table_name):
    """Load a shapefile into PostGIS database."""
    print(f"Loading shapefile: {shp_path}")

    try:
        # Read the shapefile using GeoPandas
        gdf = gpd.read_file(str(shp_path))

        # Check if shapefile was loaded successfully
        if gdf.empty:
            print(f"ERROR: Shapefile {shp_path} is empty or could not be read.")
            return False

        print(f"Loaded {len(gdf)} features from {shp_path.name}.")
        print(f"Columns: {list(gdf.columns)}")
        print(f"CRS: {gdf.crs}")

        # Create database engine
        engine = create_engine(DATABASE_URI)

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
        print(f"ERROR loading {shp_path}: {str(e)}")
        return False

def load_raster_to_postgis(tif_path, table_name):
    """Load a GeoTIFF raster into PostGIS database."""
    print(f"Loading raster: {tif_path}")

    try:
        # Open the raster file
        with rasterio.open(str(tif_path)) as src:
            print(f"Raster size: {src.width} x {src.height}")
            print(f"Number of bands: {src.count}")
            print(f"CRS: {src.crs}")
            print(f"Bounds: {src.bounds}")

            # Read the raster data
            data = src.read(1)  # Read first band
            transform = src.transform
            crs = src.crs

            # Get unique values and their counts (for categorical data)
            unique_values, counts = np.unique(data[data != src.nodata], return_counts=True)

            print(f"Unique values in raster: {len(unique_values)}")
            print(f"Value range: {unique_values.min()} - {unique_values.max()}")

            # For now, we'll store metadata about the raster
            # In a production system, you might want to store the actual raster data
            # using PostGIS raster type, but that requires additional setup

            engine = create_engine(DATABASE_URI)

            # Create a metadata table for rasters
            metadata_table = f"{table_name}_metadata"

            with engine.connect() as conn:
                # Create metadata table if it doesn't exist
                conn.execute(text(f"""
                    CREATE TABLE IF NOT EXISTS {metadata_table} (
                        id SERIAL PRIMARY KEY,
                        raster_path TEXT,
                        width INTEGER,
                        height INTEGER,
                        crs TEXT,
                        bounds_min_x DOUBLE PRECISION,
                        bounds_min_y DOUBLE PRECISION,
                        bounds_max_x DOUBLE PRECISION,
                        bounds_max_y DOUBLE PRECISION,
                        unique_values INTEGER,
                        value_min DOUBLE PRECISION,
                        value_max DOUBLE PRECISION,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))

                # Insert metadata
                conn.execute(text(f"""
                    INSERT INTO {metadata_table}
                    (raster_path, width, height, crs, bounds_min_x, bounds_min_y,
                     bounds_max_x, bounds_max_y, unique_values, value_min, value_max)
                    VALUES (:path, :width, :height, :crs, :minx, :miny, :maxx, :maxy,
                           :unique_vals, :vmin, :vmax)
                """), {
                    'path': str(tif_path),
                    'width': src.width,
                    'height': src.height,
                    'crs': str(crs),
                    'minx': src.bounds.left,
                    'miny': src.bounds.bottom,
                    'maxx': src.bounds.right,
                    'maxy': src.bounds.top,
                    'unique_vals': len(unique_values),
                    'vmin': float(unique_values.min()),
                    'vmax': float(unique_values.max())
                })

                conn.commit()

            print(f"Stored metadata for raster in {metadata_table}")

            # For actual value extraction at coordinates, we'll create a function
            # that can be called from the application
            print(f"Raster {tif_path.name} metadata loaded successfully.")
            return True

    except Exception as e:
        print(f"ERROR loading raster {tif_path}: {str(e)}")
        return False

def get_raster_value_at_coordinate(tif_path, lon, lat):
    """Extract raster value at a specific coordinate."""
    try:
        with rasterio.open(str(tif_path)) as src:
            # Transform lat/lon to pixel coordinates
            row, col = src.index(lon, lat)

            # Check if coordinates are within bounds
            if 0 <= row < src.height and 0 <= col < src.width:
                # Read value at pixel
                value = src.read(1)[row, col]

                # Check for nodata
                if value == src.nodata:
                    return None

                return float(value)
            else:
                return None
    except Exception as e:
        print(f"Error extracting value from {tif_path}: {e}")
        return None

def load_all_geographic_data():
    """Load all geographic data found in the data directory."""
    print("Starting comprehensive geographic data loading...")

    # Define data mappings
    data_mappings = {
        'Major Aquifer': {
            'path': DATA_DIR / 'Major Aquifer' / 'Major_Aquifers.shp',
            'table': 'major_aquifers',
            'type': 'vector'
        },
        'Aquifer Material': {
            'path': DATA_DIR / 'Aquifer Material' / 'Aquif_Mat.shp',
            'table': 'aquifer_materials',
            'type': 'vector'
        },
        'Soil Depth': {
            'path': DATA_DIR / 'Soil Depth' / 'SOILDEPTH.tif',
            'table': 'soil_depth',
            'type': 'raster'
        },
        'Soil Texture': {
            'path': DATA_DIR / 'Soil Texture' / 'SOILTEXTURE.tif',
            'table': 'soil_texture',
            'type': 'raster'
        }
    }

    results = {}

    for name, config in data_mappings.items():
        print(f"\n{'='*50}")
        print(f"Processing: {name}")
        print(f"{'='*50}")

        if config['path'].exists():
            if config['type'] == 'vector':
                success = load_shapefile_to_postgis(config['path'], config['table'])
            elif config['type'] == 'raster':
                success = load_raster_to_postgis(config['path'], config['table'])
            else:
                print(f"Unknown data type for {name}")
                success = False

            results[name] = success
        else:
            print(f"File not found: {config['path']}")
            results[name] = False

    print(f"\n{'='*50}")
    print("LOADING SUMMARY")
    print(f"{'='*50}")

    for name, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"{name}: {status}")

    successful_loads = sum(results.values())
    total_loads = len(results)

    print(f"\nSuccessfully loaded {successful_loads}/{total_loads} datasets.")

    return results

if __name__ == "__main__":
    success = load_all_geographic_data()
    sys.exit(0 if all(success.values()) else 1)