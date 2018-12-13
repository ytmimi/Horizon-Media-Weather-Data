import os
import json
import csv
import requests

API_KEY = os.environ['OPEN_WEATHER_API_KEY']

#see docs: https://openweathermap.org/current#name
API_URL = 'http://api.openweathermap.org/data/2.5/weather/'


def _city_weather(city, country_code='us'):
	'''
	Makes requests to the OpenWeatherMap API
	city: (str) name of a city
	country_code: (str) ISO 3166 country code
	return: (dict) dictionary containing weather info
	'''
	# url parameters
	params = {
		'q':','.join([city, country_code]),
		'APPID': API_KEY,
	}
	# makes the API requests and checks that the response is OK
	resp = requests.get(url=API_URL, params=params)
	if resp.status_code == 200:
		return json.loads(resp.text)


def _weather_dict_from_csv(csv_path):
	'''
	csv_path: (str) path to the csv with location data
	return: (dict) a dictionary of {city_name: weather_data, ...}
	'''
	#check that the csv_file exists

	#Keep track of cities
	cities = {}

	#open the csv file
	with open(csv_path, 'w') as file:
		pass



def generate_weather_csv(weather_dict, file_path):
	'''
	weather_dict: (dict) a dictionary of {city_name: weather_data, ...}
	file_path: full path to the newly generated csv
	generates a new csv
	'''
	pass












if __name__ == '__main__':
	print(weather_data_by_city('New York'))
