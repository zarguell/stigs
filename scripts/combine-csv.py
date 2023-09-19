import os
import csv

# Input directory containing individual CSV files
input_dir = "csv"

# Output combined CSV file
output_file = "U_SRG-STIG_Library.csv"

# Initialize a flag to check if the header has been written
header_written = False

# Open the output CSV file for writing
with open(output_file, "w", newline="") as combined_csv_file:
    csv_writer = csv.writer(combined_csv_file)

    # Iterate through each CSV file in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".csv"):
            csv_file_path = os.path.join(input_dir, filename)

            # Open and read the current CSV file
            with open(csv_file_path, "r") as current_csv_file:
                csv_reader = csv.reader(current_csv_file)
                
                # Skip the header row if it has already been written
                if header_written:
                    next(csv_reader)  # Skip the header row

                # Iterate through the rows in the current CSV and write to the combined CSV
                for row in csv_reader:
                    csv_writer.writerow(row)

            # Set the header_written flag to True after writing the header once
            header_written = True

print(f"Combined CSV file '{output_file}' has been created.")
