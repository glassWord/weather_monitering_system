import random 

x_axis = 0

def get_new_data():
    global x_axis
    new_x = x_axis
    new_y = random.randint(20,35)  # Replace with actual data fetching logic
    x_axis += 1
    return new_x, new_y

# To generate random Values

def weather_data():
    new_temp = random.randint(25, 35)
    new_humid = random.randint(60, 70)
    new_air_quality = random.randint(30, 40)

    data = {
    'Temperature': [30, 35, 40, 35, 25, 25, 35, 40, 30, 25],
    'Humidity': [85, 80, 70, 75, 90, 95, 65, 70, 80, 75],
    'AirQuality': [40, 45, 30, 35, 40, 55, 45, 30, 40, 55],
    }

    data['Temperature'].append(new_temp)
    data['Humidity'].append(new_humid)
    data['AirQuality'].append(new_air_quality)

    return data

