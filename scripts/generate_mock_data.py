import os
import json
from weather_data import _city_weather

#small script to build a mock data file that I can use for testing

weather_data = {}
cities = ['Albany', 'Albuquerque', 'Anchorage','Atlanta', 'Austin',]
for city in cities:
    data =_city_weather(city)
    if data:
        print(f'GETTING WEATHER DATA FOR: {city}')
        weather_data[city] = data

path = os.path.dirname(__file__)
json_path = os.path.join(path, 'test_response.json')

with open(json_path, 'w') as file:
    file.write(json.dumps(weather_data, indent=4))

print(f'WRITING WEATHER DATA TO: {json_path}')
