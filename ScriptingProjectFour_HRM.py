"""
Title: IT 338 Scripting Project Four
Author: Hannah Rose Morgenstein
Course: IT 338 - Python for ArcGIS
Date: 02-02-2025
Project: Scripting Project Four

Description:
This Python script calculates the population difference for U.S. counties between
1990 and 2010. It creates a new field `POP_DIFF` in the table `US_Population_by_County`
and writes the difference (`POP_2010 - POP_1990`) to the new field. The script handles
missing or null values by defaulting them to 0 before performing calculations.

Workflow:
1. Define the workspace and input table path.
2. Set up the ArcPy environment for overwriting outputs.
3. Add a new field `POP_DIFF` if it does not already exist.
4. Use an Update Cursor to iterate through table rows, calculate the population difference,
   and update the new field.
5. Implement error handling to capture both ArcPy and Python errors, displaying useful messages.

Issues and Limitations:
- Ensuring that the dataset contains valid numeric values in the population fields.
- Handling null or missing values by treating them as zero.
- The script includes exception handling to catch and manage ArcPy and general Python errors.
"""


# Import the ArcPy module
import arcpy

# Define the full path for the workspace and table
workspace = r"U:\Documents\US_Population_by_County_Map_for_ProjectFour\Default.gdb"
table = workspace + r"\US_Population_by_County"

# Check if the workspace exists
print(f"Workspace exists: {arcpy.Exists(workspace)}")

# Check if the table exists
print(f"Table exists: {arcpy.Exists(table)}")

# Set environment workspace
arcpy.env.workspace = workspace
arcpy.env.overwriteOutput = True  # Allow overwriting output files

try:
    # Step 1: Add a new field for population difference if it doesn't exist
    field_name = "POP_DIFF"  # Name of the new field to store the population difference
    existing_fields = [f.name for f in arcpy.ListFields(table)]  # Get the existing fields in the table

    # If the field doesn't exist, create it
    if field_name not in existing_fields:
        arcpy.AddField_management(table, field_name, "LONG")  # Add field to store difference as a long integer
        print(f"Field '{field_name}' added successfully.")
    else:
        # If the field exists, print a message and proceed with the calculation
        print(f"Field '{field_name}' already exists. Proceeding to calculations.")

    # Step 2: Use an Update Cursor to calculate and populate the field
    updated_rows = 0  # Counter for the number of rows updated with population difference

    # Use an UpdateCursor to iterate through each row and calculate the population difference
    with arcpy.da.UpdateCursor(table, ["Resident_population_1990", "Resident_population_2010", field_name]) as cursor:
        for row in cursor:
            try:
                # Step 2a: Handle None values for populations (set to 0 if missing)
                pop_1990 = row[0] if row[0] is not None else 0  # Default to 0 if 1990 population is None
                pop_2010 = row[1] if row[1] is not None else 0  # Default to 0 if 2010 population is None

                # Step 2b: Calculate the population difference and update the field
                row[2] = pop_2010 - pop_1990  # Calculate the difference between 2010 and 1990 populations

                # Update the row with the calculated population difference
                cursor.updateRow(row)
                updated_rows += 1  # Increment the updated rows counter
            except Exception as row_error:
                # Step 2c: Handle errors for specific rows (if any)
                print(f"Error processing row: {row_error}")

    # Print the number of rows that were updated
    print(f"Population difference calculated and updated for {updated_rows} rows.")

except arcpy.ExecuteError:
    # Handle any errors related to ArcPy functions or geospatial tasks
    print("ArcPy Error:", arcpy.GetMessages(2))
except Exception as e:
    # Handle general Python errors
    print("Error:", str(e))
finally:
    # Final message indicating the script has completed
    print("Script completed.")
