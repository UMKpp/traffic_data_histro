#Author:Upuli
#Date:3rd of Dec,2024
#Student ID:20240882

# Task A: Input Validation

import csv

def leap_year(year): #calculate leap years
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
    file_path = f"traffic_data{day:02d}{month:02d}{year}.csv"
    print(f"Generated file path: {file_path}")
    print("\n***********************************************")
    return file_path  # Return the file path

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

def process_csv_data(file_path):
    """
    Processes the CSV data for the selected date and extracts:
    - Total vehicles
    - Total trucks
    - Total electric vehicles
    - Two-wheeled vehicles, and other requested metrics
    """
    
    survey_outcomes = {
        "total_vehicles": 0,
        "total_trucks": 0,
        "total_electric_vehicles": 0,
        "total_two_wheeled_vehicles": 0,
        "busses_north_junction": 0,
        "vehicle_no_turns": 0,
        "truck_percentage": 0,
        "avg_bicycle_per_hour": 0,
        "total_bicycle": 0,
        "total_vehicles_over_speed_limit": 0,
        "only_elm_vehicles": 0,
        "only_hanley_vehicles": 0,
        "scooter_percentage_elm": 0,
        "scooter_elm": 0,
        "scooter_percentage_elm": 0,
        "highest_numbers_vehicles": 0,
        "hanley_peak_hour_count": 0,
        "hanley_peak_hours": [],
        "total_rain_hours": 0,
        "rain_hours": set(),  # Use a set to track unique rain hours
    }
    
    hourly_count = {} #a dictionary to store hours
    #hanley_hourly_count = {} a dictionary to store hours
    #elm_hourly_count = {} a dictionary to store hours

    try:
        #open the csv file in read mode
        with open(file_path, mode='r', encoding='utf-8') as file:
            #another dictionary to read rows as dicts
            reader = csv.DictReader(file)
            
            # Iterate through each row in the CSV file
            for row in reader:
                # Count total vehicles
                survey_outcomes["total_vehicles"] += 1

                # Count total trucks
                if row["VehicleType"].strip().lower() == "truck":
                    survey_outcomes["total_trucks"] += 1
                    
                # Count bicycles
                if row["VehicleType"].strip().lower() == "bicycle":
                    survey_outcomes["total_bicycle"] += 1

                # Count total electric vehicles
                if row["elctricHybrid"].strip().lower() == "true":
                    survey_outcomes["total_electric_vehicles"] += 1

                # Count total two-wheeled vehicles
                if row["VehicleType"].strip().lower() in ["bicycle", "motorcycle", "scooter"]:
                    survey_outcomes["total_two_wheeled_vehicles"] += 1
                
                # Count buses leaving Elm Avenue/Rabbit Road heading north
                if (
                    row["JunctionName"].strip() == "Elm Avenue/Rabbit Road" and
                    row["travel_Direction_out"].strip().upper() == "N" and
                    row["VehicleType"].strip().lower() == "buss"
                ):
                    survey_outcomes["busses_north_junction"] += 1

                # Count vehicles not turning left or right
                if row["travel_Direction_in"].strip() == row["travel_Direction_out"].strip():
                    survey_outcomes["vehicle_no_turns"] += 1

                # Count vehicles over speed limit
                if float(row["VehicleSpeed"]) > float(row["JunctionSpeedLimit"]):
                    survey_outcomes["total_vehicles_over_speed_limit"] += 1
                
                # Count only Elm Avenue/Rabbit Road vehicles
                if row["JunctionName"].strip().lower() == "elm avenue/rabbit road":
                    survey_outcomes["only_elm_vehicles"] += 1
                
                # Count only Hanley Highway/Westway vehicles
                if row["JunctionName"] == "Hanley Highway/Westway":
                    survey_outcomes["only_hanley_vehicles"] += 1
                    
                # Count scooters at Elm Avenue/Rabbit Road
                if (row["VehicleType"].strip().lower() == "scooter")and (row["JunctionName"].strip().lower() == "elm avenue/rabbit road"):
                   survey_outcomes["scooter_elm"] += 1
                
                # Check for rain condition and extract the hour
                weather_condition = row["Weather_Conditions"].strip().lower()
                if "rain" in weather_condition:  # Check if it's "Light rain" or "Heavy rain"
                    hour = row["timeOfDay"].split(":")[0]  # Extract the hour part
                    survey_outcomes["rain_hours"].add(hour)  # Add the hour to the set
                
                # Calculate the busiest hour(s)
                hour = row["timeOfDay"].split(":")[0]
                hourly_count[hour] = hourly_count.get(hour, 0) + 1

            # Determine the busiest hour
            max_count = max(hourly_count.values(), default=0)
            survey_outcomes["hanley_peak_hour_count"] = max_count
            survey_outcomes["hanley_peak_hours"] = [
                f"{hour}:00-{int(hour)+1}:00"
                for hour, count in hourly_count.items()
                if count == max_count         
            ]
            
            # Calculate highest vehicle count in hanley in an hour
            survey_outcomes["highest_numbers_vehicles"] = max_count
            
        #calculate average of bicycle
            
        survey_outcomes["avg_bicycle_per_hour"] = round(survey_outcomes["total_bicycle"]/ 24)
            
            
        #calculate truck precentage  
        if survey_outcomes["total_vehicles"] > 0:
            survey_outcomes["truck_percentage"] = round((survey_outcomes["total_trucks"] / survey_outcomes["total_vehicles"]) * 100)
            
        # Calculate percentage of scooters at Elm Avenue/Rabbit Road
        if survey_outcomes["only_elm_vehicles"] > 0:
            survey_outcomes["scooter_percentage_elm"] = round((survey_outcomes["scooter_elm"] / survey_outcomes["only_elm_vehicles"]) * 100)

        # Calculate total rain hours
        survey_outcomes["total_rain_hours"] = len(survey_outcomes["rain_hours"])

    except FileNotFoundError:  #handle the fileNotFoundError
        print(f"Error: File '{file_path}' not found.")
        return None
    return survey_outcomes #return outcomes


