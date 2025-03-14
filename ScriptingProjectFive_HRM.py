import arcpy
import logging
import time

# ----------------------------------------------------------------------------------------------------------------------
# Name:        Hannah Rose Morgenstein
# Course:      IT 338 - Geospatial Programming
# Date:        02-09-2025
# Project:     Scripting Project Five - Wilderness Area Creation Tool
# Description:
#
# This script automates the creation of a wilderness area dataset for the National Park Service. Wilderness areas are defined
# as areas that are at least:
# - 100 feet away from trails
# - 500 feet away from campsites
# - 2,000 feet away from roads and railways
#
# The script follows these key steps:
# 1. **Set Workspace**: Specifies the location of the geodatabase containing necessary feature classes and prepares the environment.
# 2. **Validate Workspace**: Checks if the specified geodatabase exists, ensuring the script runs in the correct context.
# 3. **Buffer Creation**: Creates buffer zones around the specified features (trails, campsites, and roads/rails) at the given distances.
# 4. **Merge Buffers**: Merges all buffer feature classes into a single feature class, combining the areas of influence into one dataset.
# 5. **Erase Analysis**: Uses the `Erase` tool to subtract the merged buffers from the park boundaries, creating the final wilderness area feature class.
# 6. **Cleanup**: Deletes intermediate buffer and merged buffer feature classes to ensure a clean output environment.
#
# The final output is a feature class representing the wilderness areas, where only the areas of the park that are not buffered by
# trails, campsites, or roads/rails remain.
#
# The script is designed to be robust and includes logging functionality, error handling, and workspace validation to ensure smooth execution.
# ----------------------------------------------------------------------------------------------------------------------

# Configure logging for script progress and error tracking
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set workspace (location of geodatabase)
workspace = r"U:\\Documents\\ArcGIS\\Projects\\MyProjectFive - A data set showing wilderness areas for the National Park Service\\MyProjectFive - A data set showing wilderness areas for the National Park Service.gdb"
arcpy.env.workspace = workspace
arcpy.env.overwriteOutput = True  # Allow overwriting of existing outputs

# Validate workspace to ensure it exists
def validate_workspace():
    if not arcpy.Exists(workspace):
        logging.error("Workspace geodatabase does not exist or is invalid.")  # Log error if workspace doesn't exist
        exit()  # Exit the script if workspace is invalid
    logging.info("Workspace found.")  # Log success if workspace exists

# Get list of feature classes from the workspace
def get_feature_classes():
    feature_classes = arcpy.ListFeatureClasses()
    logging.info(f"Feature classes in workspace: {feature_classes}")  # Log the list of feature classes found in workspace
    return feature_classes

# Define required feature classes and buffer distances
required_fcs = {
    "Trails": "100 Feet",    # Buffer distance for Trails
    "Campsites": "500 Feet",  # Buffer distance for Campsites
    "roads_rails": "2000 Feet",  # Buffer distance for Roads and Rails
    "park_boundaries": None,  # No buffer needed for Park Boundaries
}

# Check if all required feature classes are present in the workspace
def check_required_data(feature_classes):
    missing_data = [fc for fc in required_fcs if fc not in feature_classes]  # List feature classes not found
    if missing_data:
        logging.error(f"Missing required feature classes: {missing_data}. Exiting script.")  # Log missing feature classes
        exit()  # Exit if any required feature class is missing
    logging.info("All required feature classes exist. Proceeding with analysis.")  # Log if all required feature classes are found

# Generate a unique wilderness feature class name based on existing names
def generate_wilderness_name(feature_classes):
    wilderness_base = "wilderness"
    existing_wilderness = [fc for fc in feature_classes if fc.startswith(wilderness_base)]  # List existing wilderness feature classes
    wilderness_numbers = [int(fc.replace(wilderness_base, "")) for fc in existing_wilderness if fc.replace(wilderness_base, "").isdigit()]  # Extract numbers from existing wilderness names
    next_number = max(wilderness_numbers, default=0) + 1  # Generate next available wilderness number
    return f"{wilderness_base}{next_number}"  # Return unique wilderness name

