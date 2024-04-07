r"""
This module defines the Weather class facilitating the retrieval of weather data from
the Open-Meteo Weather API based on latitudinal and longitudinal coordinates of the location.

The Weather class allows users to extract various types of weather information, including 
current weather data, upcoming 7-days hourly weather forecast data, and upcoming 7-days 
daily weather forecast data.
"""

from typing import Literal, Any

import requests
import pandas as pd

from common import constants, tools


class Weather:
    r"""
    Weather class to extract weather data based on latitude and longitude coordinates.
    It interacts with the Open-Meteo Weather API to fetch the current or upcoming 7-days
    forecast weather data.

    Initialization(__init__) Params:
    - lat (int | float): latitudinal coordinates of the location.
    - long (int | float): longitudinal coordinates of the location.

    This class allows the user to extract the following:
    - Current weather data such as temperature, atmospheric pressure, weather code, etc.
    - Upcoming 7-days hourly weather forecast data including the current day.
    - Upcoming 7-days daily weather forecast data including the current day.
    """

    __slots__ = "_lat", "_long", "_session", "_api", "_params"

    def __init__(self, lat: int | float, long: int | float) -> None:

        # Verifying the supplied `lat` and `long` arguments.
        assert -90 <= lat <= 90, ValueError(
            f"`lat` must be in the range of -90 and 90. Got {lat}"
        )
        assert -180 <= long <= 180, ValueError(
            f"`long` must be in the range of -180 and 180. Got {long}"
        )

        self._api = constants.WEATHER_API
        self._session = requests.Session()

        # Template of the params dictionary to be used for API requests.
        self._params = {"latitude": lat, "longitude": long}

    @property
    def lat(self) -> int | float:
        return self._params["latitude"]

    @property
    def long(self) -> int | float:
        return self._params["longitude"]

    def __repr__(self) -> str:
        return f"Weather(lat={self.lat}, long={self.long})"
