from daily_report import *

alert_file_name = "alerts.json"

def calculate_threshold():
    sum_of_weight = 0
    for event in events:
        sum_of_weight += event['weight']

    return 2 * sum_of_weight

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

def detect_alert(anomaly_counter, threshold):
    # If the anomaly counter is equal or bigger than the threshold
    if anomaly_counter >= threshold:
        return "!!!!!!!!!! FLAGGED !!!!!!!!!!"
    else:
        return "OK"


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

# Step 6 to 10: Anomaly detection
read_stat_file("Step 6: Please enter the new Stats file for anomaly detection: ")
print("Step 7: New Stats file read completed.")

no_of_days = int(input("Step 8: Enter the number of days to generate activities for anomaly detection: "))
anomaly_dectect_events = generate_events(no_of_days)    # Generate activities base on number of days
# print(json.dumps(anomaly_dectect_events, indent = 4))   # Debug line

input("Step 9: Anomaly detection activity data generated completed. Press Enter to proceed next step...")
all_anomaly_dectects = detect_anomalies(anomaly_dectect_events)
write_alert_file(all_anomaly_dectects)
print(json.dumps(all_anomaly_dectects, indent = 4))  # Debug line
input("Step 10: Anomaly detection results print completed. Press Enter to proceed next step...")