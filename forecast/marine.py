r"""
This module defines the MarineWeather class facilitating the retrieval of marine weather data from
the Open-Meteo Marine Weather API based on latitudinal and longitudinal coordinates of the location.

The MarineWeather class allows users to extract various types of marine weather information, including 
current marine weather data and up to upcoming 8-days hourly and daily marine weather forecast data.
"""

import requests

from common import constants
from objects import BaseWeather


class MarineWeather(BaseWeather):
    r"""
    MarineWeather class to extract marine weather data based on latitude and longitude coordinates.
    It interacts with the Open-Meteo Marine Weather API to fetch the current or up to upcoming 8-days
    hourly and daily marine weather forecast data with a resolution of 5 kilometers(km).

    Params:
    - lat (int | float): Latitudinal coordinates of the location.
    - long (int | float): Longitudinal coordinates of the location.
    - wave_type (str): Type of ocean wave, must be one of the following:
        - 'composite' (Extracts data related to all wave types.)
        - 'wind' (Extracts data related to waves generated by winds.)
        - 'swell' (Extracts data related to waves travelling across long distances.)
    """

    __slots__ = "_lat", "_long", "_wave_type", "_type", "_params"

    _session = requests.Session()
    _api = constants.MARINE_API

    def __init__(
        self, lat: int | float, long: int | float, wave_type: constants.WAVE_TYPES
    ) -> None:
        super().__init__(lat, long)

        self.wave_type = wave_type

    @property
    def wave_type(self) -> str:
        return self._wave_type

    @wave_type.setter
    def wave_type(self, __value: str) -> None:

        # Retrieves the corresponding wave type value used as a request parameter for
        # extracting marine weather data from the Open-Meteo Marine Weather API.
        wave_type: str = constants.WAVE_TYPES_MAP.get(__value)

        if wave_type is None:
            raise ValueError(
                f"Expected `wave_type` to be 'composite', 'wind' or 'swell', got {__value}"
            )

        # self._wave_type is assigned the wave type
        # value same as provided for user reference.
        self._wave_type = __value

        # self._type is used by the internally by the methods
        # for requesting marine weather data from the API.
        self._type = wave_type
