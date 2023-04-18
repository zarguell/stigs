from stig_parser import convert_xccdf
import json
import os
import traceback

# Set the directory to search in
directory = "./U_SRG-STIG_Library_2023_01v1"

# Initialize an empty list to store the found XML files
xml_files = []

# Loop through all subdirectories of the directory
for root, dirs, files in os.walk(directory):
    # Loop through all files in the current directory
    for file in files:
        # Check if the file has a .xml extension
        if file.endswith(".xml"):
            # Add the file path to the list of XML files
            xml_files.append(os.path.join(root, file))

# Initialize an empty list to store any files that cause an error
error_files = []

# Loop through the list of XML files and extract the file name
for xml_file in xml_files:
    # Extract the file name, excluding the path and extension
    file_name = os.path.splitext(os.path.basename(xml_file))[0]
    # Print the file name
    print("Processing " + file_name)

    with open(xml_file, "r") as fh:
        raw_file = fh.read()

    ## PARSE XCCDF(XML) to JSON
    try:
        json_results = convert_xccdf(raw_file)
    except Exception as e:
        error_info = {}
        error_info["file"] = xml_file
        error_info["type"] = type(e).__name__
        error_info["message"] = str(e)
        error_info["stack_trace"] = traceback.format_exc()
        error_files.append(error_info)

    with open("./json/" + file_name + ".json", "w") as outfile:
        # Save the JSON object to the file
        json.dump(json_results, outfile)


with open("./json/error.log", "w") as f:
    f.write("Files that caused an error:\n")
    for error_file in error_files:
        f.write(f"{error_file['file']}: {error_file['type']}: {error_file['message']}\n")
        f.write(f"Stack Trace:\n{error_file['stack_trace']}\n")