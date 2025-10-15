import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# Connect to the database you created
conn = sqlite3.connect('data/roadsigns.db')
df = pd.read_sql_query("SELECT * FROM cleaned_annotations", conn)
conn.close()

# Create a plot
plt.figure(figsize=(12, 6))
df['class_id'].value_counts().sort_index().plot(kind='bar')
plt.title('Distribution of Road Sign Classes in the Dataset')
plt.xlabel('Class ID')
plt.ylabel('Number of Annotations')
plt.grid(axis='y', linestyle='--')
plt.show()