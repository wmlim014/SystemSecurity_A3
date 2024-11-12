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
alert_file_name = "alerts.json"

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
    if event["event_type"] == 'D':  # Standard deviation must be integer
        if not stat['std_deviation'].is_integer():
            print(f"Warning: {event['event_name']} is discrete but has a non-integer standard deviation.")
        
    elif event["event_type"] == 'C':   # Standard deviation must be float
        if stat['std_deviation'].is_integer():
            print(f"Warning: {event['event_name']} is discrete but has an integer standard deviation.")

    else:
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

# Step 9 to 10
# Calculate threshold
def calculate_threshold():
    sum_of_weight = 0
    for event in events:
        sum_of_weight += event['weight']

    return 2 * sum_of_weight

# Calculate anomaly counter
def calculate_anomaly_counter(anomaly_event):
    anomaly_counter = 0

    for key, value in anomaly_event.items():
        if(key == "date"):  # Skip if the key is date
            continue

        # Retrieve the event and statistic details
        event = next((e for e in events if e['event_name'] == key), None)
        # print(event)    # Debug line
        stat = next((s for s in stats if s['event_name'] == key), None)
        # print(stat) # Debug line
        
        # Declare and initialize needed information
        weight = event['weight']
        deviation = abs(value - stat['mean']) / stat['std_deviation']   # Calculate deviation in terms of standard deviations

        # Weight deviation    
        weighted_deviation = deviation * weight
        anomaly_counter += weighted_deviation
    
    return round(anomaly_counter, 2)

# Alert detection
def detect_alert(anomaly_counter, threshold):
    # If the anomaly counter is equal or bigger than the threshold
    if anomaly_counter >= threshold:
        return "!!!!!!!!!! FLAGGED !!!!!!!!!!"
    else:
        return "OK"

# Anomalies detection
def detect_anomalies(anomaly_dectect_events):
    all_anomaly_dectects = []
    threshold = calculate_threshold()

    for anomaly_event in anomaly_dectect_events:
        anomaly_counter = calculate_anomaly_counter(anomaly_event)
        status = detect_alert(anomaly_counter, threshold)

        all_anomaly_dectects.append({
            "date": anomaly_event["date"],
            "anomaly_counter": anomaly_counter,
            "threshold": threshold,
            "status": status
        })

    return all_anomaly_dectects

# Function to write the alert
def write_alert_file(all_anomaly_dectects):
    # Convert generated data into json format
    json_object = json.dumps(all_anomaly_dectects, indent = 4)
    with open(alert_file_name, "w") as outfile:
        outfile.write(json_object)

    print(f"Anomaly detection results saved to {alert_file_name}")

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

# Step 6 to 10: Anomaly detection
read_stat_file("Step 6: Please enter the new Stats file for anomaly detection: ") # Request user to input new stats file name and load through it
print("Step 7: New Stats file read completed.")

# Step 8: request user to input no_of days
no_of_days = int(input("Step 8: Enter the number of days to generate activities for anomaly detection: "))
anomaly_dectect_events = generate_events(no_of_days)    # Generate activities base on number of days
# print(json.dumps(anomaly_dectect_events, indent = 4))   # Debug line

# Step 9 and 10: Calculate and print anomilies result
input("Step 9: Anomaly detection activity data generated completed. Press Enter to proceed next step...")
all_anomaly_dectects = detect_anomalies(anomaly_dectect_events)
write_alert_file(all_anomaly_dectects)
print(json.dumps(all_anomaly_dectects, indent = 4))  # Debug line
input("Step 10: Anomaly detection results print completed. Press Enter to proceed next step...")