def display_outcomes(survey_outcomes, file_path):
    """
    Displays the calculated outcomes in a clear and formatted way.
    """
    if survey_outcomes: #check survey outcomes data
        print(f"Data file selected is {file_path}") #display selected file name
        
        #display total vehicles
        print(f"\u2022 The total number of vehicles recorded for this date is {survey_outcomes['total_vehicles']}")
        
        #display total trucks
        print(f"\u2022 The total number of trucks recorded for this date is {survey_outcomes['total_trucks']}")
        
        #display total electric vehicles
        print(f"\u2022 The total number of electric vehicles for this date is {survey_outcomes['total_electric_vehicles']}")
        
        #display 2 wheeled vehicles
        print(f"\u2022 The number of two-wheeled vehicles for this date is {survey_outcomes['total_two_wheeled_vehicles']}")
        
        #display busses leaving at north junction
        print(f"\u2022 The total number of Busses leaving Elm Avenue/Rabbit Road heading North is {survey_outcomes['busses_north_junction']}")
        
        #display vehicles without turn l/r
        print(f"\u2022 The total number of vehicles passing through both junctions without turning left or right is {survey_outcomes['vehicle_no_turns']}")
        
        #display truck percentage
        print(f"\u2022 The percentage of total vehicles recorded that are trucks for this date is {survey_outcomes['truck_percentage']}%")
        
        #display avg bicycle
        print(f"\u2022 The average number of Bicycle per hour for this date is {survey_outcomes['avg_bicycle_per_hour']}")
        
        #display vehicles over speed
        print(f"\u2022 The total number of vehicles recorded as over the speed limit for this date is {survey_outcomes['total_vehicles_over_speed_limit']}")
        
        #display only elm vehicles
        print(f"\u2022 The total number of vehicles recorded through Elm Avenue/Rabbit Road is {survey_outcomes['only_elm_vehicles']}")
        
        #display only hanley vehicles
        print(f"\u2022 The total number of vehicles recorded through Hanley Highway/Westway is {survey_outcomes['only_hanley_vehicles']}")
        
        #display scooter percentage
        print(f"\u2022 {survey_outcomes['scooter_percentage_elm']}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters")
        
        #display highest numbers vehicles
        print(f"\u2022 The highest number of vehicles in an hour on Hanley/Westway is {survey_outcomes['highest_numbers_vehicles']}")
        
        #display hanley peak hours
        print(f"\u2022 The most vehicles through Hanley Highway/Westway were recorded between {survey_outcomes['hanley_peak_hours']}")
        
        #display rain hours
        print(f"\u2022 The number of hours of rain hours for this date is {survey_outcomes['total_rain_hours']}")
        
    else: #handle the error
        print("Error: The file could not be processed.") 

