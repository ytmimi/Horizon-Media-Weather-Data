import pytest
from weather_data import _city_weather


LIVE_TESTS = False

@pytest.fixture(scope='module')
def mock_api_resp():
    return {
        'coord': {'lon': -73.99, 'lat': 40.73},
        'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10d'}, {'id': 615, 'main': 'Snow', 'description': 'light rain and snow', 'icon': '13d'}, {'id': 701, 'main': 'Mist', 'description': 'mist', 'icon': '50d'}],
        'base': 'stations',
        'main': {'temp': 274.62, 'pressure': 1029, 'humidity': 85, 'temp_min': 272.55, 'temp_max': 275.95},
        'visibility': 14484,
        'wind': {'speed': 5.1, 'deg': 10},
        'rain': {'1h': 0.25}, 'snow': {'1h': 0.08},
        'clouds': {'all': 90}, 'dt': 1544722080,
        'sys': {'type': 1, 'id': 4026, 'message': 0.0051, 'country': 'US', 'sunrise': 1544703120, 'sunset': 1544736543},
        'id': 5128581,
        'name': 'New York',
        'cod': 200
    }


# this test will make a LIVE api call
@pytest.mark.skipif(not LIVE_TESTS, reason='Explicitly run tests that ')
def test_city_weather():
    data = city_weather('New York')
    # these are the keys in the json response that contain the data that we care about
    # just running a test to make sure that they are contained in the response
    for key in ['name', 'main', 'wind', 'weather']:
        assert key in data.keys()
