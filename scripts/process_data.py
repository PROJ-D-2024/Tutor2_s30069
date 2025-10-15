import configparser
import pandas as pd
import sqlite3
import os
import glob
from configparser import ConfigParser

def load_initial_data(config: ConfigParser) -> bool:
    """
    Scans the YOLO dataset structure, parses all .txt label files,
    and loads the consolidated data into an SQLite database.
    """
    dataset_root = config['Paths']['dataset_root']
    db_path = config['Paths']['database_path']
    
    db_dir = os.path.dirname(db_path)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)
        
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Removed old database at {db_path}")

    print(f"Scanning dataset at {dataset_root}...")
    
    all_annotations = []
    for split in ['train', 'test', 'valid']:
        labels_path = os.path.join(dataset_root, split, 'labels')
        
        if not os.path.isdir(labels_path):
            print(f"Warning: Directory not found, skipping: {labels_path}")
            continue

        txt_files = glob.glob(os.path.join(labels_path, '*.txt'))
        
        for txt_file in txt_files:
            base_name = os.path.basename(txt_file)
            image_name = os.path.splitext(base_name)[0]

            try:
                with open(txt_file, 'r') as f:
                    for line in f:
                        parts = line.strip().split()
                        if len(parts) == 5:
                            all_annotations.append({
                                'image_filename': image_name,
                                'dataset_split': split,
                                'class_id': int(parts[0]),
                                'x_center': float(parts[1]),
                                'y_center': float(parts[2]),
                                'width': float(parts[3]),
                                'height': float(parts[4])
                            })
            except Exception as e:
                print(f"Error reading file {txt_file}: {e}")

    if not all_annotations:
        print("Error: No annotations found. Please check the 'dataset_root' path in your config.ini.")
        return False
        
    df: pd.DataFrame = pd.DataFrame(all_annotations)
    
    conn = sqlite3.connect(db_path)
    df.to_sql('raw_annotations', conn, if_exists='replace', index=False)
    conn.close()
    
    print(f"Successfully loaded {len(df)} total annotations from {len(df['image_filename'].unique())} images.")
    return True


def clean_and_standardize_data(config: ConfigParser) -> None:
    """Connects to the DB, cleans the annotation data, and saves it."""
    db_path = config['Paths']['database_path']
    conn = sqlite3.connect(db_path)
    
    print("\nStarting data cleaning and validation...")
    
    df: pd.DataFrame = pd.read_sql_query("SELECT * FROM raw_annotations", conn)
    print(f"Original data has {len(df)} rows.")

    # This initial dropna ensures that any rows with null values from potential
    # file parsing errors are removed before further processing.
    df.dropna(inplace=True)

    # Step 1: Data Type Correction
    # It is crucial to enforce the correct data types for each column.
    # `class_id` must be an integer for classification, and bounding box
    # coordinates must be floats for precise calculations.
    df['class_id'] = df['class_id'].astype(int)
    for col in ['x_center', 'y_center', 'width', 'height']:
        df[col] = df[col].astype(float)
    print("Step 1: Verified data types.")

    # Step 2: Outliers and Duplicates
    # The YOLO format requires normalized coordinates to be within the [0, 1] range.
    # Any values outside this range are considered outliers or data entry errors and
    # must be removed to maintain data integrity for model training. Width and height
    # must also be positive values.
    initial_rows = len(df)
    df = df[
        (df['x_center'] >= 0) & (df['x_center'] <= 1) &
        (df['y_center'] >= 0) & (df['y_center'] <= 1) &
        (df['width'] > 0) & (df['width'] <= 1) &
        (df['height'] > 0) & (df['height'] <= 1)
    ]
    rows_removed = initial_rows - len(df)
    print(f"Step 2: Removed {rows_removed} rows with invalid bounding box values.")

    # Step 3: Remove Duplicate Entries
    # Duplicate rows (identical annotations for the same image) can bias a machine
    # learning model and skew analysis. We remove them to ensure that each
    # annotation is a unique data point.
    initial_rows = len(df)
    df.drop_duplicates(inplace=True)
    rows_removed = initial_rows - len(df)
    print(f"Step 3: Removed {rows_removed} duplicate annotations.")
    
    df.to_sql('cleaned_annotations', conn, if_exists='replace', index=False)
    conn.close()
    
    print(f"\nData cleaning complete. Saved {len(df)} cleaned records to 'cleaned_annotations' table.")


def main() -> None:
    """Main function to run the data processing pipeline."""
    config = configparser.ConfigParser()
    config.read('scripts/config.ini')
    
    if 'Paths' not in config or 'dataset_root' not in config['Paths']:
        print("Error: config.ini is missing 'dataset_root' in the [Paths] section.")
        return

    if load_initial_data(config):
        clean_and_standardize_data(config)

if __name__ == "__main__":
    main()