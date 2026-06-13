#Author:Upuli
#Date:23rd of Dec,2024
#Student ID:20240882

# Task A: Input Validation

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from utils import validate_date_input, validate_continue_input

# Task B: Processed Outcomes
def process_csv_data(file_path):
    survey_outcomes = {
        "hourly_count_hanley" : {}, #vehicles per hour at hanley
        "hourly_count_elm" : {}, #vehicles per hour at elm
    }
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except FileNotFoundError:
        print(f"Error file '{file_path}'not found.")
        return survey_outcomes
        
    # Clean up column values
    df['JunctionName_lower'] = df['JunctionName'].astype(str).str.strip().str.lower()
    df['hour'] = df['timeOfDay'].astype(str).str.split(':').str[0].str.zfill(2)

    # Hanley Highway
    hanley_df = df[df['JunctionName_lower'] == 'hanley highway/westway']
    survey_outcomes["hourly_count_hanley"] = hanley_df['hour'].value_counts().to_dict()

    # Elm Avenue
    elm_df = df[df['JunctionName_lower'] == 'elm avenue/rabbit road']
    survey_outcomes["hourly_count_elm"] = elm_df['hour'].value_counts().to_dict()
    
    #print processed data in shell - hanley
    print("Processed Data for Hanley:")
    for hour , count in sorted(survey_outcomes["hourly_count_hanley"].items()):
        print(f"Hour {hour} :00 - {count} ")
        
    print() #readability
    
    #print processed data in shell - elm
    print("Processed Data for Elm:")
    for hour , count in sorted(survey_outcomes["hourly_count_elm"].items()):
        print(f"Hour {hour} :00 - {count} ")
        
    return survey_outcomes

# Task C: Save Results
def save_results_to_file(survey_outcomes,file_path, file_name="results.txt"):
    try:
        #open the results file in append mode to add new results
        with open(file_name , 'a') as file:
            file.write(f"\n\nData File: {file_path}\n")
            file.write(f"\n"
                       )
            #write hourly count for hanley highway
            file.write("Hourly Vehicles Counts (Hanley:\n)")
            file.write(f"\n")
            for hour,count in sorted(survey_outcomes["hourly_count_hanley"].items()):
                file.write(f"{hour}:00 - {hour}:59: {count} \n")
                file.write(f"\n")
            
            #write hourly count for elm
            file.write("Hourly Vehicles Counts (Elm:\n)")
            file.write(f"\n")
            for hour,count in sorted(survey_outcomes["hourly_count_elm"].items()):
                file.write(f"{hour}:00 - {hour}:59: {count} \n")
                file.write(f"\n")
    except IOError: #handle errors
        print("Error: You're not able to write the results file.")

# Task D: Histogram Display

class HistogramApp:
    def __init__(self, hanley_data, elm_data, date):
        self.hanley_data = hanley_data #hourly data for hanley highway/westway
        self.elm_data = elm_data #hourly data for elm avenue/rabbit road
        self.date = date #date of the datas

    def run(self):
        hours = [f"{h:02d}" for h in range(24)]
        
        hanley_counts = [self.hanley_data.get(hour, 0) for hour in hours]
        elm_counts = [self.elm_data.get(hour, 0) for hour in hours]
        
        x = np.arange(len(hours))
        width = 0.35
        
        fig, ax = plt.subplots(figsize=(12, 6))
        rects1 = ax.bar(x - width/2, hanley_counts, width, label='Hanley Highway / Westway', color='#4682B4', edgecolor='black')
        rects2 = ax.bar(x + width/2, elm_counts, width, label='Elm Avenue / Rabbit Road', color='#87CEEB', edgecolor='black')
        
        ax.set_xlabel('Hours')
        ax.set_ylabel('Vehicle Count')
        ax.set_title(f"Histogram of Vehicle Frequency per Hour ({self.date})")
        ax.set_xticks(x)
        ax.set_xticklabels(hours)
        ax.legend()
        
        # Add labels on top of bars
        ax.bar_label(rects1, padding=3)
        ax.bar_label(rects2, padding=3)
        
        fig.tight_layout()
        plt.show()

# Task E: Code Loops to Handle Multiple CSV Files
class MultiCSVProcessor:
    def __init__(self):
        self.current_data = None #initialize the processor with no current data loaded

    def load_csv_file(self, file_path):
        #load and process the csv data from the file
        return process_csv_data(file_path)

    def clear_previous_data(self):
        #clear any previously loaded data
        self.current_data = None

    def handle_user_interaction(self):
        #main loop for handling user interaction and processing datasets
        while True:
            file_path, date = validate_date_input() #prompt user to enter a file path
            self.current_data = self.load_csv_file(file_path) #load and process csv file
            if self.current_data:
                save_results_to_file(self.current_data, file_path) #save the processed results to a file
                hanley_data = self.current_data["hourly_count_hanley"] #retrieve data for hanley 
                elm_data = self.current_data["hourly_count_elm"] #retrieve data for elm
                histogram_app = HistogramApp(hanley_data, elm_data, date) #initialize the histogram
                histogram_app.run()
            if not self.process_files(): #check if the user wants to process additional files
                break

    def process_files(self):
        return validate_continue_input()

if __name__ == "__main__": 
    processor = MultiCSVProcessor() #create an instance of the multiCSVprocessor class
    processor.handle_user_interaction() #start handling user interaction for processing files
