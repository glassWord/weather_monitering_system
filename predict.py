import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import tkinter as tk

rest_time = 600 # in Ms

rows_to_read_only=12 # Limit 

# Function to load initial data from CSV
def load_initial_data(csv_file):
    df = pd.read_csv(csv_file,nrows=rows_to_read_only)
    return {
        'Temperature': df['Temperature'].tolist(),
        'Humidity': df['Humidity'].tolist(),
        'AirQuality': df['AirQuality'].tolist(),
    }

# Load data from CSV file
initial_data = load_initial_data('data/weather_data.csv')

# Tkinter Setup
root = tk.Tk()
root.title("Weather Prediction")

# Create labels to display the predictions
label_temp = tk.Label(root, text="Predicted Temperature: ", font=('Helvetica', 12))
label_temp.pack(pady=5)

label_humid = tk.Label(root, text="Predicted Humidity: ", font=('Helvetica', 12))
label_humid.pack(pady=5)

label_air = tk.Label(root, text="Predicted Air Quality: ", font=('Helvetica', 12))
label_air.pack(pady=5)

# Function to predict weather
def predict_weather(data):
    df = pd.DataFrame(data)
    
    # Create dummy features if needed
    if len(df) > 0:
        X = pd.DataFrame({'Feature1': np.ones(len(df))})  # Dummy feature
        y_temp = df['Temperature']
        y_humid = df['Humidity']
        y_air_quality = df['AirQuality']
        
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
    else:
        # Return default values if no data is available
        return [[[], [], []], [[], [], []]]

# Function to print results
def result_print(y_pred_temp, y_pred_humid, y_pred_air):
    keys = ["Predicted Temperature:", "Predicted Humidity:", "Predicted Air Quality:"]
    pred_data = [y_pred_temp, y_pred_humid, y_pred_air]
    values_pred = []
    # Loop to print values with key
    key_index = 0
    for i in pred_data:
        if len(i) == 0:
            values_to_print = 0
        else:
            values_to_print = sum(i) / len(i)
        to_print = f'{keys[key_index]} {values_to_print}'
        print(to_print)
        values_pred.append(values_to_print)
        key_index += 1
    return values_pred

# Function to update labels
def update_labels():
    res = predict_weather(initial_data)
    pred_weather_values = result_print(*res[0])
    label_temp.config(text=f"Predicted Temperature: {pred_weather_values[0]:.2f}")
    label_humid.config(text=f"Predicted Humidity: {pred_weather_values[1]:.2f}")
    label_air.config(text=f"Predicted Air Quality: {pred_weather_values[2]:.2f}")
    
    # Schedule the function to be called again after 600 ms
    root.after(rest_time, update_labels)

# Start updating labels
update_labels()

# Run the Tkinter event loop
root.mainloop()