# Perform buffer analysis on the required feature classes
def buffer_analysis():
    buffer_fcs = {fc: f"buffer_{fc.lower()}" for fc in required_fcs if required_fcs[fc]}  # Create a dictionary of buffer feature class names
    for fc, dist in required_fcs.items():  # Iterate over each required feature class
        if dist:  # If a buffer distance is defined
            buffer_fc = buffer_fcs[fc]
            if arcpy.Exists(buffer_fc):  # If a buffer feature class already exists, delete it
                logging.info(f"Deleting existing {buffer_fc}...")  # Log buffer deletion
                arcpy.Delete_management(buffer_fc)
            try:
                logging.info(f"Creating buffer for {fc} ({dist})...")  # Log the buffer creation process
                arcpy.Buffer_analysis(fc, buffer_fc, dist, "FULL", "ROUND", "ALL")  # Perform buffer analysis
            except arcpy.ExecuteError:  # Handle any errors during buffer analysis
                logging.error(f"Buffer analysis for {fc} failed: {arcpy.GetMessages(2)}")  # Log any error messages from buffer analysis
    return buffer_fcs  # Return the dictionary of buffer feature classes

# Merge the buffer feature classes into one
def merge_buffers(buffer_fcs):
    merged_buffers_fc = "merged_buffers"
    try:
        logging.info("Merging buffer feature classes into a single dataset...")  # Log the merge operation
        arcpy.Merge_management(list(buffer_fcs.values()), merged_buffers_fc)  # Merge all buffer feature classes into a single feature class
    except arcpy.ExecuteError:  # Handle any errors during the merge operation
        logging.error(f"Merge operation failed: {arcpy.GetMessages(2)}")  # Log any error messages from merge operation
    return merged_buffers_fc  # Return the merged buffer feature class

# Create the wilderness feature class by erasing the buffers from the park boundaries
def create_wilderness(merged_buffers_fc, new_wilderness_fc):
    try:
        logging.info(f"Creating wilderness feature class: {new_wilderness_fc}...")  # Log creation of wilderness feature class
        arcpy.Erase_analysis("park_boundaries", merged_buffers_fc, new_wilderness_fc)  # Erase the buffers from park boundaries
    except arcpy.ExecuteError:  # Handle any errors during the erase operation
        logging.error(f"Wilderness area creation failed: {arcpy.GetMessages(2)}")  # Log any error messages from erase operation

# Clean up temporary buffer files and merged buffer feature class
def cleanup(buffer_fcs, merged_buffers_fc):
    for buffer_fc in buffer_fcs.values():
        if arcpy.Exists(buffer_fc):  # Check if buffer feature class exists before deleting
            arcpy.Delete_management(buffer_fc)  # Delete the buffer feature class
    if arcpy.Exists(merged_buffers_fc):  # Check if merged buffers exists before deleting
        arcpy.Delete_management(merged_buffers_fc)  # Delete merged buffer feature class
    logging.info("Cleanup completed.")  # Log the completion of cleanup process

# Main script execution
def main():
    start_time = time.time()  # Record the start time
    logging.info("Starting Wilderness Area Creation Tool...")  # Log start of script execution
    validate_workspace()  # Validate the workspace
    feature_classes = get_feature_classes()  # Get the feature classes in the workspace
    check_required_data(feature_classes)  # Check if all required data is present
    new_wilderness_fc = generate_wilderness_name(feature_classes)  # Generate a unique wilderness name
    buffer_fcs = buffer_analysis()  # Perform buffer analysis
    merged_buffers_fc = merge_buffers(buffer_fcs)  # Merge buffer feature classes into a single feature class
    create_wilderness(merged_buffers_fc, new_wilderness_fc)  # Create wilderness area by erasing buffers from park boundaries
    cleanup(buffer_fcs, merged_buffers_fc)  # Clean up temporary files
    logging.info(f"Script completed successfully. New wilderness dataset created: {new_wilderness_fc}")  # Log script completion
    logging.info(f"Total execution time: {round(time.time() - start_time, 2)} seconds")  # Log execution time

# Run the script
if __name__ == "__main__":
    main()  # Call main function to start the process
