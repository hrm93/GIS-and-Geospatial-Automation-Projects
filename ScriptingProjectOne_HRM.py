# IT 338: Scripting Project One
# Name: Hannah Rose Morgenstein
# Date: 12th of January 2025
# Project: Collecting User Input and Printing Results
#
# Discussion:
# This script demonstrates collecting and validating user input in Python 2.7. It asks the user for their name,
# address, the number of years at the current address, and their housing status (rent or own). The script ensures
# input is valid by using error handling for numeric values and conditional checks for specific text input.
# Key features include:
# - The use of `raw_input` for gathering user data.
# - A `while` loop for error handling and input validation.
# - String formatting with `format()` to create a readable output.
# The script's primary goal is to ensure robust handling of user input and produce a formatted summary of the collected data.

# Collect input from the user.
name = input("Please enter your name: ")  # Collects the user's name.
address = input("Please enter your address: ")  # Collects the user's address.

# Validate numeric input for years at the current address
while True:
    try:
        years_at_address = int(input("How many years have you lived at your current address? "))
        break  # Exit loop if input is valid
    except ValueError:
        print("Invalid input. Please enter a whole number for the years at your current address.")

# Validate housing status input as 'rent' or 'own'
while True:
    housing_status = input("Do you rent or own your current residence? (Type 'rent' or 'own'): ").strip().lower()
    if housing_status in ["rent", "own"]:
        break  # Exit loop if input is valid
    else:
        print("Invalid input. Please type 'rent' or 'own'.")

# Combine and format the collected input into a single string using format() for improved readability.
output = "{}: {} - {} years at current address, {}er.".format(name, address, years_at_address, housing_status)

# Print the formatted output.
print("\nCollected User Information:")
print(output)

# End of script.