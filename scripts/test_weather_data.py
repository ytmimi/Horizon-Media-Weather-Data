import os
import pytest
import weather_data as wd
from unittest.mock import patch

LIVE_TESTS = False

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
    def test_location_csv_with_moch_data(self, mock_request, test_csv, mock_api_response):
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


def test_weather_csv_from_dict(tmpdir, mock_api_response):
    pass
