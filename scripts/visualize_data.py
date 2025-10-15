# scripts/visualize_data.py
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import os

def visualize_class_distribution():
    """
    Connects to the database, loads cleaned data, and generates a bar chart
    of the class distribution, saving it to the assets folder.
    """
    db_path = 'data/roadsigns.db'
    output_path = 'assets/class_distribution.png'

    if not os.path.exists(db_path):
        print(f"Error: Database not found at {db_path}. Please run process_data.py first.")
        return

    # Ensure the assets directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM cleaned_annotations", conn)
    conn.close()

    print(f"Loaded {len(df)} records for visualization.")

    plt.figure(figsize=(12, 6))
    df['class_id'].value_counts().sort_index().plot(kind='bar')
    plt.title('Distribution of Road Sign Annotations per Class')
    plt.xlabel('Class ID')
    plt.ylabel('Number of Annotations')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    # Save the plot to the assets folder
    plt.savefig(output_path)
    print(f"Chart saved successfully to {output_path}")

if __name__ == "__main__":
    # You may need to install matplotlib: pip install matplotlib
    visualize_class_distribution()