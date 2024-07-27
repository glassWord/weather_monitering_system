import pandas as pd
import matplotlib.pyplot as plt
import time
# Load data from CSV file
df = pd.read_csv('data/weather_data.csv')

# Sample or smooth data if necessary
# For example, using a moving average to smooth the data
window_size = 50  # Adjust window size as needed
df['Temperature_Smoothed'] = df['Temperature'].rolling(window=window_size).mean()
df['Humidity_Smoothed'] = df['Humidity'].rolling(window=window_size).mean()
df['AirQuality_Smoothed'] = df['AirQuality'].rolling(window=window_size).mean()

# Set up the plot
plt.figure(figsize=(14, 12))

# Plot Temperature
plt.subplot(3, 1, 1)
plt.plot(df.index, df['Temperature'], marker='o', linestyle='-', color='r', alpha=0.5, label='Temperature (Raw)')
plt.plot(df.index, df['Temperature_Smoothed'], color='darkred', label=f'Temperature (Smoothed, window={window_size})')
plt.title('Temperature Over Time')
plt.xlabel('Index')
plt.ylabel('Temperature (°C)')
plt.legend()
plt.grid(True)

# Plot Humidity
plt.subplot(3, 1, 2)
plt.plot(df.index, df['Humidity'], marker='o', linestyle='-', color='g', alpha=0.5, label='Humidity (Raw)')
plt.plot(df.index, df['Humidity_Smoothed'], color='darkgreen', label=f'Humidity (Smoothed, window={window_size})')
plt.title('Humidity Over Time')
plt.xlabel('Index')
plt.ylabel('Humidity (%)')
plt.legend()
plt.grid(True)

# Plot Air Quality
plt.subplot(3, 1, 3)
plt.plot(df.index, df['AirQuality'], marker='o', linestyle='-', color='b', alpha=0.5, label='Air Quality (Raw)')
plt.plot(df.index, df['AirQuality_Smoothed'], color='darkblue', label=f'Air Quality (Smoothed, window={window_size})')
plt.title('Air Quality Over Time')
plt.xlabel('Index')
plt.ylabel('Air Quality (AQI)')
plt.legend()
plt.grid(True)

while True:
    time.sleep(2)
    # Adjust layout and display
    plt.tight_layout()
    plt.show()
