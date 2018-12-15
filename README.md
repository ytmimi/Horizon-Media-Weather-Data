# Weather Data

### Horizon Media Requirements
* Language: Python 3


* Goals: Get weather data for a list of locations in the United States.


* Input - CSV containing:
  * Location


* Output - CSV containing:
  * Location
  * Temperature
  * Wind Speed
  * Weather Description

### Yacin Tmimi's Solution
Below is a detailed description of how to run the code and the rational for the choices I made while working on this assignment

##### Setup
I'll be using `pipenv` for dependency management during this project. It's important to keep packages for different projects isolated in their own environment, otherwise you run the risk of updating global packages and breaking older projects. I enjoy `pipenv` because it's simple, allows others to easily recreate your enviornment from the `pipfile.lock`, and loads enviornment variables from a `.env` file. If you'd like to use other tools for setting up your virtual enviornment I've included a `requirements.txt` file, which outlines all the external packages used. The main package to note is `requests version 2.21.0`. All other packages are dependencies of requests.

If you don't already have `pipenv` installed you can do so with:
```
$: pip install pipenv
```

Once `pipenv` is installed you can create the virtual environment by running:
```
$: pipenv install
```

This will create a new python 3 environment and download all the required packages.

As is best practice, I have not committed my OpenWeatherMap API key to source control. Before you can run the code you will have to get your own [API KEY](https://openweathermap.org/appid). I recommend creating a `.env` file in the root project directory and putting your api key in there.

If you've chosen to create a `.env` file, add your API KEY as follows:
```
OPEN_WEATHER_API_KEY = your_api_key
```

If you would rather hard code your API KEY, then edit the global variable set in `scripts/weather_data.py`
```python
#scripts/weather_data.py

# hard code the API_KEY if not loading it from a .env file using pipenv
# API_KEY = os.environ['OPEN_WEATHER_API_KEY']
API_KEY = 'your_api_key'
```


If you have a paid account with OpenWeatherMap please adjust the ACCOUNT_STATUS variable in `scripts/weather_data.py`
```python
#scripts/weather_data.py

#if you have a paid account set ACCOUNT_STATUS to 'paid'
ACCOUNT_STATUS = 'free'
```

This setting controls rate limiting to one request/second for free accounts. If you have a free account and still decide to change the `ACCOUNT_STATUS` to `paid` any 429 responses you get from the server will not be handled and you wont get weather data for that city. In the worst case OpenWeatherMap may suspend your account.


If you're using `pipenv` you can now activate the virtual enviornment by running:å
```
$: pipenv shell
```

If you're eager to run the code at this point you can with:
```
$: python scripts/weather_data.py
```
However, I would recommend first running all the tests to ensure that everything is working properly.


##### Tests
Since this project revolves around a weather data service that we don't control I wanted to write some unit tests. This would allow me to mock out API responses to test the functionality of the code without having to continually make outgoing requests to OpenWeatherMap's API. Just to be sure that the code continues to function in the future, some tests don't mock the API response, and instead actually call the service. If these "LIVE" tests fail, while the mocked tests pass we can assume OpenWeatherMap has made changes to their API.

Assuming you've activated your virtual environment, you can run the tests with:
```
$: pytest
```
The output should look something like this:
```
collected 15 items

scripts/test_weather_data.py sss....s......s

```

If you'd like to also run "LIVE" tests, set the LIVE_TESTS variable in `scripts/test_weather_data.py` to True
```python
# scripts/test_weather_data.py
...

LIVE_TESTS = True
```
Running the tests with pytest this time should output:
```
collected 15 items

scripts/test_weather_data.py ...............

```
If you don't see any 'F' or 'E' characters in the output, then that means that there were no test failures or errors.

##### Running the code
If you've setup the virtual environment, included your API key, and didn't get errors when running the tests (include LIVE tests), then you can be sure that the code will work as its written.

As stated above, to generate a csv containing weather data run:
```
$: python scripts/weather_data.py
```

This will generate a new csv file: `CSVs/weather_data.csv`

##### Teardown
If you've run the code and now have a `weather_data.csv` file in the `CSVs` directory then the program worked! If you're using `pipenv` and would like to exit the virtual environment go to the command line and enter:
```
$: exit
```

If you'd like to completely remove the virtual environment form your system execute the following command:
```
pipenv --rm
```

### Future Considerations
*1)* What features should be implemented in future versions?
  * Store more data:

  * Expand the possible inputs to the API. Currently the API supports getting weather data by city name, city ID, geographic coordinates, and ZIP code.
  ##### [OpenWeatherMap API Tips](https://openweathermap.org/appid)
  * "Better call API by city ID instead of a city name, city coordinates or zip code to get a precise result"

  * currently just a command line tool. We could exapand the project to include a frontend where useres could select a csv file and send it

  * write and package a client library for the
  OpenWeatherMap API. Currently all the code that interacts with the API is included within

*2)* What are potential optimization opportunities?
  * asyncronous requests requests are made in parallel
  * using the bulk endpoint fewer requests are made.
  * combination of both approaches to make simultaneous bult data requests
  * for performance and reduced hits to the api you could add a cache layer into the system

*3)* What could break this current version?
  currently data is only being fetched by city name. If you instead tried to requests data using a city ID, geographic coordinates or zipcode the code would break.
