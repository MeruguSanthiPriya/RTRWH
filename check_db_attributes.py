import sqlalchemy

# Database connection parameters
DATABASE_URI = 'postgresql://app_user:password@localhost:5432/rtrwh_gis'
TABLES_TO_CHECK = [
    'aquifer_materials',
    'major_aquifers',
    'ground_water_level_stations',
    'ground_water_quality_stations',
    'soil_depth_vector',
    'soil_texture_vector',
    'soil_slope_vector'
]

try:
    # Create database engine
    engine = sqlalchemy.create_engine(DATABASE_URI)

    with engine.connect() as connection:
        print("--- Database Contents ---")
        inspector = sqlalchemy.inspect(engine)
        for table_name in TABLES_TO_CHECK:
            print(f"\n--- Table: {table_name} ---")
            if not inspector.has_table(table_name):
                print("Table does not exist.")
                continue
            
            try:
                columns = inspector.get_columns(table_name)
                
                if not columns:
                    print(f"Table '{table_name}' has no columns.")
                    continue

                print(f"Number of attributes (columns): {len(columns)}")
                print("Attributes:")
                for column in columns:
                    print(f"- {column['name']} ({column['type']})")

            except Exception as e:
                print(f"Could not inspect table '{table_name}'. Error: {e}")

except Exception as e:
    print(f"ERROR connecting to the database: {e}")
