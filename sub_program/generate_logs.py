from check_file_data import *
import numpy as np
import datetime

no_of_days = 10
log_file_name = "logs.json"

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

# Function to write the event
def write_log_file(generated_events):
    # Convert generated data into json format
    json_object = json.dumps(generated_events, indent = np.size(events))
    with open(log_file_name, "w") as outfile:
        outfile.write(json_object)

    print(f"Generated event data saved to {log_file_name}")

generated_events = generate_events(no_of_days)
write_log_file(generated_events)
print(json.dumps(generated_events, indent = np.size(events)))   # Debug line
input("Step 4: Event generation completed. Press Enter to proceed next step...")