# scripts/showcase_bounding_box.py
import pandas as pd
import sqlite3
import os
from PIL import Image, ImageDraw
import configparser

def draw_bounding_box_example():
    """
    Loads a random annotation from the cleaned database, finds the corresponding
    image, draws the bounding box, and saves it as an example.
    """
    config = configparser.ConfigParser()
    config.read('scripts/config.ini')

    db_path = config['Paths']['database_path']
    image_root = config['Paths']['dataset_root'] # We need the path to the images
    output_path = 'assets/bounding_box_example.png'

    if not all([os.path.exists(db_path), os.path.isdir(image_root)]):
        print("Error: Database or dataset root path not found. Check config.ini and run process_data.py.")
        return

    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM cleaned_annotations", conn)
    conn.close()

    # Pick one random annotation
    random_annotation = df.sample(1).iloc[0]
    
    # Construct the full path to the image
    image_filename = random_annotation['image_filename'] + '.png' # Assuming images are .png
    split = random_annotation['dataset_split']
    image_path = os.path.join(image_root, split, 'images', image_filename)
    
    if not os.path.exists(image_path):
         # Handle the complex ".png.rf.xyz" filenames from the dataset
        image_glob_path = os.path.join(image_root, split, 'images', random_annotation['image_filename'] + '*')
        possible_files = glob.glob(image_glob_path)
        if not possible_files:
            print(f"Error: Image file not found for annotation: {random_annotation['image_filename']}")
            return
        image_path = possible_files[0]


    # Open the image with Pillow
    with Image.open(image_path) as img:
        draw = ImageDraw.Draw(img)
        img_width, img_height = img.size

        # Convert YOLO's normalized coordinates back to pixel coordinates
        x_center = random_annotation['x_center'] * img_width
        y_center = random_annotation['y_center'] * img_height
        box_width = random_annotation['width'] * img_width
        box_height = random_annotation['height'] * img_height

        # Calculate top-left and bottom-right corners
        x_min = x_center - (box_width / 2)
        y_min = y_center - (box_height / 2)
        x_max = x_center + (box_width / 2)
        y_max = y_center + (box_height / 2)

        # Draw the rectangle
        draw.rectangle([x_min, y_min, x_max, y_max], outline="red", width=3)
        
        # Save the result
        img.save(output_path)
        print(f"Bounding box example saved successfully to {output_path}")

if __name__ == "__main__":
    # You may need to install Pillow: pip install Pillow
    draw_bounding_box_example()