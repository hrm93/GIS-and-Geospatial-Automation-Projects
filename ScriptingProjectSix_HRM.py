import arcpy
import os
import logging

# Project: IT 338 - Scripting Project Six
# Author: Hannah Rose Morgenstein
# Date: 2025-02-16
#
# Description:
#   This script processes a list of coordinate data from a text file to create polygons representing property boundaries.
#   Coordinates are grouped by unique property ID, and polygons are created using these coordinates. These polygons
#   are then inserted into a new feature class. The script also writes the names of the polygons to an output text file.
#   A projection file (properties.prj) is used for spatial reference to align the data.
#
#   The script performs error checking, ensuring that only valid coordinate data is processed. Any errors, such as
#   invalid file paths or non-numeric coordinate data, are caught and reported with helpful messages for debugging.
#
# Dependencies:
#   - Python 3.11
#   - ArcPy (ArcGIS 10.8)
#
# Usage:
#   Run this script in an ArcGIS Python environment.
#   Ensure the input text file is formatted as [ID, Name, X, Y], where X and Y are numeric coordinates.
#   The script requires a projection file (properties.prj) for correct spatial referencing.
#
# Key Functions:
#   - Reads coordinate data from a text file and groups them by unique ID.
#   - Creates polygons from the coordinate data and inserts them into a feature class.
#   - Writes feature names to an output text file.
#
# Error Handling:
#   - Checks for existence of input file and output directory; raises an error if missing.
#   - Handles invalid or non-numeric coordinates by skipping the erroneous entries.
#   - Catches errors during feature class creation or insertion, providing detailed messages to help debug.
#
# Issues Encountered:
#   - Handling of non-numeric coordinate data in the input file required special attention. Errors are handled by
#     skipping the problematic entries.
#   - Managing spatial reference was challenging due to the need to align the feature class with the provided data.
#
# Notes:
#   - Ensure all input files are in the correct format and required files (e.g., projection file) are accessible.
#   - Check the output directory before running the script to avoid write errors.
#
# Style and Structure:
#   - The script follows Python best practices, including proper indentation and meaningful variable names.
#   - Error handling is implemented through try-except blocks to gracefully handle issues.
#   - The code is modular for clarity and future modifications.
#
# Version History:
#   - v1.0: Initial version to read coordinates, create polygons, and insert into feature class.
#   - v1.1: Added error handling for missing files and data format issues.
#   - v1.2: Enhanced comments and structure for better clarity.
#   - v1.3: Improved file path handling and error reporting.
#   - v1.4: Fixed duplicate entries for property IDs by grouping coordinates and ensuring each ID is processed once.
#   - v1.5: Added dynamic logging using the Python logging module for more flexible reporting and output.


# Setup logging
# Log file will capture all messages from INFO level and above (INFO, WARNING, ERROR)
log_file = r"U:\Documents\module_6_data\script_log.txt"

# Ensure the log file directory exists before starting logging
log_directory = os.path.dirname(log_file)
if not os.path.exists(log_directory):
    os.makedirs(log_directory)  # Create the directory if it does not exist

# Configuring the logging mechanism to log into the specified file with desired format
logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Log the starting point of the script execution
logging.info('Starting script execution.')

# Set the workspace to the geodatabase
# This defines where the script will work and store output data
arcpy.env.workspace = r"U:\Documents\ArcGIS\Projects\MyProjectSix\MyProjectSix.gdb"
arcpy.env.overwriteOutput = True  # Allow overwriting existing outputs

# Output text file path to store feature names (properties)
output_text_file = r"U:\Documents\module_6_data\FeatureNames.txt"

# Check if the output directory exists, and create it if it doesn't
output_directory = os.path.dirname(output_text_file)
if not os.path.exists(output_directory):
    logging.error(f"Error: Output directory does not exist: {output_directory}")  # Log error if directory is missing
    raise FileNotFoundError(f"Output directory not found: {output_directory}")  # Raise an error to stop execution

# Write feature names to output text file
try:
    with open(output_text_file, 'w') as OutputText:
        # Use a SearchCursor to access the 'Name' field from the provided feature class
        with arcpy.da.SearchCursor("Provided_Property_FC", ["Name"]) as cursor:
            for row in cursor:
                OutputText.write("{0}\n".format(row[0]))  # Write each property name to the text file
    logging.info("Feature names written to text file successfully.")  # Log success
except Exception as e:
    logging.error(f"Error writing to text file: {e}")  # Log any error in file writing
    raise  # Stop execution if an error occurs

# Check if feature class already exists, and create if not
fc = "Property"
if arcpy.Exists(fc):  # Check if the feature class already exists
    logging.warning(f"Feature class '{fc}' already exists. It will be overwritten.")  # Warn if feature class exists
