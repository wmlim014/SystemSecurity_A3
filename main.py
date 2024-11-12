import numpy as np
import datetime
import json

# Declare variable needed
events = []
stats = []
num_of_events = 0
num_of_stats = 0
no_of_days = 10

# Declare and initializes variable needed for file generation
log_file_name = "logs.json"
analysis_file_name = "analysis_results.json"

# Read event file
def read_event_file(input_string):
    file_found = False
    global num_of_events
    file_name = input(input_string)

    while not file_found:
        try:
            with open(file_name, "r") as file:
                file_found = True # File found

                num_of_events = int(file.readline().strip()) # Initialize file number of events with first line
                
                # Read file content and store it
                for line in file:
                    data = (line.split(':'))

                    # Declare distionary for each event
                    event_dist = {
                        "event_name": data[0].strip(),
                        "event_type": data[1].strip()
                    }

                    # If the event is countinuous event
                    if(event_dist["event_type"] == 'C'):
                        event_dist["min"] = round(float(data[2].strip()), 2)
                        event_dist["max"] = round(float(data[3].strip()), 2)
                    
                    else: # If the event is discrete events
                        event_dist["min"] = int(data[2].strip())
                        event_dist["max"] = int(data[3].strip())

                    event_dist["weight"] = int(data[4].strip())
                    
                    events.append(event_dist)
                    # print(event_dist)  # Debug line

        except FileNotFoundError:
            print("File not found. Please check the file name and try again.")
            file_name = input(input_string)

# Read stat file
def read_stat_file(input_string):
    file_found = False
    global num_of_stats
    file_name = input(input_string)

    while not file_found:
        try:
            with open(file_name, "r") as file:
                file_found = True # File found

                num_of_stats = int(file.readline().strip()) # Initialize file number of stats with first line
                
                # Read file content and store it
                for line in file:
                    data = (line.split(':'))

                    # Declare distionary for each event
                    stat_dist = {
                        "event_name": data[0].strip(),
                        "mean": round(float(data[1].strip()), 2),
                        "std_deviation": round(float(data[2].strip()), 2)
                    }
                    
                    stats.append(stat_dist)
                    # print(stat_dist)  # Debug line

        except FileNotFoundError:
            print("File not found. Please check the file name and try again.")
            file_name = input(input_string)

# Step 1 and 2: Prompt user to input the file name
def load_file():
    read_event_file("Please enter the events file name: ")
    print("Step 1: Events file read completed, proceed to next step...")

    print()
    read_stat_file("Please enter the stats file name: ")
    print("Step 2: Stats file read for event generation completed. ")

# Step 3: 
# Check inconsistencies
def std_dvt_match_event_type(event, stat):
    match event['event_type']:
        case 'D':   # Standard deviation must be integer
            if not stat['std_deviation'].is_integer():
                print(f"Warning: {event['event_name']} is discrete but has a non-integer standard deviation.")
        
        case 'C':   # Standard deviation must be float
            if stat['std_deviation'].is_integer():
                print(f"Warning: {event['event_name']} is discrete but has an integer standard deviation.")

        case _:
            print(f"Warning: {event['event_name']} is not discrete and continuous.")
            reload_file()

# Check weight
def check_weight(event):
    # If the weight is not positive integer {1, 2, 3, ...}
    if int(event['weight']) <= 0:
        print(f"Warning: {event['event_name']} weight is not a positive integer.")
        reload_file()

def validate_min_max(event, min, max):

    if min > max:
        print(f"Warning: {event['event_name']} minimum value is bigger than the maximum value.")
        reload_file()

    elif min == max:
        print(f"Warning: {event['event_name']} minimum and maximum value are equal.")
        reload_file()

def reload_file():
    print("Please correct the last warning data before re-load the file...")
    load_file()

