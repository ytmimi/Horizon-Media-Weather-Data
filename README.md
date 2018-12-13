# Weather Data

### Horizon Media Requirements
* Language: Python 3


* Goals: Get weather data for list of locations in the United States.


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
I'll be using `pipenv` for dependency management during this project. It's important to keep packages for different projects isolated in their own environment, otherwise you run the risk of updating global packages and breaking older projects. I enjoy `pipenv` because it's simple, allows others to easily recreate your enviornment from the 'pipfile.lock', and loads enviornment variables from a .env file.









##### Tests
I'm a firm believer that the code you write should be tested. Also, since we're writing code thats interacting with a 3rd party API that we don't control we can mock the API response to make sure that any code that uses that response works properly.

##### [OpenWeatherMap API Tips](https://openweathermap.org/appid)
* "Better call API by city ID instead of a city name, city coordinates or zip code to get a precise result"






### Future Considerations
*1)* What features should be implemented in future versions?
  * Store more data:

  * Expand the possible inputs to the API. Currently the API supports getting weather data by city name, city ID, geographic coordinates, and ZIP code.


  * write and package a client library for the
  OpenWeatherMap API. Currently all the code that interacts with the API is included within

*2)* What are potential optimization opportunities?
  * asyncronous requests requests are made in parallel
  * using the bulk endpoint fewer requests are made.
  * combination of both approaches to make simultaneous bult data requests

*3)* What could break this current version?
  currently data is only being fetched by city name. If you instead tried to requests data using a city ID, geographic coordinates or zipcode the code would break.
