#Author:Upuli
#Date:3rd of Dec,2024
#Student ID:20240882

# Task A: Input Validation

import pandas as pd

from utils import validate_date_input, validate_continue_input

def process_csv_data(file_path):
    """
    Processes the CSV data for the selected date using pandas and extracts:
    - Total vehicles
    - Total trucks
    - Total electric vehicles
    - Two-wheeled vehicles, and other requested metrics
    """
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None

    # Clean up column names and strings for robust comparisons
    df['VehicleType_lower'] = df['VehicleType'].astype(str).str.strip().str.lower()
    df['JunctionName_lower'] = df['JunctionName'].astype(str).str.strip().str.lower()
    df['travel_Direction_out_upper'] = df['travel_Direction_out'].astype(str).str.strip().str.upper()
    df['travel_Direction_in'] = df['travel_Direction_in'].astype(str).str.strip()
    df['travel_Direction_out'] = df['travel_Direction_out'].astype(str).str.strip()

    total_vehicles = len(df)
    
    # Base dictionary setup
    survey_outcomes = {
        "total_vehicles": total_vehicles,
        "total_trucks": int((df['VehicleType_lower'] == 'truck').sum()),
        "total_electric_vehicles": int((df['elctricHybrid'].astype(str).str.strip().str.lower() == 'true').sum()),
        "total_two_wheeled_vehicles": int(df['VehicleType_lower'].isin(['bicycle', 'motorcycle', 'scooter']).sum()),
        "busses_north_junction": int((
            (df['JunctionName_lower'] == 'elm avenue/rabbit road') & 
            (df['travel_Direction_out_upper'] == 'N') & 
            (df['VehicleType_lower'] == 'buss')
        ).sum()),
        "vehicle_no_turns": int((df['travel_Direction_in'] == df['travel_Direction_out']).sum()),
        "total_bicycle": int((df['VehicleType_lower'] == 'bicycle').sum()),
        "total_vehicles_over_speed_limit": int((pd.to_numeric(df['VehicleSpeed'], errors='coerce') > pd.to_numeric(df['JunctionSpeedLimit'], errors='coerce')).sum()),
        "only_elm_vehicles": int((df['JunctionName_lower'] == 'elm avenue/rabbit road').sum()),
        "only_hanley_vehicles": int((df['JunctionName_lower'] == 'hanley highway/westway').sum()),
        "scooter_elm": int((
            (df['VehicleType_lower'] == 'scooter') & 
            (df['JunctionName_lower'] == 'elm avenue/rabbit road')
        ).sum()),
    }

    # Weather conditions: rain hours
    df['Weather_lower'] = df['Weather_Conditions'].astype(str).str.strip().str.lower()
    rain_df = df[df['Weather_lower'].str.contains('rain', na=False)].copy()
    if not rain_df.empty:
        rain_df['hour'] = rain_df['timeOfDay'].str.split(':').str[0]
        rain_hours = set(rain_df['hour'].unique())
    else:
        rain_hours = set()
    
    survey_outcomes['rain_hours'] = rain_hours
    survey_outcomes['total_rain_hours'] = len(rain_hours)

    # Hourly counts for Hanley Highway specifically
    hanley_df = df[df['JunctionName_lower'] == 'hanley highway/westway'].copy()
    if not hanley_df.empty:
        hanley_df['hour'] = hanley_df['timeOfDay'].str.split(':').str[0]
        hourly_counts = hanley_df['hour'].value_counts()
        if not hourly_counts.empty:
            max_count = int(hourly_counts.max())
            peak_hours = hourly_counts[hourly_counts == max_count].index.tolist()
        else:
            max_count = 0
            peak_hours = []
    else:
        max_count = 0
        peak_hours = []

    survey_outcomes["hanley_peak_hour_count"] = max_count
    survey_outcomes["hanley_peak_hours"] = [f"{hour}:00-{int(hour)+1}:00" for hour in sorted(peak_hours)]
    survey_outcomes["highest_numbers_vehicles"] = max_count
    
    # Derived calculations
    survey_outcomes["avg_bicycle_per_hour"] = round(survey_outcomes["total_bicycle"] / 24)
    
    survey_outcomes["truck_percentage"] = 0
    if total_vehicles > 0:
        survey_outcomes["truck_percentage"] = round((survey_outcomes["total_trucks"] / total_vehicles) * 100)
        
    survey_outcomes["scooter_percentage_elm"] = 0
    if survey_outcomes["only_elm_vehicles"] > 0:
        survey_outcomes["scooter_percentage_elm"] = round((survey_outcomes["scooter_elm"] / survey_outcomes["only_elm_vehicles"]) * 100)

    return survey_outcomes


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
        file_path, _ = validate_date_input()  # call user input function
        survey_outcomes = process_csv_data(file_path)
        if survey_outcomes: #if outcomes contain data
            display_outcomes(survey_outcomes, file_path)
            save_results_to_file(survey_outcomes)  # Save results to a text file

        if not validate_continue_input(): #call continue_input function
            break #exit the programme
    