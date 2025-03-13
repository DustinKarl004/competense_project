import pandas as pd
import json
import os
import logging

# Configure logging
logging.basicConfig(filename='clean.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

logging.info("Script is running...")
print("Script is running...")

# Step 1: Read the existing CSV file
csv_file = "parameters1(Datafields).csv"
try:
    df = pd.read_csv(csv_file)
    logging.info("Existing CSV file read successfully.")
    print("Existing CSV file read successfully.")
except FileNotFoundError:
    logging.warning("Existing CSV file not found. Creating a new one.")
    print("Existing CSV file not found. Creating a new one.")
    df = pd.DataFrame(columns=[
        "section", "field", "type", "units", "description", "notes", 
        "constraints", "default", "example", "json_path", "status", "Review status"
    ])

# Step 2: Prompt the user to drop a file
try:
    file_path = input("Drop the file to read new sections and fields (provide the full path): ").strip("'\"")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")
except Exception as e:
    logging.error(f"Error: {e}")
    print(f"Error: {e}")
    exit()

# Step 3: Read the file based on its extension
if file_path.endswith(".json") or file_path.endswith(".ship"):  # Add support for .ship files
    logging.info("Reading JSON file...")
    print("Reading JSON file...")
    with open(file_path, "r") as f:
        new_data = json.load(f)
    logging.info("JSON file read successfully.")
    print("JSON file read successfully.")
else:
    logging.error("Unsupported file format. Please provide a JSON or .ship file.")
    print("Unsupported file format. Please provide a JSON or .ship file.")
    exit()

# Step 4: Function to auto-detect data type
def detect_type(value):
    if isinstance(value, int):
        return "int"
    elif isinstance(value, float):
        return "float"
    elif isinstance(value, str):
        return "str"
    elif isinstance(value, bool):
        return "bool"
    elif isinstance(value, list):
        return "list"
    elif isinstance(value, dict):
        return "dict"
    else:
        return "unknown"

# Step 5: Loop through the new data and add to the DataFrame if not already present
logging.info(f"New data: {new_data}")
print(f"New data: {new_data}")

for section, fields in new_data.items():
    logging.info(f"Processing section: {section}")
    print(f"Processing section: {section}")
    if isinstance(fields, dict):  # Ensure fields is a dictionary
        for field, value in fields.items():
            logging.info(f"Processing field: {field}")
            print(f"Processing field: {field}")
            if not ((df["section"] == section) & (df["field"] == field)).any():
                logging.info(f"Adding new row for section '{section}' and field '{field}'")
                print(f"Adding new row for section '{section}' and field '{field}'")
                data_type = detect_type(value)
                new_row = {
                    "section": section,
                    "field": field,
                    "type": data_type,
                    "units": "",
                    "description": "",
                    "notes": "",
                    "constraints": "",
                    "default": None,
                    "example": value,
                    "json_path": f"{section}.{field}",
                    "status": "active",
                    "Review status": "pending"
                }
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    else:
        logging.warning(f"Skipping section '{section}' because it is not a dictionary.")
        print(f"Warning: Skipping section '{section}' because it is not a dictionary.")

# Step 6: Sort the DataFrame by the 'section' column alphabetically
df = df.sort_values(by='section')

# Step 7: Save the updated DataFrame back to the same CSV file
df.to_csv(csv_file, index=False)
logging.info(f"Updated CSV file saved as '{csv_file}'.")
print(f"Updated CSV file saved as '{csv_file}'.")