else:
    logging.info(f"Feature class '{fc}' does not exist. It will be created.")  # Inform that feature class will be created

try:
    # Create feature class of type 'POLYGON' in the workspace with a specified spatial reference
    arcpy.management.CreateFeatureclass(arcpy.env.workspace, fc, "POLYGON", spatial_reference=r"U:\Documents\module_6_data\Property.prj")
except Exception as e:
    logging.error(f"Error creating feature class: {e}")  # Log error if feature class creation fails
    raise  # Stop execution if an error occurs

# Add a 'Name' field to the feature class to store property names
try:
    arcpy.management.AddField(fc, "Name", "TEXT")  # Add 'Name' field to store property names
except Exception as e:
    logging.error(f"Error adding 'Name' field: {e}")  # Log error if field addition fails
    raise  # Stop execution if an error occurs

# Read input text file for coordinates
input_text_file = r"U:\Documents\module_6_data\Property_Module_6.txt"

# Check if the input file exists before reading
if not os.path.exists(input_text_file):
    logging.error(f"Error: Input file not found: {input_text_file}")  # Log error if input file does not exist
    raise FileNotFoundError(f"Input file not found: {input_text_file}")  # Stop execution if file is missing

# Read coordinates from the input file, skipping the header line
try:
    with open(input_text_file, 'r') as infile:
        coords_list_with_header = [line.split() for line in infile]  # Read each line and split by whitespace
    coords_list = coords_list_with_header[1:]  # Remove the header line
except Exception as e:
    logging.error(f"Error reading input file: {e}")  # Log error if reading the file fails
    raise  # Stop execution if an error occurs

# Check if the Provided_Property_FC exists before proceeding
if not arcpy.Exists("Provided_Property_FC"):
    logging.error("Error: 'Provided_Property_FC' does not exist.")  # Log error if feature class doesn't exist
    raise FileNotFoundError("'Provided_Property_FC' not found.")  # Stop execution if missing

# Get spatial reference from the existing feature class to match the projection
try:
    spatial_reference = arcpy.Describe("Provided_Property_FC").spatialReference
except Exception as e:
    logging.error(f"Error accessing spatial reference from 'Provided_Property_FC': {e}")  # Log error if spatial reference access fails
    raise  # Stop execution if error occurs

# Create InsertCursor for inserting polygons into the feature class
try:
    cursor = arcpy.da.InsertCursor(fc, ["SHAPE@", "Name"])  # Insert polygons and their names into the feature class
except Exception as e:
    logging.error(f"Error creating InsertCursor: {e}")  # Log error if cursor creation fails
    raise  # Stop execution if error occurs

# Create a dictionary to group coordinates by property ID
property_coords = {}

# Group coordinates by property ID
for coords in coords_list:
    current_ID = coords[0]  # Property ID
    if current_ID not in property_coords:
        property_coords[current_ID] = []  # Create a new list for this property ID if not already present
    property_coords[current_ID].append(coords)  # Add coordinates to the corresponding property ID

# Process each property ID and create polygons
processed_ids = set()  # Set to keep track of processed property IDs
for current_ID, coords_group in property_coords.items():
    current_Name = coords_group[0][1]  # Take the first name from the coordinates list for the property
    array = arcpy.Array()  # Array to hold points for the polygon

    # Iterate through the coordinates for this property ID and create points
    for coords in coords_group:
        try:
            x_coord = float(coords[2])  # X coordinate
            y_coord = float(coords[3])  # Y coordinate
            array.add(arcpy.Point(x_coord, y_coord))  # Add point to the array
        except ValueError as ve:
            logging.warning(f"Error in coordinate data for ID '{coords[0]}' (Name: {coords[1]}): {ve}. Skipping this entry.")  # Log if invalid coordinates
            continue  # Skip invalid coordinates

    # Skip if this ID has already been processed
    if current_ID in processed_ids:
        continue

    # Create the polygon from the array of points
    polygon = arcpy.Polygon(array, spatial_reference)

    # Insert the new polygon into the feature class
    try:
        cursor.insertRow([polygon, current_Name])  # Insert polygon and name into the feature class
        processed_ids.add(current_ID)  # Mark this ID as processed
        logging.info(f"Polygon for property ID '{current_ID}' (Name: {current_Name}) added successfully.")  # Log success
    except Exception as e:
        logging.error(f"Error inserting row for ID '{current_ID}' (Name: {current_Name}): {e}")  # Log error if insertion fails
        continue  # Skip and proceed with next property

# Delete the cursor to release resources
del cursor
logging.info("Polygons created successfully.")  # Log that polygons were created successfully

# Final log entry marking the end of the script execution
logging.info('Script execution completed.')
