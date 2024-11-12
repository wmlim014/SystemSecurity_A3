from read_files import *

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


check_data()
input("Step 3: Inconsistencies check completed. Press enter to proceed next step...")