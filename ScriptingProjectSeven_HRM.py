import arcpy
import os
import datetime
import time

"""
Title: Export Virginia County Maps to PDF
Course: IT 338 - Geospatial Programming
Author: Hannah Rose Morgenstein
Date: 2025-03-02
Project: Scripting Project Seven

Description:
This script automates the process of exporting county maps from an ArcGIS Pro
project (.aprx) using the map series feature. It loops through all counties 
in Virginia and exports a separate PDF for each one.

How It Works:
1. The script opens an ArcGIS Pro project (.aprx) and retrieves the layout 
   named "Virginia Counties."
2. It ensures that the layout has a Map Series enabled.
3. The script loops through each page of the Map Series, setting the 
   current page to the county being processed.
4. It retrieves the county name from the field 'NAMELSAD00' and uses it 
   to name the exported PDF.
5. If the file already exists, the script skips exporting to avoid redundancy.
6. The script logs each step, including successful exports, skipped files, 
   and any errors encountered.
7. Execution time is recorded at the end to track performance.

Key Features and Enhancements:
- **Error Handling:** Ensures that missing APRX files, layouts, or required 
  fields do not crash the script.
- **Logging System:** Tracks script execution and errors in a log file for 
  easy debugging.
- **Efficiency:** Skips counties that have already been exported to save time.
- **Performance Tracking:** Measures execution time to optimize workflow.

Requirements:
- An ArcGIS Pro project (.aprx) with a layout containing an enabled map series.
- The layout must reference a feature class of county boundaries as the index layer.
- The project should include roads, streams, and towns layers.

This script is designed for automation and ensures that all county maps 
are exported efficiently with minimal manual intervention.
"""

# Get the current script directory to keep file paths flexible
script_dir = os.path.dirname(os.path.abspath(__file__))

# Workspace path
aprx_path = r"\\C-FSVR02-40113A.snhu-vdi.com\Folder Redirection\hannah.morgenstein\Documents\ArcGIS\Projects\MyProjectSeven\MyProjectSeven.aprx"
# Folder where PDFs will be stored
output_folder = r"\\C-FSVR02-40113A.snhu-vdi.com\Folder Redirection\hannah.morgenstein\Documents\ArcGIS\Projects\MyProjectSeven\Exports"
# Folder where PDFs will be stored
log_file_path = r"\\C-FSVR02-40113A.snhu-vdi.com\Folder Redirection\hannah.morgenstein\Documents\ArcGIS\Projects\MyProjectSeven\export_log.txt"

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Function to log messages to a file and print them to the console
def log_message(message):
    """Writes a timestamped message to the log file and prints it."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file_path, "a", encoding="utf-8") as log_file:  # Use UTF-8 encoding to avoid errors
        log_file.write(f"[{timestamp}] {message}\n")
    print(message)

# Track script execution time
start_time = time.time()

try:
    # Ensure the ArcGIS Pro project file exists
    if not os.path.exists(aprx_path):
        raise FileNotFoundError(f"ERROR: ArcGIS Pro project not found at {aprx_path}")

    # Open the ArcGIS Pro project
    aprx = arcpy.mp.ArcGISProject(aprx_path)

    # Retrieve the layout by name
    layouts = aprx.listLayouts("Virginia Counties")  # Ensure this matches the ArcGIS Pro layout name

    # Check if the layout exists
    if not layouts:
        raise ValueError("ERROR: Layout 'Virginia Counties' not found in the project.")

    layout = layouts[0]  # Access the first (and expected) layout
    map_series = layout.mapSeries  # Retrieve the map series from the layout

    # Ensure the map series is enabled before proceeding
    if map_series and map_series.enabled:
        log_message("✅ Map series is enabled and ready for export.")

        # Loop through each county in the map series
        for pageNum in range(1, map_series.pageCount + 1):
            map_series.currentPageNumber = pageNum  # Set the current map series page

            # Try to retrieve the county name, ensuring the expected field exists
            try:
                county_name = map_series.pageRow.NAMELSAD00  # Adjust this if your field name differs
            except AttributeError:
                log_message(f"❌ ERROR: Field 'NAMELSAD00' not found on page {pageNum}. Skipping.")
                continue  # Move to the next page if the field is missing

            # Define the output file path for the county's PDF
            pdf_path = os.path.join(output_folder, f"{county_name}.pdf")

            # Check if this county's PDF has already been exported
            if os.path.exists(pdf_path):
                log_message(f"⚠️ Skipping {county_name}, already exported. (Checked: {pdf_path})")
                continue  # Skip to the next county to save time

            # Try exporting the current page as a PDF
            try:
                layout.exportToPDF(pdf_path, resolution=300, image_quality="BEST")
                log_message(f"📄 Exported: {pdf_path}")
            except Exception as export_error:
                log_message(f"❌ ERROR exporting {county_name}: {export_error}")

    else:
        raise ValueError("ERROR: Map Series is not enabled. Check ArcGIS Pro settings.")

except Exception as e:
    # Catch and log any major script failures
    log_message(f"❌ ERROR: {str(e)}")

finally:
    # Cleanup ArcGIS Pro project object
    if 'aprx' in locals():
        del aprx

    # Calculate and log the total execution time
    elapsed_time = round(time.time() - start_time, 2)
    log_message(f"✅ All county maps have been processed. Total execution time: {elapsed_time} seconds.")