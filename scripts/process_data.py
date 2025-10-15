# scripts/process_data.py
import configparser
import pandas as pd
import sqlite3
import os

def load_initial_data(config):
    """Loads data from the raw CSV file into a new SQLite database."""
    
    # Read paths from the config file
    csv_path = config['Paths']['raw_data_csv']
    db_path = config['Paths']['database_path']
    
    # Ensure the data directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # Remove old database file if it exists to ensure a fresh start
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Removed old database at {db_path}")

    print(f"Loading data from {csv_path}...")
    try:
        df = pd.read_csv(csv_path)
        
        # Connect to SQLite and load the data
        conn = sqlite3.connect(db_path)
        df.to_sql('raw_road_signs', conn, if_exists='replace', index=False)
        conn.close()
        
        print(f"Successfully loaded {len(df)} records into 'raw_road_signs' table in {db_path}")
        return True
    except FileNotFoundError:
        print(f"Error: The file was not found at {csv_path}. Please check your config.ini.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def main():
    """Main function to run the data processing pipeline."""
    config = configparser.ConfigParser()
    config.read('scripts/config.ini')
    
    if load_initial_data(config):
        # We will add cleaning steps here later
        pass

if __name__ == "__main__":
    main()