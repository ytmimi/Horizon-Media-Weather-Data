import os
import json
import csv
from time import sleep
from functools import wraps

import requests

# hard code the API_KEY if not loading it from a .env file using pipenv
API_KEY = os.environ['OPEN_WEATHER_API_KEY']

#see docs: https://openweathermap.org/current#name
API_URL = 'http://api.openweathermap.org/data/2.5/weather/'

#if you have a paid account set ACCOUNT_STATUS to 'paid'
ACCOUNT_STATUS = 'free'

def rate_limit(f):
	'''
	https://openweathermap.org/price explains that free accounts can make up to
	60 request per second. this ensures that this restriction is respected if using
	a free API KEY.
	'''
	@wraps(f)
	def wrapper(*args, **kwargs):
		if ACCOUNT_STATUS != 'paid':
			sleep(1)
		return f(*args, **kwargs)
	return wrapper


@rate_limit
def _city_weather(city, country_code='us'):
	'''
	Makes requests to the OpenWeatherMap API
	city: (str) name of a city
	country_code: (str) ISO 3166 country code
	return: (dict) dictionary containing weather info or None if a bad request was made
	'''
	# url parameters
	# addtional API url parameters https://openweathermap.org/current#other
	params = {
		'q':','.join([city, country_code]), # for accurate city search
		'units':'imperial', # for Fahrenheit temp units
		'APPID': API_KEY,
	}
	# makes the API requests and checks that the response is OK
	resp = requests.get(url=API_URL, params=params)
	if resp.status_code == 200:
		return json.loads(resp.text)


def _weather_dict_from_csv(csv_path):
	'''
	csv_path: (str) full path and file name to the csv with location data
	return: (dict) a dictionary of {city_name: weather_data, ...}
	'''
	#verify csv_path is a csv file.
	if not csv_path.endswith('.csv'):
		raise ValueError(f'{csv_path} is not a CSV file.')
	#Keep track of cities
	cities = {}
	try:
		with open(csv_path, 'r') as file:
			csv_file = csv.DictReader(file, fieldnames=['Location'])
			next(csv_file) # skip the header row
			for row in csv_file:
				city = row['Location']
				#get weather data from the API
				data = _city_weather(city)
				if data and city not in cities:
					cities[city] = data
					print(f'GETTING WEATHER DATA FOR: {city}')
	except FileNotFoundError:
		raise FileNotFoundError(f'{csv_path} not found')
	except StopIteration:
		raise StopIteration(f'{csv_path} is empty')
	return cities


def _generate_weather_csv(weather_dict, file_path):
	'''
	weather_dict: (dict) in the form {city1: weather_data, city2: weather_data, ...}
	file_path: full path to the newly generated csv
	generates a new csv
	'''
	header = ['Location', 'Temperature', 'Wind Speed', 'Weather Description']
	with open(file_path, 'w') as file:
		csv_file = csv.writer(file)
		csv_file.writerow(header)
		for city, data in weather_dict.items():
			temp = data['main']['temp']
			wind = data['wind']['speed']
			desc = data['weather'][0]['description']
			csv_file.writerow([city, temp, wind, desc])


def weather_data_csv(csv_path):
	'''
	Given the path to a csv containing locatin data, output a new file (weather_data.csv)
	in the same directory as the original csv. The new csv file contains information
	on Location, Temperature, Wind Speed, and a weather description.
	return: file path to newly generated csv
	'''
	new_file_path = os.path.join(os.path.dirname(csv_path), 'weather_data.csv')
	weather_dict = _weather_dict_from_csv(csv_path)
	if weather_dict:
		_generate_weather_csv(weather_dict, new_file_path)
	else:
		raise ValueError(f'No weather data found while parsing {csv_path}')

	return new_file_path


if __name__ == '__main__':
	base_path = os.path.dirname(os.path.dirname(__file__))

	#path to the location csv
	location_csv = os.path.join(base_path, 'CSVs', 'locations.csv')
	#generate the new file
	csv_path = weather_data_csv(location_csv)

	print(f'GENERATING WEATHER CSV AT: {csv_path}')
