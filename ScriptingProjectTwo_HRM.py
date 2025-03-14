# IT 338: Scripting Project Two
# Name: Hannah Rose Morgenstein
# Date: 19th of January 2025
# Project: Collecting User Input and Printing Results
#
# Discussion:
# This script collects, validates, and analyzes user input for a residency data collection program.
# It prompts users to enter their name, address, the number of years at their current address,
# and their housing status (rent or own). The program ensures input validity through error handling
# and realistic boundary checks (e.g., residency years between 0-100).
#
# Key Features:
# - Robust input validation for text and numeric fields.
# - Real-time feedback for extreme residency values (e.g., short or long stays).
# - Statistical analysis, including total counts, averages, medians, modes, ranges, and standard deviations.
# - Modular design with separate functions for input collection, data processing, and results display.
# - User-friendly output with detailed records and summary statistics.
#
# Main Functions:
# - get_user_input: Gathers and validates user input, ensuring realistic values for years and housing status.
# - calculate_statistics: Computes statistical measures (mean, median, mode, range, and standard deviation).
# - print_summary_statistics: Displays a formatted summary of collected data, including totals and statistical measures.
# - main: Coordinates the program flow, including user prompts, data collection, and results display.
#
# Data Flow:
# - User input is collected and validated in `get_user_input`, then stored in lists for analysis.
# - Statistical calculations are performed on renter and owner data using `calculate_statistics`.
# - Summarized statistics and detailed records are displayed using `print_summary_statistics`.
#
# Challenges and Enhancements:
# - Handling empty datasets: Ensured calculations like mean or range return fallback values (e.g., 0 or N/A).
# - Enhancements: Added standard deviation for deeper insights and feedback for extreme residency years.
#
# The script's primary goals are to ensure robust input handling, improve user experience, and provide meaningful
# insights based on collected data. Its modular design allows for easy maintenance and scalability.


import numpy as np
from scipy import stats
from typing import List, Tuple, Optional, Union


def get_user_input() -> Optional[Tuple[str, str, int, str]]:
    """Handles user input and returns data for a single entry."""
    name = input("Please enter your name (or press Enter to finish): ").strip()
    if not name:
        return None  # Exit signal

    address = input("Please enter your address: ").strip()

    # Validate numeric input for years at the current address
    while True:
        try:
            years_at_address = int(input("How many years have you lived at your current address? "))
            if 0 <= years_at_address <= 100:
                if years_at_address > 50:
                    print("Wow! You've lived there for a very long time!")
                elif years_at_address < 2:
                    print("That's a short stay so far!")
                break
            else:
                print("Please enter a realistic number of years (0-100).")
        except ValueError:
            print("Invalid input. Please enter a whole number for the years at your current address.")

    # Validate housing status input as 'rent' or 'own'
    while True:
        housing_status = input("Do you rent or own your current residence? (Type 'rent' or 'own'): ").strip().lower()
        if housing_status in {"rent", "own"}:
            break
        print("Invalid input. Please type 'rent' or 'own'.")

    print(f"Thank you, {name}! We recorded that you {'rent' if housing_status == 'rent' else 'own'} at {address} for {years_at_address} years.\n")
    return name, address, years_at_address, housing_status


def calculate_statistics(years: List[int]) -> Tuple[float, float, Union[int, str], Tuple[int, int], float]:
    """Calculates average, median, mode, range, and standard deviation for a list of years."""
    if not years:
        return 0.0, 0.0, "N/A", (0, 0), 0.0

    avg = np.mean(years)
    median = np.median(years)
    
    # Handle the mode properly
    mode_result = stats.mode(years, keepdims=False)
    mode = mode_result.mode if mode_result.count > 0 else "N/A"
    
    range_years = (min(years), max(years))
    
    # Calculate standard deviation only if there are at least 2 data points
    stdev = np.std(years, ddof=1) if len(years) > 1 else 0.0
    
    return avg, median, mode, range_years, stdev


def print_summary_statistics(total: int, renters: int, owners: int,
                             renter_stats: Tuple[float, float, Union[int, str], Tuple[int, int], float],
                             owner_stats: Tuple[float, float, Union[int, str], Tuple[int, int], float]) -> None:
    """Prints a formatted summary of collected data."""
    print("\nSummary of Collected Data:")
    print(f"{'Total Individuals':40}: {total}")
    print(f"{'Total Renters':40}: {renters}")
    print(f"{'Total Owners':40}: {owners}")

    print("\nStatistics for Renters:")
    print(f"{'Average Length of Residency':40}: {renter_stats[0]:.2f} years")
    print(f"{'Median Length of Residency':40}: {renter_stats[1]:.2f} years")
    print(f"{'Mode of Residency Years':40}: {renter_stats[2]}")
    print(f"{'Range of Residency Years':40}: {renter_stats[3][0]} to {renter_stats[3][1]} years")
    print(f"{'Standard Deviation of Residency':40}: {renter_stats[4]:.2f}")

    print("\nStatistics for Owners:")
    print(f"{'Average Length of Residency':40}: {owner_stats[0]:.2f} years")
    print(f"{'Median Length of Residency':40}: {owner_stats[1]:.2f} years")
    print(f"{'Mode of Residency Years':40}: {owner_stats[2]}")
    print(f"{'Range of Residency Years':40}: {owner_stats[3][0]} to {owner_stats[3][1]} years")
    print(f"{'Standard Deviation of Residency':40}: {owner_stats[4]:.2f}")


def main() -> None:
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

    # Calculate statistics
    renter_stats = calculate_statistics(renter_years)
    owner_stats = calculate_statistics(owner_years)

    # Print summary
    print_summary_statistics(len(data), len(renter_years), len(owner_years), renter_stats, owner_stats)

    # Print detailed records
    print("\nDetailed Records:")
    for i, record in enumerate(data, start=1):
        print(f"{i}. {record[0]}: {record[1]} - {record[2]} years at current address, {record[3]}er.")

    print("\nThank you for using the Residency Data Collection Program!")


if __name__ == "__main__":
    main()