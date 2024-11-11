# Declare variable needed
events = []
stats = []
num_of_events = 0
num_of_stats = 0

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

                    event_dist["alert"] = int(data[4].strip())
                    
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

# Step 3: Check inconsistencies
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

# Step 3: Alert check
def check_alert():
    global events

    print()
    for event in events:
        if event['alert'] <= 0:
            print(f"Warning: {event['event_name']} alert is not a positive integer.")
            print("Please correct the alert and re-load the file...")
            load_file()

################
# MAIN PROGRAM #
################
load_file() # Step 1 and 2: Prompt user to input the file name

# Step 3
check_std_deviation()   # Inconsistencies check
check_alert()   # Alert check
input("Step 3: Inconsistencies check completed. Press enter to proceed next step...")