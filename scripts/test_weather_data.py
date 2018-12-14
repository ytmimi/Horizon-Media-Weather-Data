import os
import csv

import weather_data as wd

import pytest
from unittest.mock import patch

LIVE_TESTS = True

@pytest.mark.skipif(not LIVE_TESTS, reason='Explicitly run tests that make API requests')
class TestAPI_Requests:
    def test_request_by_city(self):
        data = wd._city_weather('New York')
        # these are the keys in the json response that contain the data that we care about
        # just running a test to make sure that they are contained in the response
        for key in ['name', 'main', 'wind', 'weather']:
            assert key in data.keys()

    def test_request_by_ID(self):
        #requests made with an ID should return None
        #example id taken from docs: https://openweathermap.org/current#cityid
        data = wd._city_weather('2172797')
        assert data == None

    def test_request_by_zip(self):
        #surprisingly, passing in a vaild zip and country code returns a result
        #example zip taken from docs: https://openweathermap.org/current#zip
        data = wd._city_weather('94040')
        assert isinstance(data, dict)


class TestWeatherDictFromCSV:
    def test_non_csv(self, non_csv_file):
        #raise ValueError if non csv file is used
        with pytest.raises(ValueError) as err:
            wd._weather_dict_from_csv(non_csv_file)

    def test_csv_does_not_exist(self, non_existent_csv):
        #raise FileNotFoundError if incorrect file path is given
        with pytest.raises(FileNotFoundError) as err:
            wd._weather_dict_from_csv(non_existent_csv)

    def test_empty_csv(self, empty_csv):
        #raise a StopIteration error if you attempt to parse and empty csv
        with pytest.raises(StopIteration) as err:
            wd._weather_dict_from_csv(empty_csv)

    @patch('weather_data._city_weather')
    def test_location_csv_with_mock_data(self, mock_request, test_csv, mock_api_response):
        #mock the request object to return data from the mock_request dict
        mock_request.side_effect = lambda city: mock_api_response.get(city)
        data = wd._weather_dict_from_csv(test_csv)

        assert isinstance(data, dict)
        assert mock_api_response.keys() == data.keys()

    @pytest.mark.skipif(not LIVE_TESTS, reason='Explicitly run tests that make API requests')
    def test_location_csv_with_API_data(self, test_csv, cities):
        data = wd._weather_dict_from_csv(test_csv)
        assert isinstance(data, dict)
        assert list(data.keys()) == cities


@pytest.fixture
def generated_csv(tmpdir, mock_api_response):
    #create the file
    path = str(tmpdir.join('test.csv'))
    wd._generate_weather_csv(mock_api_response, path)

    #open the file
    with open(path) as file:
        csv_file = csv.reader(file)
        yield csv_file

@pytest.fixture(scope='session')
def headers():
    return ['Location', 'Temperature', 'Wind Speed', 'Weather Description']

class TestWeatherCSVFromDict:
    def test_generate_csv(self, tmpdir, mock_api_response):
        path = str(tmpdir.join('test.csv'))
        wd._generate_weather_csv(mock_api_response, path)
        # check that a new csv file was created
        assert 'test.csv' in os.listdir(str(tmpdir))

    def test_csv_headers(self, generated_csv, headers):
        assert next(generated_csv) == headers

    def test_csv_data(self, generated_csv, headers):
            next(generated_csv) #skip the header row
            for row in generated_csv:
                # each row should contain ['Location', 'Temperature', 'Wind Speed', 'Weather Description']
                assert len(row) == len(headers)


class TestWeatherCSVFromCSV:
    @patch('weather_data._city_weather')
    def test_weather_csv_from_mock_data(self, mock_request, test_csv, mock_api_response):
        mock_request.side_effect = lambda city: mock_api_response.get(city)
        path = wd.weather_data_csv(test_csv)
        # make sure that the csv file was created in the same file
        assert 'weather_data.csv' in os.listdir(os.path.dirname(test_csv))

    @patch('weather_data._city_weather')
    def test_headers(self, mock_request, test_csv, mock_api_response, headers):
        mock_request.side_effect = lambda city: mock_api_response.get(city)
        path = wd.weather_data_csv(test_csv)
        with open(path) as file:
            csv_file = csv.reader(file)
            assert next(csv_file) == headers

    @patch('weather_data._city_weather')
    def test_csv_data(self, mock_request, test_csv, mock_api_response, headers):
        mock_request.side_effect = lambda city: mock_api_response.get(city)
        path = wd.weather_data_csv(test_csv)
        with open(path) as file:
            csv_file = csv.reader(file)
            next(csv_file) #skip the header row
            for row in csv_file:
                assert len(row) == len(headers)

    @pytest.mark.skipif(not LIVE_TESTS, reason='Explicitly run tests that make API requests')
    def test_weather_csv_from_api_request(self, test_csv):
        path = wd.weather_data_csv(test_csv)
        assert 'weather_data.csv' in os.listdir(os.path.dirname(test_csv))
