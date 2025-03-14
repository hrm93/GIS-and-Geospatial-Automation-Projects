"""
IT 338: Scripting Project Three
Name: Hannah Rose Morgenstein
Date: 26th of January 2025
Project: Collecting User Input and Validating Data

Discussion:
This script is designed to collect user input regarding residency details and validate the data provided. It collects information such as:
- Name of the individual
- Address of residence
- Number of years the individual has lived at the current address
- Housing status (whether the individual rents or owns the property)

Key Features:
- **Input Validation for Years at Address**: The script ensures that the number of years the user has lived at the current address is a valid integer within the realistic range of 0 to 100. It provides feedback for values outside this range.
- **Handling Variations in Housing Status Input**: The script accounts for possible misspellings or variations in the words "rent" and "own" (e.g., "rnt", "0wn", "r@nt", etc.), using regular expressions for validation.
- **Real-time Feedback**: For extreme values of years at an address (e.g., too high or too low), the script provides user-friendly feedback, making the application more interactive.
- **Statistical Summary and Records**: Once data is collected, the script calculates various statistics (e.g., average, median, mode, range, and standard deviation) for renters and owners. It also provides a detailed summary and records of all collected data.
- **Error Logging**: Invalid inputs (e.g., non-numeric years or unrecognized housing statuses) are logged to an error log file ("error_log.txt") for later review.
- **Regex for Housing Status Validation**: The script uses flexible and streamlined regex patterns to handle various input forms for "rent" and "own".

The program ensures **robust data collection** while providing **user-friendly error handling** and feedback.

"""

import numpy as np
from scipy import stats
import re  # Regular expression module
import logging

# Configure logging for error tracking
logging.basicConfig(filename="error_log.txt", level=logging.ERROR, format="%(asctime)s - %(message)s")

def is_ascii(s):
    """Checks if a string contains only ASCII characters.

    This function ensures that the name provided by the user consists only of standard ASCII characters
    (no special characters or non-English alphabets).

    Args:
        s (str): The string to be checked.

    Returns:
        bool: True if the string contains only ASCII characters, False otherwise.
    """
    return all(ord(c) < 128 for c in s)

def is_valid_address(address):
    """Checks if an address contains valid characters (including special characters).

    The address is validated to ensure it follows the correct format, which includes allowing special characters.
    '#' is only valid if followed by digits.

    Args:
        address (str): The address provided by the user.

    Returns:
        bool: True if the address matches the allowed format, False otherwise.
    """
    # Ensure '#' is only valid when followed by numbers (at least one digit)
    return bool(re.match(r'^[\w\s,.\-()&]*#\d+[\w\s,.\-()&]*$|^[\w\s,.\-()&]+$', address))

# Mapping of common worded numbers to numeric equivalents
word_to_number = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
    "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19,
    "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60,
    "seventy": 70, "eighty": 80, "ninety": 90, "hundred": 100
}

def convert_worded_number(worded_number):
    """Converts a worded number (including hyphenated) to its numeric equivalent.

    Handles cases like "twenty-three", "sixty-five", etc.

    Args:
        worded_number (str): The worded number to be converted (e.g., "twenty-three").

    Returns:
        int: The numeric equivalent of the worded number, or None if invalid.
    """
    # Split the input if it contains a hyphen (for cases like "twenty-three")
    parts = worded_number.split('-')

    if len(parts) == 1:
        # If no hyphen, simply look up the number in the dictionary
        return word_to_number.get(parts[0], None)
    elif len(parts) == 2:
        # If it's hyphenated, look up each part and sum them
        first_part = word_to_number.get(parts[0], None)
        second_part = word_to_number.get(parts[1], None)

        if first_part is not None and second_part is not None:
            return first_part + second_part
    return None  # If invalid input or not found in the dictionary

def get_user_input():
    """Collects user input for their name, address, years at current address, and housing status.

    This function now also handles the input for years in both numeric and word form.
    """
    while True:
        name = raw_input("Please enter your name (or press Enter to finish): ").strip()
        if not name:
            return None  # Exit signal
        if len(name) > 100 or not is_ascii(name):
            logging.error("Invalid name input: %s", name)
            print("Invalid name. Please enter a shorter or valid name.")
            continue
        break

    while True:
        address = raw_input("Please enter your address: ").strip()
        if len(address) > 200 or not is_valid_address(address):
            logging.error("Invalid address input: %s", address)
            print("Invalid address. Please enter a valid address.")
            continue
        break

    # Validate input for years at the current address, accepting both numbers and spelled-out numbers
    while True:
        years_input = raw_input("How many years have you lived at your current address? ").strip().lower()

        try:
            # First check if the input is a numeric value
            years_at_address = int(years_input)
            if 0 <= years_at_address <= 100:
                if years_at_address > 50:
                    print("Wow! You've lived there for a very long time!")
                elif years_at_address < 2:
                    print("That's a short stay so far!")
                break
            else:
                print("Please enter a realistic number of years (0-100).")
        except ValueError:
            # If input is not a number, check if it's a worded number in the dictionary
            years_at_address = convert_worded_number(years_input)
            if years_at_address is not None and 0 <= years_at_address <= 100:
                if years_at_address > 50:
                    print("Wow! You've lived there for a very long time!")
                elif years_at_address < 2:
                    print("That's a short stay so far!")
                break
            else:
                print("Invalid input. Please enter a valid number for the years at your current address.")

    # Housing status validation (rent/own input)
    while True:
        housing_status = raw_input(
            "Do you rent or own your current residence? (Type 'rent' or 'own'): ").strip().lower()
        if re.match(r"^rent?$", housing_status):  # Matches "rent" or slight variations like "rnt"
            housing_status = "rent"
            break
        elif re.match(r"^o(w)?n$", housing_status):  # Matches "own" or slight variations like "own"
            housing_status = "own"
            break
        # Allow more variations like 0wn, r@nt, r$nt, 00wwn
        elif re.match(r"^[0o][a-z]*w[a-z]*n[a-z]*$", housing_status):  # Matches "0wn", "00wn", "00wwn"
            housing_status = "own"
            break
        elif re.match(r"^r[a-z]*n[a-z]*t[a-z]*$", housing_status):  # Matches "r@nt", "r$nt", "rnt"
            housing_status = "rent"
            break
        logging.error("Invalid housing status input: %s", housing_status)
        print("Invalid input. Please type 'rent' or 'own'.")

    print("\nThank you, {}! We recorded that you {} at {} for {} years.\n".format(
        name, "rent" if housing_status == "rent" else "own", address, years_at_address))

    return name, address, years_at_address, housing_status

