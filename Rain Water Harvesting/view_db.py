import sqlite3
import os

# --- Configuration ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, 'instance', 'rtrwh_data.db')
TABLES_TO_VIEW = ['user_input', 'admin_user']

# --- Main Script ---
if not os.path.exists(DB_FILE):
    print(f"Error: Database file not found at '{DB_FILE}'")
    exit()

try:
    # Connect to the SQLite database
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name
    cursor = conn.cursor()

    print(f"--- Contents of Database: {os.path.basename(DB_FILE)} ---\n")

    for table_name in TABLES_TO_VIEW:
        print(f"--- Table: {table_name} ---")
        try:
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()

            if not rows:
                print("Table is empty.\n")
                continue

            # Print header
            headers = [description[0] for description in cursor.description]
            print(" | ".join(f"{h:<20}" for h in headers))
            print("-" * (23 * len(headers) - 1))

            # Print rows
            for row in rows:
                # Truncate long values for better display
                values = [str(row[h])[:18] + '..' if len(str(row[h] or '')) > 20 else str(row[h] or '') for h in headers]
                print(" | ".join(f"{v:<20}" for v in values))
            
            print("\n")

        except sqlite3.OperationalError:
            print(f"Table '{table_name}' does not exist.\n")

except sqlite3.Error as e:
    print(f"Database error: {e}")

finally:
    if conn:
        conn.close()