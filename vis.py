import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import pandas as pd
import random
from data.serial_data import weather_data # Weather Data

# Convert data dictionary to DataFrame
df = pd.DataFrame(weather_data())

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

def get_new_data():
    global x_axis
    if x_axis < len(df):
        new_data = {
            'Temperature': df['Temperature'].iloc[x_axis],
            'Humidity': df['Humidity'].iloc[x_axis],
            'AirQuality': df['AirQuality'].iloc[x_axis]
        }
    else:
        new_data = {
            'Temperature': random.randint(20, 40),
            'Humidity': random.randint(60, 100),
            'AirQuality': random.randint(30, 60)
        }
    x_axis += 1
    return new_data

def update(frame):
    new_data = get_new_data()
    xdata.append(x_axis)
    ydata_temp.append(new_data['Temperature'])
    ydata_humid.append(new_data['Humidity'])
    ydata_air.append(new_data['AirQuality'])
    
    line_temp.set_data(xdata, ydata_temp)
    line_humid.set_data(xdata, ydata_humid)
    line_air.set_data(xdata, ydata_air)
    
    ax.set_xlim(max(0, x_axis - 100), x_axis + 10)  # Adjust x-axis dynamically
    ax.relim()
    ax.autoscale_view()
    return line_temp, line_humid, line_air

x_axis = 0

ani = animation.FuncAnimation(fig, update, frames=np.arange(0, 1000), init_func=init, blit=True, interval=600)
plt.show()