# Task C: Save Results to Text File

def save_results_to_file(survey_outcomes, file_name="results.txt"):
               
    """
    Saves the processed outcomes to a text file and appends if the program loops.
    """
    
    #open the file in appenned mode and update new results continuously
    with open(file_name, 'a') as file:
        
        #write the file path
        file.write(f"\n\nData File: {file_path}\n")
        
        #write for each survey outcomes
        file.write(f"\u2022 The total number of vehicles recorded for this date is {survey_outcomes['total_vehicles']}\n")
        file.write(f"\u2022 The total number of trucks recorded for this date is {survey_outcomes['total_trucks']}\n")
        file.write(f"\u2022 The total number of electric vehicles for this date is {survey_outcomes['total_electric_vehicles']}\n")
        file.write(f"\u2022 The number of two-wheeled vehicles for this date is {survey_outcomes['total_two_wheeled_vehicles']}\n")
        file.write(f"\u2022 The total number of Busses leaving Elm Avenue/Rabbit Road heading North is {survey_outcomes['busses_north_junction']}\n")
        file.write(f"\u2022 The total number of vehicles passing through both junctions without turning left or right is {survey_outcomes['vehicle_no_turns']}\n")
        file.write(f"\u2022 The percentage of total vehicles recorded that are trucks for this date is {survey_outcomes['truck_percentage']}%\n")
        file.write(f"\u2022 The average number of Bicycle per hour for this date is {survey_outcomes['avg_bicycle_per_hour']}\n")
        file.write(f"\u2022 The total number of vehicles recorded as over the speed limit for this date is {survey_outcomes['total_vehicles_over_speed_limit']}\n")
        file.write(f"\u2022 The total number of vehicles recorded through Elm Avenue/Rabbit Road is {survey_outcomes['only_elm_vehicles']}\n")
        file.write(f"\u2022 The total number of vehicles recorded through Hanley Highway/Westway is {survey_outcomes['only_hanley_vehicles']}\n")
        file.write(f"\u2022 {survey_outcomes['scooter_percentage_elm']}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters\n")
        file.write(f"\u2022 The highest number of vehicles in an hour on Hanley/Westway is {survey_outcomes['highest_numbers_vehicles']}\n")
        file.write(f"\u2022 The most vehicles through Hanley Highway/Westway were recorded between {survey_outcomes['hanley_peak_hours']}\n")
        file.write(f"\u2022 The number of hours of rain hours for this date is {survey_outcomes['total_rain_hours']}\n")
        file.write(f"***********************************************************************************************\n")


if __name__ == "__main__":
    while True:
        file_path = validate_date_input()  # call user input function
        survey_outcomes = process_csv_data(file_path)
        if survey_outcomes: #if outcomes contain data
            display_outcomes(survey_outcomes, file_path)
            save_results_to_file(survey_outcomes)  # Save results to a text file

        if not validate_continue_input(): #call continue_input function
            break #exit the programme
    