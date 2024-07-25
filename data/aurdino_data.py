import serial
import time
import csv

data = {
    'Temperature': [],
    'Humidity': [],
    'AirQuality': [],
}

# Define the serial port and configure explicitly
ser = serial.Serial(port='COM5', baudrate=9600, timeout=1)

# * This 

# Initial data dictionary
def export_data_to_csv(filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Temperature', 'Humidity', 'AirQuality'])
        for i in range(len(data['Temperature'])):
            writer.writerow([data['Temperature'][i], data['Humidity'][i], data['AirQuality'][i]])

def read_from_serial():
    # Attempt to read a line of data from the Arduino
    if ser.in_waiting > 0:
    
        return data
    else:
        return None

def update_data(data_str):
    # Parse the incoming data and update the 'data' dictionary
    lines = data_str.split('\n')
    for line in lines:
        if line.startswith('Temperature:'):
            temperature = float(line.split(':')[1].split('*')[0].strip())
            data['Temperature'].append(temperature)
        elif line.startswith('Humidity:'):
            humidity = float(line.split(':')[1].split('%')[0].strip())
            data['Humidity'].append(humidity)
        elif line.startswith('Air Quality (MQ-135):'):
            air_quality = int(line.split(':')[1].strip())
            data['AirQuality'].append(air_quality)
   
def print_data_interval(interval):
    while True:
        data_str = read_from_serial()
        if data_str:
            update_data(data_str)
            print(f"Updated data: {data}")
        
        # Wait for the specified interval
        time.sleep(interval)

if __name__ == '__main__':
    try:
        # Print data every 5 seconds
        print_data_interval(5)
    except KeyboardInterrupt:
        print('Interrupted')
    finally:
        ser.close()



# Initial export of data to CSV file
export_data_to_csv('initial_data.csv')
