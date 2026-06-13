#Author:Upuli
#Date:23rd of Dec,2024
#Student ID:20240882

# Task A: Input Validation

import pandas as pd
import tkinter as tk

canvas_width = 1400
canvas_height = 650

def leap_year(year): #calculate leap years
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

def validate_date_input():
    
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
    
    print(f"Generated file path: {file_path}") #display the path of histogram
    print(f"Date:{date}")
    
    print("\n***********************************************")
    
    return file_path , date  # Return the file path

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
        self.root = tk.Tk() #tkinter root window

    def setup_window(self):
        self.root.title("Traffic Data Histogram") #setup window title

    def draw_histogram(self):
        global canvas_width, canvas_height
        
        #create a canvas for drawing the histogram
        self.canvas = tk.Canvas(self.root, width = canvas_width, height = canvas_height, bg = "white")
        self.canvas.pack()
        
        #title of the histogram
        self.canvas.create_text(
            canvas_width // 2, 20,
            text = f"Histogram of Vehicle Frequency per Hour ({self.date})",
            font = ("Arial",16,"bold"),
            fill = "black"
            )
        
        #determine the maximum vehicle count for scaling the bars
        max_count = max(
            max(self.hanley_data.values(), default = 0),
            max(self.elm_data.values(), default = 0)
            )       
        
        #bar and  gaps
        bar_width = 20
        gap_width = 15
        x_start = 50
        
        #define the range of x axis
        hours = [f"{h:02d}" for h in range(24)]
        
        for i, hour in enumerate(hours) :
            #hanley data
            hanley_count = self.hanley_data.get(hour, 0)
            bar_height_hanley = (hanley_count / max_count) * (canvas_height - 100)
            x0_hanley = x_start + i * (2 * bar_width + gap_width)
            y0_hanley = canvas_height - bar_height_hanley - 50
            x1_hanley = x0_hanley + bar_width
            y1_hanley = canvas_height - 50
            self.canvas.create_rectangle(x0_hanley, y0_hanley, x1_hanley, y1_hanley, fill = "#4682B4", outline = "black")
            self.canvas.create_text(x0_hanley + bar_width // 2, y0_hanley - 10, text = str(hanley_count), anchor = "s", fill = "#4682B4")
            
            #elm data
            elm_count = self.elm_data.get(hour, 0)
            bar_height_elm = (elm_count / max_count) * (canvas_height - 100)
            x0_elm = x_start + i * (2 * bar_width + gap_width) + bar_width +2
            y0_elm = canvas_height - bar_height_elm - 50
            x1_elm = x0_elm + bar_width
            y1_elm = canvas_height - 50
            self.canvas.create_rectangle(x0_elm, y0_elm, x1_elm, y1_elm, fill = "#87CEEB", outline = "black")
            self.canvas.create_text(x0_elm + bar_width // 2, y0_elm - 10, text = str(elm_count), anchor = "s", fill = "#87CEEB")
        
        #add hour labels to the x axis
        for i, hour in enumerate(hours):
            self.canvas.create_text(
                x_start + i * (2 * bar_width + gap_width ) + bar_width // 2, canvas_height - 40, text = hour, anchor = "n"
                )
        #add labels  
        self.canvas.create_text(canvas_width // 2, canvas_height - 10, text = "Hours", anchor = "s")
        self.canvas.create_text(20, canvas_height // 2, text = "Vehicle Count", anchor = "w", angle = 90)
        #add a line for the x axis 
        self.canvas.create_line(70,600,1500,600)

    def add_legend(self):
        #draw legend for the histogram
        legend_x = canvas_width - 200
        legend_y = 50
        self.canvas.create_rectangle(legend_x, legend_y, legend_x + 20, legend_y + 20, fill = "#4682B4", outline = "black")
        self.canvas.create_text(legend_x + 30, legend_y + 10, text = "Hanley Highway / Westway", anchor = "w")
        self.canvas.create_rectangle(legend_x, legend_y +30, legend_x + 20, legend_y + 50, fill = "#87CEEB", outline = "black")
        self.canvas.create_text(legend_x + 30, legend_y + 40, text = "Elm Avenue / Rabbit Road", anchor = "w")

    def run(self):
        #call functions under the main function
        self.setup_window()
        self.draw_histogram()
        self.add_legend()
        self.root.mainloop()

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
        while True: #loop user needs to input another dataset
            user_input = input("Do you want to add another dataset? 'Y' or 'N': ").strip().upper()
            if user_input == "Y":
                print("You chose to add another dataset.")
                print() #readability
                return True
            elif user_input == "N":
                print("You chose to quit the program.")
                return False
            
            else:
                print("Invalid input. Please enter 'Y' or 'N'.")

if __name__ == "__main__": 
    processor = MultiCSVProcessor() #create an instance of the multiCSVprocessor class
    processor.handle_user_interaction() #start handling user interaction for processing files
