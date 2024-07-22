import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import pandas as pd
from data.serial_data import weather_data  # Import the weather_data function

# Initialize x_axis
x_axis = 0

# Initialize DataFrame with initial data
initial_data = {
    'Temperature': [30, 35, 40, 35, 25, 25, 35, 40, 30, 25],
    'Humidity': [85, 80, 70, 75, 90, 95, 65, 70, 80, 75],
    'AirQuality': [40, 45, 30, 35, 40, 55, 45, 30, 40, 55],
}
df = pd.DataFrame(initial_data)

# Initialize figure and axis
fig, ax = plt.subplots()
xdata, ydata_temp, ydata_humid, ydata_air = [], [], [], []
line_temp, = plt.plot([], [], 'r-', label='Temperature')
line_humid, = plt.plot([], [], 'g-', label='Humidity')
line_air, = plt.plot([], [], 'b-', label='AirQuality')

def init():
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 120)  # Adjusted y-limits to fit all data ranges
    ax.legend()
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
    
    # Update line data
    line_temp.set_data(xdata, ydata_temp)
    line_humid.set_data(xdata, ydata_humid)
    line_air.set_data(xdata, ydata_air)
    
    # Adjust x-axis dynamically
    ax.set_xlim(max(0, x_axis - 100), x_axis + 10)
    ax.relim()
    ax.autoscale_view()

    # Increment x_axis
    x_axis += 1

    return line_temp, line_humid, line_air

x_axis = 0

ani = animation.FuncAnimation(fig, update, frames=np.arange(0, 1000), init_func=init, blit=True, interval=600)
plt.show()
