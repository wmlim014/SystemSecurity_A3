from generate_logs import *

analysis_file_name = "analysis_results.json"

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

event_stats = calculate_event_stats(generated_events)
write_analysis_file(event_stats)
print(json.dumps(event_stats, indent = 4))  # Debug line
input("Step 5: Calculated statistics printed completed. Press Enter to proceed next step...")