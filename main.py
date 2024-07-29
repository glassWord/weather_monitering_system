import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import numpy as np
import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

rest_time = 6000  # in ms
csv_file = "data/weather_data.csv"
max_ele = 40

class ModernWhiteApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Modern White Theme App")
        self.configure(bg='#FFFFFF')
        self.state('zoomed')  # Start in full-screen mode
        self.accent_color = '#333333'  # Dark gray accent color for text
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
        left_frame = tk.Frame(self, bg='#FFFFFF')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
     
        # Frame for bottom left (for additional info or controls)
        self.bottom_left_frame = tk.Frame(self, bg='#F0F0F0', height=100)
        self.bottom_left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        self.bottom_left_frame.pack_propagate(False)  # Prevent the frame from resizing to fit its content

        # Predicted data section
        tk.Label(left_frame, text="Predicted Data", font=self.font_large, fg='#333333', bg='#FFFFFF', anchor='w').pack(pady=10, padx=20, anchor='w')
        
        self.label_temp = tk.Label(left_frame, text="Predicted Temperature: ", font=self.font_small, fg='#333333', bg='#FFFFFF', anchor='w')
        self.label_temp.pack(pady=5, padx=20, anchor='w')

        self.label_humid = tk.Label(left_frame, text="Predicted Humidity: ", font=self.font_small, fg='#333333', bg='#FFFFFF', anchor='w')
        self.label_humid.pack(pady=5, padx=20, anchor='w')

        self.label_air = tk.Label(left_frame, text="Predicted Air Quality: ", font=self.font_small, fg='#333333', bg='#FFFFFF', anchor='w')
        self.label_air.pack(pady=5, padx=20, anchor='w')

        # Graphs section (right side)
        graph_frame = tk.Frame(self, bg='#FFFFFF')
        graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.create_graphs(graph_frame)

    def create_graphs(self, parent):
        # Initialize figure and axes for multiple subplots
        self.fig, (self.ax_temp, self.ax_humid, self.ax_air) = plt.subplots(3, 1, figsize=(14, 18))  # Increased width
        self.fig.patch.set_facecolor('#FFFFFF')

        # Initialize data lists for plotting
        self.xdata, self.ydata_temp, self.ydata_humid, self.ydata_air = [], [], [], []
        self.line_temp, = self.ax_temp.plot([], [], 'r-', label='Temperature')
        self.line_humid, = self.ax_humid.plot([], [], 'g-', label='Humidity')
        self.line_air, = self.ax_air.plot([], [], 'b-', label='AirQuality')

        # Enable grid lines
        for ax in [self.ax_temp, self.ax_humid, self.ax_air]:
            ax.grid(True)

        # Embed the plot into Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Create the animation
        self.ani = FuncAnimation(self.fig, self.update_plot, frames=200, init_func=self.init_plot, blit=True, interval=600)

    def init_plot(self):
        for ax in [self.ax_temp, self.ax_humid, self.ax_air]:
            ax.set_facecolor('#FFFFFF')
            ax.tick_params(colors=self.accent_color)
            for spine in ax.spines.values():
                spine.set_color(self.accent_color)

        title_color = '#333333'

        self.ax_temp.set_xlim(0, 100)
        self.ax_temp.set_ylim(20, 60)
        self.ax_temp.legend()
        self.ax_temp.set_title('Temperature', color=title_color)

        self.ax_humid.set_xlim(0, 100)
        self.ax_humid.set_ylim(30, 64)
        self.ax_humid.legend()
        self.ax_humid.set_title('Humidity', color=title_color)

        self.ax_air.set_xlim(0, 100)
        self.ax_air.set_ylim(120, 300)
        self.ax_air.legend()
        self.ax_air.set_title('Air Quality', color=title_color)

        return self.line_temp, self.line_humid, self.line_air

    def update_plot(self, frame):
        # Fetch new data
        new_data = self.weather_data()
        if isinstance(new_data, pd.DataFrame) and not new_data.empty:
            new_data = new_data.iloc[0]  # Get the first row of new_data

            # Remove empty or all-NA columns from new_data
            new_data = new_data.dropna(how='all')

            # Exclude empty or all-NA columns before concatenation
            if not new_data.empty:
                self.df = pd.concat([self.df, new_data.to_frame().T], ignore_index=True)

                # Append new data to the lists
                self.xdata.append(self.x_axis)
                self.ydata_temp.append(new_data['Temperature'])
                self.ydata_humid.append(new_data['Humidity'])
                self.ydata_air.append(new_data['AirQuality'])
                
                # Update line data for each subplot
                self.line_temp.set_data(self.xdata, self.ydata_temp)
                self.line_humid.set_data(self.xdata, self.ydata_humid)
                self.line_air.set_data(self.xdata, self.ydata_air)

                # Add annotations for the latest data points
                self.ax_temp.plot(self.xdata, self.ydata_temp, 'ro')
                self.ax_humid.plot(self.xdata, self.ydata_humid, 'go')
                self.ax_air.plot(self.xdata, self.ydata_air, 'bo')

                for i in range(len(self.xdata)):
                    self.ax_temp.annotate(f"{self.ydata_temp[i]:.2f}", xy=(self.xdata[i], self.ydata_temp[i]), textcoords="offset points", xytext=(0,10), ha='center')
                    self.ax_humid.annotate(f"{self.ydata_humid[i]:.2f}", xy=(self.xdata[i], self.ydata_humid[i]), textcoords="offset points", xytext=(0,10), ha='center')
                    self.ax_air.annotate(f"{self.ydata_air[i]:.2f}", xy=(self.xdata[i], self.ydata_air[i]), textcoords="offset points", xytext=(0,10), ha='center')
                
                # Adjust x-axis dynamically for each subplot
                for ax in [self.ax_temp, self.ax_humid, self.ax_air]:
                    ax.set_xlim(max(0, self.x_axis - 100), self.x_axis + 10)
                    ax.relim()
                    ax.autoscale_view()
                
                # Increment x_axis
                self.x_axis += 1

        return self.line_temp, self.line_humid, self.line_air

    def weather_data(self):
        if os.path.exists(csv_file):
            try:
                # Read the CSV file into a DataFrame
                df = pd.read_csv(csv_file)
                
                if not df.empty and all(col in df.columns for col in ['Temperature', 'Humidity', 'AirQuality']):
                    # Return the last row of the DataFrame
                    return df.iloc[[-1]].reset_index(drop=True)
            
            except pd.errors.EmptyDataError:
                print("The CSV file is empty or not readable.")
    
    # Return a DataFrame with default values if the CSV file is empty or missing
        return pd.DataFrame({'Temperature': [0], 'Humidity': [0], 'AirQuality': [0]})

    def load_initial_data(self, csv_file, end_point=max_ele):
        if os.path.exists(csv_file):
            try:
                data = pd.read_csv(csv_file)
                if not data.empty and all(col in data.columns for col in ['Temperature', 'Humidity', 'AirQuality']):
                    start_index = max(0, len(data) - end_point)  # Ensure start index is non-negative
                    data_to_predict = {
                        'Temperature': data['Temperature'].tolist()[start_index:],
                        'Humidity': data['Humidity'].tolist()[start_index:],
                        'AirQuality': data['AirQuality'].tolist()[start_index:],
                    }
                    return data_to_predict
            except pd.errors.EmptyDataError:
                print("The CSV file is empty or not readable.")
        return {'Temperature': [], 'Humidity': [], 'AirQuality': []}

    def predict_weather(self, data):
        data = self.load_initial_data(csv_file, max_ele)
        if not data or not any(data.values()):  # Check if data is empty
            return [0], [0], [0]  # Return zero predictions if no data

        X = np.ones((len(data['Temperature']), 1))  # Dummy feature
        y_temp = np.array(data['Temperature'])
        y_humid = np.array(data['Humidity'])
        y_air_quality = np.array(data['AirQuality'])

        # Split the data into training/testing sets for each target
        X_train_temp, X_test_temp, y_train_temp, y_test_temp = train_test_split(X, y_temp, test_size=0.2, random_state=42)
        X_train_humid, X_test_humid, y_train_humid, y_test_humid = train_test_split(X, y_humid, test_size=0.2, random_state=42)
        X_train_air, X_test_air, y_train_air, y_test_air = train_test_split(X, y_air_quality, test_size=0.2, random_state=42)

        # Train linear regression models
        reg_temp = LinearRegression().fit(X_train_temp, y_train_temp)
        reg_humid = LinearRegression().fit(X_train_humid, y_train_humid)
        reg_air = LinearRegression().fit(X_train_air, y_train_air)

        # Make predictions using the last data point
        y_pred_temp = reg_temp.predict([[1]])
        y_pred_humid = reg_humid.predict([[1]])
        y_pred_air = reg_air.predict([[1]])

        return y_pred_temp, y_pred_humid, y_pred_air

    def update_labels(self):
        predicted_temp, predicted_humid, predicted_air = self.predict_weather(csv_file)
        self.label_temp.config(text=f"Predicted Temperature: {predicted_temp[0]:.2f}")
        self.label_humid.config(text=f"Predicted Humidity: {predicted_humid[0]:.2f}")
        self.label_air.config(text=f"Predicted Air Quality: {predicted_air[0]:.2f}")
        self.after(rest_time, self.update_labels)


if __name__ == "__main__":
    try:
        app = ModernWhiteApp()
        app.protocol("WM_DELETE_WINDOW", app.destroy)  # Proper close when clicking the X button
        app.mainloop()
    except KeyboardInterrupt:
        print("\n Closed.")

else:
    print("This App can't be use in This way.")
