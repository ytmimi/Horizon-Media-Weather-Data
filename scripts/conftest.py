import os
import csv
import json

import pytest

@pytest.fixture(scope='session')
def cities():
    return ['Albany', 'Albuquerque', 'Anchorage','Atlanta', 'Austin',]

@pytest.fixture(scope='session')
def mock_api_response(cities):
    path = os.path.dirname(__file__)
    with open(os.path.join(path, 'test_response.json')) as file:
        data = json.loads(file.read())
        yield {city:weather for city, weather in data.items() if city in cities}

@pytest.fixture
def non_existent_csv(tmpdir):
    return str(tmpdir.join('test.csv'))

@pytest.fixture
def non_csv_file(tmpdir):
    path = tmpdir.join('test.txt')
    f = open(path, 'w')
    f.close()
    return str(path)

@pytest.fixture
def empty_csv(tmpdir):
    path = tmpdir.join('empty.csv')
    csv = path.open('w')
    csv.close()
    return str(path)

@pytest.fixture
def test_csv(tmpdir, cities):
    header = ['Location']
    path = tmpdir.join('test.csv')
    with open(path, 'w') as file:
        csv_file = csv.writer(file)
        csv_file.writerow(header)
        for city in cities:
            csv_file.writerow([city])
    return str(path)
