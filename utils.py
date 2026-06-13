import argparse

def get_cli_args():
    parser = argparse.ArgumentParser(description="Process traffic data for a specific date.")
    parser.add_argument('--date', nargs=3, type=int, metavar=('DD', 'MM', 'YYYY'),
                        help="Date of the survey (e.g. --date 15 06 2024)")
    args, _ = parser.parse_known_args()
    return args

def leap_year(year):
    """Calculate leap years."""
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

def validate_date_input():
    """
    Prompts the user for a date in DD MM YYYY format, validates the input for:
    - Correct data type
    - Correct range for day, month, and year
    """
    while True:  # Validate day
        try:
            day = int(input("Please enter the day of the survey in the format DD: "))
            if not (1 <= day <= 31):  # Check the day is in the valid range
                print("Day out of range. Please enter a value between 1 and 31.")
                continue
            break
        except ValueError: #error handelling
            print("Invalid input. Please enter a number for the day.")

    while True:  # Validate month
        try:
            month = int(input("Please enter the month of the survey in the format MM: "))
            if not (1 <= month <= 12):  # Check the month is in the valid range
                print("Month out of range. Please enter a value between 1 and 12.")
                continue
            break
        except ValueError: #error handelling
            print("Invalid input. Please enter a number for the month.")

    while True:  # Validate year
        try:
            year = int(input("Please enter the year of the survey in the format YYYY: "))
            if not (2000 <= year <= 2024):  # Check the year is in the valid range
                print("Year out of range. Please enter a value between 2000 and 2024.")
                continue
            break
        except ValueError: #error handelling
            print("Invalid input. Please enter a number for the year.")
            
    while True:
        # checking if the February is leap year or not 
        if month == 2:
            if leap_year(year) and day > 29: #conditions for being a leap year
                print("February in a leap year has only 29 days.")
                break
            elif not leap_year(year) and day > 28: #conditions for being a non leap year
                print("February has only 28 days in a non-leap year.")
                break
            
        elif month in [4, 6, 9, 11] and day > 30:
            print(f"The month {month} has only 30 days.") #prevent from misleading
            break
        elif day > 31:
            print(f"The month {month} has only 31 days.") #prevent from misleading
        else:
            break
        
    print("\n***********************************************")
    
    file_path = f"traffic_data{day:02d}{month:02d}{year}.csv" #filepath
    date = f"{day:02d}/{month:02d}/{year}" #date format
    
    print(f"Generated file path: {file_path}")
    print(f"Date:{date}")
    
    print("\n***********************************************")
    
    return file_path, date

def validate_continue_input():
    """
    Prompts the user to decide whether to load another dataset:
    - Validates "Y" or "N" input
    """
    while True:
        user_input = input("Do you want to add another dataset? 'Y' or 'N': ").strip().upper()
        if user_input == "Y":
            print("You chose to add another dataset.")
            print()
            return True
        elif user_input == "N":
            print("You chose to quit the program.")
            return False
        else:
            print("Invalid input. Please enter 'Y' or 'N'.")