def calculate_statistics(years):
    """Calculates average, median, mode, range, and standard deviation for a list of years.

    This function computes various statistical measures for the number of years individuals have lived at their current address.

    Args:
        years (list of int): A list containing the number of years for each individual (either renters or owners).

    Returns:
        tuple: A tuple containing:
            - avg (float): The average number of years.
            - median (float): The median number of years.
            - mode (str or int): The mode of the years (most frequent value).
            - range_years (tuple): The range (min, max) of the years.
            - stdev (float): The standard deviation of the years.
    """
    avg = np.mean(years) if years else 0
    median = np.median(years) if years else 0
    mode = stats.mode(years)[0][0] if years else "N/A"
    range_years = (min(years), max(years)) if years else (0, 0)

    # Handle case where there is only one data point (standard deviation is undefined)
    if len(years) > 1:
        stdev = np.std(years, ddof=1) if years else 0
    else:
        stdev = 0  # For a single data point, standard deviation is 0

    return avg, median, mode, range_years, stdev

def print_summary_statistics(total, renters, owners, renter_stats, owner_stats):
    """Prints a formatted summary of collected data, including overall statistics for renters and owners.

    This function prints detailed statistics for both renters and owners, including:
    - Average length of residency
    - Median length of residency
    - Mode of residency years
    - Range of residency years
    - Standard deviation of residency years

    Args:
        total (int): The total number of individuals.
        renters (int): The total number of renters.
        owners (int): The total number of owners.
        renter_stats (tuple): A tuple containing statistics for renters (average, median, mode, range, stdev).
        owner_stats (tuple): A tuple containing statistics for owners (average, median, mode, range, stdev).
    """
    print("\nSummary of Collected Data:")
    print("{:40s}: {}".format("Total Individuals", total))
    print("{:40s}: {}".format("Total Renters", renters))
    print("{:40s}: {}".format("Total Owners", owners))

    print("\nStatistics for Renters:")
    print("{:40s}: {:.2f} years".format("Average Length of Residency", renter_stats[0]))
    print("{:40s}: {:.2f} years".format("Median Length of Residency", renter_stats[1]))
    print("{:40s}: {}".format("Mode of Residency Years", renter_stats[2]))
    print("{:40s}: {} to {} years".format("Range of Residency Years", *renter_stats[3]))
    print("{:40s}: {:.2f}".format("Standard Deviation of Residency", renter_stats[4]))

    print("\nStatistics for Owners:")
    print("{:40s}: {:.2f} years".format("Average Length of Residency", owner_stats[0]))
    print("{:40s}: {:.2f} years".format("Median Length of Residency", owner_stats[1]))
    print("{:40s}: {}".format("Mode of Residency Years", owner_stats[2]))
    print("{:40s}: {} to {} years".format("Range of Residency Years", *owner_stats[3]))
    print("{:40s}: {:.2f}".format("Standard Deviation of Residency", owner_stats[4]))

def main():
    """Main function to drive the program. It collects data from the user, processes the data,
    calculates statistics for renters and owners, and then prints the summary and detailed records."""
    print("Welcome to the Residency Data Collection Program!\n")
    data = []
    renter_years = []
    owner_years = []

    while True:
        entry = get_user_input()
        if entry is None:  # Break loop on exit signal
            break
        data.append(entry)
        if entry[3] == "rent":
            renter_years.append(entry[2])
        else:
            owner_years.append(entry[2])

    # Calculate statistics for renters and owners
    renter_stats = calculate_statistics(renter_years)
    owner_stats = calculate_statistics(owner_years)

    # Print a summary of collected data:
    # - Total number of individuals
    # - Number of renters and owners
    # - Statistical summary (average, median, mode, etc.) for both renters and owners
    print_summary_statistics(len(data), len(renter_years), len(owner_years), renter_stats, owner_stats)

    # Print detailed records
    print("\nDetailed Records:")
    for i, record in enumerate(data, start=1):
        print("{}. {}: {} - {} years at current address, {}er.".format(
            i, record[0], record[1], record[2], record[3]))

    print("\nThank you for using the Residency Data Collection Program!")

if __name__ == "__main__":
    main()
# End of script.