import os
import json
import csv

# Function to flatten a rule into a dictionary
def flatten_rule(rule, prefix=""):
    rule_data = {}
    for key, value in rule.items():
        if isinstance(value, dict):
            flattened = flatten_rule(value, prefix + key + "_")
            rule_data.update(flattened)
        else:
            rule_data[prefix + key] = value
    return rule_data

# Input and output directories
input_dir = "json"
output_dir = "csv"

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Process each JSON file in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith(".json"):
        # Read the JSON file
        with open(os.path.join(input_dir, filename), "r") as json_file:
            data = json.load(json_file)

        # Combine metadata and rule attributes into a single header row
        header = list(data.keys())
        if "Rules" in header:
            header.remove("Rules")
            first_rule = data["Rules"][0]
            flattened_rule = flatten_rule(first_rule, "Rule_")
            header += flattened_rule.keys()

        # Define CSV filename
        csv_filename = os.path.splitext(filename)[0] + ".csv"

        # Write data to a CSV file with quotes around cells
        with open(os.path.join(output_dir, csv_filename), "w", newline="") as csv_file:
            writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
            
            # Write the header row
            writer.writerow(header)
            
            # Write the data rows
            if "Rules" in data:
                for rule in data["Rules"]:
                    flattened_rule = flatten_rule(rule, "Rule_")
                    row_data = [data.get(key, flattened_rule.get(key, "")) for key in header]
                    writer.writerow(row_data)

print("Conversion complete. CSV files have been saved in the 'csv' folder.")
