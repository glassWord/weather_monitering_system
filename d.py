import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from matplotlib.animation import FuncAnimation

rest_time = 6000  # in ms
csv_file = "data/weather_data.csv"
max_ele = 40

class ModernDarkApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Modern Dark Theme App")
        self.configure(bg='#121212')
        self.state('zoomed')  # Start in full-screen mode
        self.accent_color = '#E0E0E0'  # Light white accent color
        self.font_large = ("Helvetica", 24)
        self.font_medium = ("Helvetica", 18)
        self.font_small = ("Helvetica", 12)  # Slightly smaller font size for predicted data
        
        # Initialize data-related attributes
        self.x_axis = 0
        self.df = pd.DataFrame(columns=['Temperature', 'Humidity', 'AirQuality'])
        
        self.create_widgets()
        self.update_labels()

    def create_widgets(self):
        # Left frame (for predicted data)
        left_frame = tk.Frame(self, bg='#121212')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Predicted data section without background rectangle
        tk.Label(left_frame, text="Predicted Data", font=self.font_large, fg='#90EE90', bg='#121212', anchor='w').pack(pady=10, padx=20, anchor='w')
        
        self.label_temp = tk.Label(left_frame, text="Predicted Temperature: ", font=self.font_small, fg='#90EE90', bg='#121212', anchor='w')
        self.label_temp.pack(pady=5, padx=20, anchor='w')

        self.label_humid = tk.Label(left_frame, text="Predicted Humidity: ", font=self.font_small, fg='#90EE90', bg='#121212', anchor='w')
        self.label_humid.pack(pady=5, padx=20, anchor='w')

        self.label_air = tk.Label(left_frame, text="Predicted Air Quality: ", font=self.font_small, fg='#90EE90', bg='#121212', anchor='w')
        self.label_air.pack(pady=5, padx=20, anchor='w')

        # Graphs section (right side)
        graph_frame = tk.Frame(self, bg='#121212')
        graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.create_graphs(graph_frame)

    def create_graphs(self, parent):
        # Initialize figure and axes for multiple subplots
        self.fig, (self.ax_temp, self.ax_humid, self.ax_air) = plt.subplots(3, 1, figsize=(14, 18))  # Increased width
        self.fig.patch.set_facecolor('#121212')

        # Initialize data lists for plotting
        self.xdata, self.ydata_temp, self.ydata_humid, self.ydata_air = [], [], [], []
        self.line_temp, = self.ax_temp.plot([], [], 'r-', label='Temperature')
        self.line_humid, = self.ax_humid.plot([], [], 'g-', label='Humidity')
        self.line_air, = self.ax_air.plot([], [], 'b-', label='AirQuality')

        canvas = FigureCanvasTkAgg(self.fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.ani = FuncAnimation(self.fig, self.update_plot, frames=200, init_func=self.init_plot, blit=True, interval=100)

    def init_plot(self):
        for ax in [self.ax_temp, self.ax_humid, self.ax_air]:
            ax.set_facecolor('#1E1E1E')
            ax.tick_params(colors=self.accent_color)
            for spine in ax.spines.values():
                spine.set_color(self.accent_color)

        self.ax_temp.set_xlim(0, 100)
        self.ax_temp.set_ylim(0, 120)
        self.ax_temp.legend()
        self.ax_temp.set_title('Temperature', color=self.accent_color)
        
        self.ax_humid.set_xlim(0, 100)
        self.ax_humid.set_ylim(0, 120)
        self.ax_humid.legend()
        self.ax_humid.set_title('Humidity', color=self.accent_color)
        
        self.ax_air.set_xlim(0, 100)
        self.ax_air.set_ylim(100, 220)
        self.ax_air.legend()
        self.ax_air.set_title('Air Quality', color=self.accent_color)
        
        return self.line_temp, self.line_humid, self.line_air

    def update_plot(self, frame):
        # Fetch new data
        new_data = self.weather_data()
        # Append new data to the DataFrame
        self.df = self.df._append(new_data, ignore_index=True)
        # Append new data to the lists
        self.xdata.append(self.x_axis)
        self.ydata_temp.append(new_data['Temperature'])
        self.ydata_humid.append(new_data['Humidity'])
        self.ydata_air.append(new_data['AirQuality'])
        
        # Update line data for each subplot
        self.line_temp.set_data(self.xdata, self.ydata_temp)
        self.line_humid.set_data(self.xdata, self.ydata_humid)
        self.line_air.set_data(self.xdata, self.ydata_air)
        
        # Adjust x-axis dynamically for each subplot
        for ax in [self.ax_temp, self.ax_humid, self.ax_air]:
            ax.set_xlim(max(0, self.x_axis - 100), self.x_axis + 10)
            ax.relim()
            ax.autoscale_view()
        
        # Increment x_axis
        self.x_axis += 1
        return self.line_temp, self.line_humid, self.line_air

    def weather_data(self):
        # Dummy function to generate random weather data
        return {
            'Temperature': np.random.randint(20, 30),
            'Humidity': np.random.randint(50, 70),
            'AirQuality': np.random.randint(100, 200)
        }

    def load_initial_data(self, csv_file, end_point=max_ele):
        data = pd.read_csv(csv_file)
        start_index = max(0, len(data) - end_point)  # Ensure start index is non-negative
        data_to_predict = {
            'Temperature': data['Temperature'].tolist()[start_index:],
            'Humidity': data['Humidity'].tolist()[start_index:],
            'AirQuality': data['AirQuality'].tolist()[start_index:],
        }
        return data_to_predict

    def predict_weather(self, data):
        data = self.load_initial_data(csv_file, max_ele)
        if not data or not any(data.values()):  # Check if data is empty
            return [[[], [], []], [[], [], []]]  # Return empty predictions if no data

        X = np.ones((len(data['Temperature']), 1))  # Dummy feature
        y_temp = np.array(data['Temperature'])
        y_humid = np.array(data['Humidity'])
        y_air_quality = np.array(data['AirQuality'])

        # Split the data into training/testing sets for each target
        X_train_temp, X_test_temp, y_train_temp, y_test_temp = train_test_split(X, y_temp, test_size=0.2, random_state=42)
        X_train_humid, X_test_humid, y_train_humid, y_test_humid = train_test_split(X, y_humid, test_size=0.2, random_state=42)
        X_train_air, X_test_air, y_train_air, y_test_air = train_test_split(X, y_air_quality, test_size=0.2, random_state=42)

        # Model Training
        model_temp = LinearRegression()
        model_temp.fit(X_train_temp, y_train_temp)

        model_humid = LinearRegression()
        model_humid.fit(X_train_humid, y_train_humid)

        model_air = LinearRegression()
        model_air.fit(X_train_air, y_train_air)

        # Prediction
        y_pred_temp = model_temp.predict(X_test_temp)
        y_pred_humid = model_humid.predict(X_test_humid)
        y_pred_air = model_air.predict(X_test_air)

        return [[y_pred_temp, y_pred_humid, y_pred_air], [y_test_temp, y_test_humid, y_test_air]]

    def result_print(self, y_pred_temp, y_pred_humid, y_pred_air):
        keys = ["Predicted Temperature:", "Predicted Humidity:", "Predicted Air Quality:"]
        pred_data = [y_pred_temp, y_pred_humid, y_pred_air]
        values_pred = []
        key_index = 0
        for i in pred_data:
            if len(i) == 0:
                values_to_print = 0
            else:
                values_to_print = sum(i) / len(i)
            to_print = f'{keys[key_index]} {values_to_print}'
            values_pred.append(values_to_print)
            key_index += 1
        return values_pred

    def update_labels(self):
        res = self.predict_weather(self.df)
        pred_weather_values = self.result_print(*res[0])
        self.label_temp.config(text=f"Predicted Temperature: {pred_weather_values[0]:.2f}")
        self.label_humid.config(text=f"Predicted Humidity: {pred_weather_values[1]:.2f}")
        self.label_air.config(text=f"Predicted Air Quality: {pred_weather_values[2]:.2f}")
        
        # Schedule the function to be called again after rest_time ms
        self.after(rest_time, self.update_labels)

if __name__ == "__main__":
    app = ModernDarkApp()
    app.mainloop()
