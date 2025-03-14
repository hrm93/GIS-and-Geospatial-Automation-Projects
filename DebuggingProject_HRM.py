"""IT 338: Debugging Exercise
Name: Hannah Rose Morgenstein
Date: 26th of January 2025
Project: Debugging and Listing Text Files

Discussion:
This script is designed to collect a list of `.txt` files from a specified directory called "SampleFolder" located in the user's "Documents" folder. It uses Python's `os` module to list files and filter out non-text files (such as `.docx` files). This script also handles potential errors, such as issues with the directory path, and prints out the list of `.txt` files found in the directory.

Steps:
1. The user must first create a folder in their "My Documents" directory called "SampleFolder".
2. Two text files, "TextFile1.txt" and "TextFile2.txt", must be created and saved in the "SampleFolder".
3. A Microsoft Word document, "WordFile.docx", should also be created in the same folder to test the filtering of non-text files.
4. The script then checks the directory for `.txt` files and outputs the results.

Key Features:
- Uses `os.listdir()` to read files in the directory.
- Filters the list to include only `.txt` files.
- Handles errors related to file access using a `try-except` block.
"""

import os  # Import the os module for interacting with the operating system

# Create an empty list to store the names of the text files found in the directory
AvailableReports = []

# Define the directory path, using a raw string to handle backslashes properly
directory = r'\\C-FSVR02-40113A.snhu-vdi.com\Folder Redirection\hannah.morgenstein\Documents\SampleFolder'  # Update the path to point to your "SampleFolder"

# Check if the directory exists before proceeding
if os.path.exists(directory):
    try:
        # Loop through all the entries in the specified directory
        for entry in os.listdir(directory):
            # Create the full file path by joining the directory and entry name
            full_path = os.path.join(directory, entry)

            # Check if the entry is a file and ends with ".txt"
            if os.path.isfile(full_path) and entry.endswith(".txt"):
                AvailableReports.append(entry)  # Add the file name to the list

        # Print the list of available text files found in the directory
        print(AvailableReports)  # This will print the list of .txt files found in the directory

        # Confirmation message after the script completes
        print("Script Completed Successfully")  # Indicates the script finished without errors

    # If an error occurs, print the error message
    except Exception as e:
        print("Error occurred while accessing the directory: %s" % e)

else:
    print("Error: The specified directory does not exist. Please check the path and try again.")

# Debugging Process Summary:
#
# Issues found:
# 1. **Missing Colon in 'for' Loop**:
#    The 'for' loop declaration had a missing colon (`:`) after it, which caused a syntax error.
# 2. **Incorrect 'print' Syntax**:
#    The 'print' statements were written incorrectly without parentheses, which is required in Python 2.7. The correct syntax is `print()` instead of `print[]` or `print""`.
#
# Changes made:
# 1. **Fixed the 'for' loop** by adding the missing colon (`:`).
# 2. **Corrected the 'print' statements** to use the proper parentheses for Python 2.7.
#
# The directory path was updated to correctly point to the "SampleFolder" in the user's "Documents" folder.
# This ensures that the script can access the folder where the `.txt` files are located.
#
# **Additional Fixes**:
# 1. **Redundant `.txt` check**: The original script had two identical conditions checking for `.txt` files.
#    I simplified this to one condition.
# 2. **Error Handling**: I added a check to ensure the directory exists before proceeding with file listing.
#    This prevents errors if the directory is not found.
#
# **Summary of the Final Script**:
# The script now:
# - Correctly lists all `.txt` files in the specified directory.
# - Provides feedback to the user if the directory does not exist.
# - Handles potential errors in a user-friendly way.
# - Outputs the list of found text files and prints a confirmation message upon successful completion.