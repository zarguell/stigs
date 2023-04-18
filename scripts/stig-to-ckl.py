from stig_parser import generate_ckl, generate_ckl_file
import json
import os
import traceback

# Set the directory to search in
directory = "./zips"

# Initialize an empty list to store the found XML files
zip_files = []

# Loop through all subdirectories of the directory
for root, dirs, files in os.walk(directory):
    # Loop through all files in the current directory
    for file in files:
        # Check if the file has a .xml extension
        if file.endswith(".zip"):
            # Add the file path to the list of XML files
            zip_files.append(os.path.join(root, file))

# Initialize an empty list to store any files that cause an error
error_files = []

# Loop through the list of XML files and extract the file name
for zip_file in zip_files:
    # Extract the file name, excluding the path and extension
    file_name = os.path.splitext(os.path.basename(zip_file))[0]
    # Print the file name
    print("Processing " + file_name)

    ## PARSE XCCDF(XML) to JSON
    try:
        CHECKLIST_INFO ={
            "ROLE": "None",
            "ASSET_TYPE": "Computing",
            "HOST_NAME": "Test_Host",
            "HOST_IP": "1.2.3.4",
            "HOST_MAC": "",
            "HOST_FQDN": "test.hostname.dev",
            "TARGET_COMMENT": "",
            "TECH_AREA": "",
            "TARGET_KEY": "3425",
            "WEB_OR_DATABASE": "true",
            "WEB_DB_SITE": "true",
            "WEB_DB_INSTANCE": "true"
        }
        ckl_results = generate_ckl(zip_file, CHECKLIST_INFO)
        generate_ckl_file(ckl_results, "./ckl/" + file_name + ".ckl")
    except Exception as e:
        error_info = {}
        error_info["file"] = file_name
        error_info["type"] = type(e).__name__
        error_info["message"] = str(e)
        error_info["stack_trace"] = traceback.format_exc()
        error_files.append(error_info)


with open("./ckl/error.log", "w") as f:
    f.write("Files that caused an error:\n")
    for error_file in error_files:
        f.write(f"{error_file['file']}: {error_file['type']}: {error_file['message']}\n")
        f.write(f"Stack Trace:\n{error_file['stack_trace']}\n")