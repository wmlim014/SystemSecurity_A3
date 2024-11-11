from read_files import *

def match_event_type(event_name, event_type, std_deviation):
    match event_type:
        case 'D':   # Standard deviation must be integer
            if not std_deviation.is_integer():
                print(f"Warning: {event_name} is discrete but has a non-integer standard deviation.")
        
        case 'C':   # Standard deviation must be float
            if std_deviation.is_integer():
                print(f"Warning: {event_name} is discrete but has an integer standard deviation.")

        case _:
            print(f"Warning: {event_name} is not discrete and continuous.")
            print("Please correct it with either 'C' and 'D' before re-load the file...")
            load_file()

def check_std_deviation():
    global events, stats

    print()
    for event in events:
        for stat in stats:
            # If current stats event name is equal to event event name...
            if event['event_name'] == stat['event_name']:
                # Check event type...
                match_event_type(event['event_name'], event['event_type'], stat['std_deviation'])

def check_alert():
    global events

    print()
    for event in events:
        if event['alert'] <= 0:
            print(f"Warning: {event['event_name']} alert is not a positive integer.")
            print("Please correct the alert and re-load the file...")
            load_file()

def step1_to_3():
    # Prompt user to input the file name
    load_file()
    check_std_deviation()
    check_alert()
    input("Step 3: Inconsistencies check completed. Press enter to proceed next step...")

# step1_to_3()    # Debug line