def check_data():

    print()
    for event in events:
        min = event['min']
        max = event['max']

        check_weight(event)
        validate_min_max(event, min, max)

        for stat in stats:
            # If current stats event name is equal to event event name...
            if event['event_name'] == stat['event_name']:
                # Check event type...
                std_dvt_match_event_type(event, stat)

# Step 4:
# Generate value for specific event
def generate_event_value(event, stat):
    mean = stat['mean']
    std_dev = stat['std_deviation']
    min_val = event['min']
    max_val = event['max']

    # If the event is continues respectively... 
    if event['event_type'] == 'C':
        value = np.random.normal(mean, std_dev, 1000)
        value = np.clip(value, min_val, max_val)  # Clip to range
        return round(np.random.choice(value), 2)
    
    # Else the event is discrete respectively...
    else:
        value = np.random.normal(mean, std_dev, 1000)
        value = np.clip(value, min_val, max_val)
        value = np.round(value).astype(int)  # Convert to integer
        return int(np.random.choice(value))

# Loop through all events and stats to generate the events value for days
def generate_events(no_of_days):
    all_days_data = []  # Declare empty list to store generated events
    global events, stats

    start_date = datetime.datetime.now() - datetime.timedelta(days=no_of_days)

    for i in range (no_of_days): # Loop the date from start date current date
        current_date = start_date + datetime.timedelta(days=i)
        generated_event_dict = {
            "date": current_date.strftime("%d %b %Y")
        }

        for event in events:
            for stat in stats:
                # If current stats event name is equal to event event name...
                if event['event_name'] == stat['event_name']:
                    event_value = generate_event_value(event, stat)
                    generated_event_dict[event['event_name']] = event_value
        all_days_data.append(generated_event_dict)
    return all_days_data

# Function to write the event into logs file
def write_log_file(generated_events):
    # Convert generated data into json format
    json_object = json.dumps(generated_events, indent = np.size(events))
    with open(log_file_name, "w") as outfile:
        outfile.write(json_object)

    print(f"Generated event data saved to {log_file_name}")

# Step 5
# Example of the generated data for 10 days
# {"date": "02 Nov 2024", "Logins": 2, "Time online": 122.71, "Emails sent": 6, "Emails opened": 6, "Emails deleted": 6}
def calculate_event_stats(all_days_data):
    event_statistics = {}
    # Extract event names from the first entry, ignoring the 'date' key
    event_names = [key for key in all_days_data[0].keys() if key != 'date']
    
    for event_name in event_names:
        # Gather all values for this event across all days into a list
        event_values = [day_data[event_name] for day_data in all_days_data]

        total = sum(event_values)
        mean = total / len(event_values)
        std_dev = np.std(event_values, ddof = 0)  # Population standard deviation

        # Store the calculated statistic result into dictionary
        event_statistics[event_name] = {
            "total": total, 
            "mean": round(mean, 2),
            "std_dev": round(std_dev, 2)   # Population standard deviation
        }
    
    return event_statistics

# Function to write analysis result
def write_analysis_file(event_stats):
    # Convert event_stats into json format
    json_object = json.dumps(event_stats, indent = 4)
    with open(analysis_file_name, "w") as outfile:
        outfile.write(json_object)

    print(f"Calculated statistics (total, mean, standard deviation) saved to {analysis_file_name}")

################
# MAIN PROGRAM #
################
load_file() # Step 1 and 2: Prompt user to input the file name

# Step 3
check_data()
input("Step 3: Inconsistencies check completed. Press enter to proceed next step...")

# Step 4
generated_events = generate_events(no_of_days)
write_log_file(generated_events)
print(json.dumps(generated_events, indent = np.size(events)))   # Debug line
input("Step 4: Event generation completed. Press Enter to proceed next step...")

# Step 5
event_stats = calculate_event_stats(generated_events)
write_analysis_file(event_stats)
print(json.dumps(event_stats, indent = 4))  # Debug line
input("Step 5: Calculated statistics printed completed. Press Enter to proceed next step...")