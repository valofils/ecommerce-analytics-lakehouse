import duckdb
import os

# Define paths
DATA_DIR = 'data'
DB_FILE = os.path.join(DATA_DIR, 'ecommerce.duckdb')

# Define the CSV files and their corresponding table names in the raw schema
TABLE_MAPPINGS = {
    'raw_users': 'raw_users.csv',
    'raw_products': 'raw_products.csv',
    'raw_orders': 'raw_orders.csv',
    'raw_order_items': 'raw_order_items.csv'
}

def load_data():
    # Delete existing database if it exists to ensure a fresh run
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print("Removed existing database.")

    # Connect to DuckDB (it will create the file if it doesn't exist)
    con = duckdb.connect(DB_FILE)
    print("Connected to DuckDB.")

    # Create the 'raw' schema to separate source data from transformed data
    con.execute("CREATE SCHEMA IF NOT EXISTS raw;")
    print("Created 'raw' schema.")

    # Load each CSV into its corresponding table
    for table_name, file_name in TABLE_MAPPINGS.items():
        file_path = os.path.join(DATA_DIR, file_name)
        
        if not os.path.exists(file_path):
            print(f"Warning: {file_path} not found. Skipping.")
            continue
            
        print(f"Loading {file_name} into raw.{table_name}...")
        
        # Use DuckDB's native CSV reader (much faster than pandas for large files)
        # We auto-detect types but keep the raw data as true to the CSV as possible
        load_sql = f"""
            CREATE OR REPLACE TABLE raw.{table_name} AS 
            SELECT * FROM read_csv_auto('{file_path}', header=true);
        """
        
        con.execute(load_sql)
        
        # Quick validation: count rows
        count = con.execute(f"SELECT COUNT(*) FROM raw.{table_name};").fetchone()[0]
        print(f"-> Successfully loaded {count} rows into raw.{table_name}.")

    # Close the connection
    con.close()
    print("\nData loading complete! Database saved to:", DB_FILE)

if __name__ == "__main__":
    load_data()