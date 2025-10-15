---

## Tutor2: Road Sign Data Cleaning and Standardization

This part of the project focuses on cleaning and preparing a dataset of road signs for a future analysis or machine learning project.

### Database Source

The dataset is a mock CSV (`raw_road_signs.csv`) representing data collected for road sign analysis. It includes columns for image paths, sign types, GPS coordinates, and recording dates.

### Local Setup

1.  **Create a virtual environment and install dependencies:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install pandas
    ```
2.  **Create your configuration file:**
    - In the `scripts/` folder, create a file named `config.ini`.
    - Add the following content, adjusting the paths to match your local machine:
      ```ini
      [Paths]
      raw_data_csv = /path/on/your/machine/data/raw_road_signs.csv
      database_path = /path/on/your/machine/data/roadsigns.db
      ```
3.  **Run the script:**
    ```bash
    python scripts/process_data.py
    ```
