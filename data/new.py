import serial
import pandas as pd

# Initialize an empty dictionary to store data
data = {
    'Temperature': [],
    'Humidity': [],
    'AirQuality': [],
}

# Define the serial port and configure explicitly
ser = serial.Serial(port='COM5', baudrate=9600, timeout=1)


def read_from_serial():
    # Attempt to read a line of data from the Arduino
        data_str = ser.readline().decode('utf-8').strip()
        return data_str

def main():
    data_str=(read_from_serial())
    lines =None

    try:
        lines = data_str.split('\n')
    except:
        print("value none")

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


def csv_write(data):
    df = pd.DataFrame(data)
    csv_file = 'example_pandas.csv'
    df.to_csv(csv_file, index=False)
if __name__ == '__main__':
    try:
        while True:
            main()
            print(data)
            
            try:
                csv_write(data)
            except:
                print("data is empty")
    except KeyboardInterrupt:
        print('Interrupted')
        print(data)
        csv_write(data)

    finally:
        ser.close()


        