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

### Setup
I'll be using `pipenv` for dependency management during this project. I beleive it's important to keep packages for different projects isolated in their own environment, otherwise you run the risk of updating global packages and breaking older projects. I enjoy `pipenv` because it's simple, allows others to easily recreate your enviornment from the `pipfile.lock`, and loads enviornment variables from a `.env` file. If you'd like to use other tools for setting up your virtual enviornment I've included a `requirements.txt` file, which outlines all the external packages used. The main package to note is `requests version 2.21.0`. All other packages are dependencies of requests.

If you don't already have `pipenv` installed you can do so with:
```
$: pip install pipenv
```
If you're having trouble installing `pipenv`, please refer to the following [documentation](https://packaging.python.org/tutorials/managing-dependencies/).

Once `pipenv` is installed you can create the virtual environment by running:
```
$: pipenv install
```

This will create a new python 3 environment and download all the required packages.

I have not committed my OpenWeatherMap API key to source control. Before you can run the code you will have to get your own [API KEY](https://openweathermap.org/appid). I recommend creating a `.env` file in the root project directory and putting your api key in there.

If you've chosen to create a `.env` file, open it and add your API KEY as follows:
```
OPEN_WEATHER_API_KEY = your_api_key
```

If you would rather hard code your API KEY, then edit the global variable in `scripts/weather_data.py`
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

This setting controls rate limiting to one request/second for free accounts. If you have a free account and still decide to change the `ACCOUNT_STATUS` to `paid` any 429 responses you get from the server will not be handled and you wont get weather data for that city. In the worst case OpenWeatherMap may [suspend your account](https://openweathermap.org/appid).


If you're using `pipenv` you can now activate the virtual enviornment by running:
```
$: pipenv shell
```

If you're eager to run the code at this point you can from the root directory with:
```
$: python scripts/weather_data.py
```
However, I would recommend first running all the tests to ensure that everything is working properly.


### Tests
Since this project revolves around a weather data service that we don't control I wanted to write some unit tests. This would allow me to mock out API responses to test the functionality of the code without having to continually make outgoing requests to OpenWeatherMap's API. Just to be sure that the code continues to function in the future, some tests actually call the API when they run. Having a set of tests will also help prevent adding bugs to the system when updating the code in the future.

I've writen my tests using `pytest`. To make sure `pytest` is available in your virtual environment run:
```
$: pipenv install --dev
```
This will install all developemnt dependencies (`pytets`), for this project.

Assuming you've activated your virtual environment, you can run the tests with:
```
$: pytest
```
The output should look something like this:
```
collected 15 items

scripts/test_weather_data.py sss....s......s

```

If you'd like to also run "LIVE" tests, which actually use the OpenWeatherMap API set the LIVE_TESTS variable in `scripts/test_weather_data.py` to True
```python
# scripts/test_weather_data.py
...

LIVE_TESTS = True
```

Running the tests with `pytest` this time should output:

```
collected 15 items

scripts/test_weather_data.py ...............

```
If you don't see any 'F' or 'E' characters in the output, then that means that there were no test failures or errors.

### Running the code
If you've setup the virtual environment, included your API key, and didn't get errors when running the tests (include "LIVE" tests), then you can be sure that the code will work as its written.

Before running the tests, make sure you've activated the virtual enviornment:
```
$: pipenv shell
```
As stated above, to generate a csv containing weather data run:
```
$: python scripts/weather_data.py
```

This will generate a new csv file: `CSVs/weather_data.csv`

### Teardown
If you've run the code and now have a `weather_data.csv` file in the `CSVs` directory, then the program worked! If you're using `pipenv` and would like to exit the virtual environment go to the command line and enter:
```
$: exit
```

If you'd like to completely remove the virtual environment from your system, execute the following command:
```
$: pipenv --rm
```

### Future Considerations
#### *1)* What features should be implemented in future versions?
  * It might be nice to expand the amount of data collected from the OpenWeatherMap API. Humidity, pressure, and time are all additional fields that users might find useful to include in the output csv. Currently, location, temperature, wind Speed, and a weather description are hard coded fields. It might also be nice to allow users to specify which fields they want in their response.

  * Another useful addition might be allowing users to request weather data through without using a city name. For example the OpenWeatherMap API supports weather data lookups by city name, city ID, geographic coordinates, and ZIP code. In fact the [OpenWeatherMap API Tips](https://openweathermap.org/appid) state that it's better to call the api using a city ID, coordinates, or zip, as it leads to more precise results.

  * In the programs current condition it's just a script run from the command line. Anyone who wants to use it has to be technical enough to install python on their machine, set up their virtual environment, and go through the trouble of getting an API key. We could expand the project to include a web interface that would allow non technical users to send a list of locations, via a form, to a web server running the code. The response from the server would be a properly formatted weather data csv.


#### *2)* What are potential optimization opportunities?
  * The [OpenWeatherMap API Tips](https://openweathermap.org/appid) also state that weather data in their system doesn't update more than once every 10 minutes. To improve our programs performance and reduce the number of API calls we need to make, we could introduce caching to our program. It would make sense to cache data for each city up to 10 minutes since that's the refresh rate. If a user requests data for a city that's already been cached we can immideately return the response instead of making an API request.

  * It might also make sense to make API requests asynchronously. Because of rate limiting there would need to be some consideration for batching requests together before making a group of API requests. Being able to send a group of requests off at the same time would drastically improve the speed of the program.

  * Another feature the API provides is a [bulk data endpoint](https://openweathermap.org/current#severalid). Data for several cities can be requested at once by specify a list of city ID's. This approach is also limited to 20 cities per request, and rate limiting is still applied based on the number of cities selected. However, making one request per 20 cities would be much more performant than making 20 requests one after the other.

#### *3)* What could break this current version?
  Through testing I've identified certain scenarios where I explicitly throw errors to inform the users that they have done something incorrectly. The main function `weather_data_csv` takes one argument: The path to a csv file with city names. Errors will be thrown if:
  * The path to a non csv file is passed into the function.
  * The path to a non existent csv file is passed into the function.
  * The path to an empty csv file is passed into the function.


  Because the program expects to call the city name API endpoint, no weather data is collected if users try to request data by city ID or geographic location. However, through testing, I was surprised to discover that passing in a zipcode and country code to the city name endpoint sometimes returns data. If no weather data is collected from the API while parsing through the input csv, then an exception is thrown and no output csv is generated.
