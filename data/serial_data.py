import random
import pandas as pd
import time

csv_file = "weather_data.csv"
rest_time = 1  # In seconds

def weather_data():
    # Generate new data
    new_temp = random.randint(25, 35)
    new_humid = random.randint(60, 70)
    new_air_quality = random.randint(30, 40)

    new_data = {
        'Temperature': [new_temp],  # List of one item
        'Humidity': [new_humid],    # List of one item
        'AirQuality': [new_air_quality]  # List of one item
    }

    # Convert new data to DataFrame
    new_df = pd.DataFrame(new_data)

    # Append new data to the CSV file
    new_df.to_csv(csv_file, mode='a', header=not pd.io.common.file_exists(csv_file), index=False)

    return new_data

if __name__ == "__main__":
    # Main code here
    print("Data updating is going on,")
    print("Press Ctrl+C to stop the script.")
    try:
        while True:
            weather_data()
            print("Data updated")
            time.sleep(rest_time)
    except KeyboardInterrupt:
        print("\nData updating stopped.")
