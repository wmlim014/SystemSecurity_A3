from read_files import *

def check_std_deviation():
    global events, stats

    print()
    for event in events:
        for stat in stats:
            # If current stats event name is equal to event event name...
            if event['event_name'] == stat['event_name']:
                # Check event type...
                match event['event_type']:
                    case 'D':   # Standard deviation must be integer
                        if not stat['std_deviation'].is_integer():
                            print(f"Warning: {event['event_name']} is discrete but has a non-integer standard deviation.")
                        break
                    
                    case 'C':   # Standard deviation must be float
                        if stat['std_deviation'].is_integer():
                            print(f"Warning: {event['event_name']} is discrete but has an integer standard deviation.")
                        break

                    case _:
                        print(f"Warning: {event['event_name']} is not discrete and continuous.")
                        break

def check_alert():
    global events

    print()
    for event in events:
        if event['alert'] <= 0:
            print(f"Warning: {event['event_name']} alert is not a positive integer.")
            print("Please correct the alert and re-load the file...")
            load_file()

# Prompt user to input the file name
load_file()
check_std_deviation()
check_alert()
input("Step 3: Inconsistencies check completed. Press enter to proceed next step...")