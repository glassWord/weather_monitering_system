import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import pandas as pd
from data.serial_data import weather_data  # Import the weather_data function

# Initialize x_axis
x_axis = 0

# Read the CSV file into a DataFrame
df = pd.read_csv('data/weather_data.csv')

# Extract columns into lists
initial_data = {
    'Temperature': df['Temperature'].tolist(),
    'Humidity': df['Humidity'].tolist(),
    'AirQuality': df['AirQuality'].tolist(),
}

df = pd.DataFrame(initial_data)

# Initialize figure and axes for multiple subplots
fig, (ax_temp, ax_humid, ax_air) = plt.subplots(3, 1, figsize=(10, 15))

# Initialize data lists for plotting
xdata, ydata_temp, ydata_humid, ydata_air = [], [], [], []
line_temp, = ax_temp.plot([], [], 'r-', label='Temperature')
line_humid, = ax_humid.plot([], [], 'g-', label='Humidity')
line_air, = ax_air.plot([], [], 'b-', label='AirQuality')

def init():
    ax_temp.set_xlim(0,100)
    ax_temp.set_ylim(20, 60)
    ax_temp.legend()
    ax_temp.set_title('Temperature')
    
    ax_humid.set_xlim(0,100)
    ax_humid.set_ylim(45, 54)
    ax_humid.legend()
    ax_humid.set_title('Humidity')
    
    ax_air.set_xlim(0, 100)
    ax_air.set_ylim(130, 145)
    ax_air.legend()
    ax_air.set_title('Air Quality')
    
    return line_temp, line_humid, line_air

def update(frame):
    global x_axis, df

    # Fetch new data
    new_data = weather_data()

    # Append new data to the DataFrame
    df = df._append(new_data, ignore_index=True)

    # Append new data to the lists
    xdata.append(x_axis)
    ydata_temp.append(new_data['Temperature'])
    ydata_humid.append(new_data['Humidity'])
    ydata_air.append(new_data['AirQuality'])
    
    # Update line data for each subplot
    line_temp.set_data(xdata, ydata_temp)
    line_humid.set_data(xdata, ydata_humid)
    line_air.set_data(xdata, ydata_air)
    
    # Adjust x-axis dynamically for each subplot
    for ax in [ax_temp, ax_humid, ax_air]:
        ax.set_xlim(max(0, x_axis - 100), x_axis + 10)
        ax.relim()
        ax.autoscale_view()

    # Increment x_axis
    x_axis += 1

    return line_temp, line_humid, line_air

x_axis = 0

def main():
    try:
        # Your main code here
        print("Data visualization is going on,")
        print("Press Ctrl+C to stop the script.")

        # * To run the main script
        ani = animation.FuncAnimation(fig, update, frames=np.arange(0, 1000), init_func=init, blit=True, interval=600)
        plt.tight_layout()
        plt.show()

        print("\n Closed")
    except KeyboardInterrupt:
        print("\n Closed.")

if __name__ == "__main__":
    main()
else:
    print("visualization starts")
    main()