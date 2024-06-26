"""
Marine Module
-------------

This module defines the MarineWeather class facilitating the extraction of marine
weather data from the Open-Meteo Marine Weather API based on the latitudinal and
longitudinal coordinates of the location.
"""

import atexit

import requests
import pandas as pd

from ..objects import BaseForecast
from ..common import constants, tools


class MarineWeather(BaseForecast):
    """
    MarineWeather class allows extraction of marine weather data based on the latitude and longitude
    coordinates. It interacts with the Open-Meteo Marine Weather API to fetch the current or up to
    upcoming 8-days hourly and daily marine weather forecast data with a resolution of 5 kilometers(km).
    """

    __slots__ = "_lat", "_long", "_wave_type", "_type", "_params", "_forecast_days"

    _session = requests.Session()
    _api = constants.MARINE_API

    # Closes the request session upon exit.
    atexit.register(_session.close)

    # The maximum number of days in the future for forecast data extraction.
    _max_forecast_days = 8

    def __init__(
        self,
        lat: int | float,
        long: int | float,
        wave_type: constants.WAVE_TYPES = "composite",
        forecast_days: int = 7,
    ) -> None:
        """
        Creates an instance of the MarineWeather class.

        #### Params:
        - lat (int | float): Latitudinal coordinates of the location.
        - long (int | float): Longitudinal coordinates of the location.
        - wave_type (str): Type of ocean wave; must be one of the following:
            - 'composite' (Waves of all types)
            - 'wind' (Waves generated by winds)
            - 'swell' (Waves travelling across long distances)
        - forecast_days (int): Number of days for which the forecast has to
        be extracted; must be in the range of 1 and 8.

        #### Raises:
        - RequestError: If no marine data is available at the specified coordinates.
        """
        super().__init__(lat, long, forecast_days)
        self.wave_type = wave_type

    @property
    def wave_type(self) -> str:
        return self._wave_type

    @wave_type.setter
    def wave_type(self, __value: str) -> None:

        # Retrieves the corresponding wave type value used as a request parameter for
        # extracting marine weather data from the Open-Meteo Marine Weather API.
        wave_type: str | None = constants.WAVE_TYPES_MAP.get(__value)

        if wave_type is None:
            raise ValueError(
                f"Expected `wave_type` to be 'composite', 'wind' or 'swell'; got {__value!r}."
            )

        # `self._wave_type` is assigned the wave type value
        # same as specified for user reference.
        self._wave_type = __value

        # `self._type` is used internally by the methods for
        # requesting marine weather data from the API.
        self._type = wave_type

    def __repr__(self) -> str:
        return (
            f"MarineWeather(lat={self._lat}, long={self._long}, "
            f"wave_type={self._wave_type!r}, forecast_days={self._forecast_days})"
        )

    def get_current_summary(self) -> pd.Series:
        """
        Returns a pandas Series of current marine weather summary data
        at the specified coordinates of the specified wave type.

        #### The marine weather summary data includes the following data types:
        - Wave height
        - Wave direction
        - Wave period
        """

        # A string representation of the marine weather summary data types
        # separated by commas as supported for requesting the Web API.
        data_types: str = self._type + f",{self._type}".join(
            constants.MARINE_WEATHER_SUMMARY_DATA_TYPES
        )

        return tools.get_current_summary(
            self._session,
            self._api,
            self._params | {"current": data_types},
            constants.MARINE_WEATHER_SUMMARY_DATA_TYPES,
        )

    def get_hourly_summary(self) -> pd.DataFrame:
        """
        Returns a pandas DataFrame of hourly marine weather summary data
        at the specified coordinates of the specified wave type.

        #### The marine weather summary data includes the following data types:
        - Wave height
        - Wave direction
        - Wave period
        """

        # A string representation of the marine weather summary data types
        # separated by commas as supported for requesting the Web API.
        data_types: str = self._type + f",{self._type}".join(
            constants.MARINE_WEATHER_SUMMARY_DATA_TYPES
        )

        return tools.get_periodical_summary(
            self._session,
            self._api,
            self._params | {"hourly": data_types},
            constants.MARINE_WEATHER_SUMMARY_DATA_TYPES,
        )

    def get_daily_summary(self) -> pd.DataFrame:
        """
        Returns a pandas DataFrame of daily marine weather summary data
        at the specified coordinates of the specified wave type.

        #### The marine weather summary data includes the following data types:
        - Max wave height
        - Dominant wave direction
        - Max wave period
        """

        # A string representation of the marine weather summary data types
        # separated by commas as supported for requesting the Web API.
        data_types: str = self._type + f",{self._type}".join(
            (
                "wave_height_max",
                "wave_direction_dominant",
                "wave_period_max",
            )
        )

        return tools.get_periodical_summary(
            self._session,
            self._api,
            self._params | {"daily": data_types},
            constants.MARINE_WEATHER_SUMMARY_DATA_TYPES,
        )

    def get_current_wave_height(self) -> int | float:
        """
        Returns the current wave height in meters(m) of the
        specified wave type at the specified coordinates.
        """
        return self._get_current_data({"current": f"{self._type}wave_height"})

    def get_current_wave_direction(self) -> int | float:
        """
        Returns the current wave direction in degrees of the specified
        wave type at the specified coordinates.
        """
        return self._get_current_data({"current": f"{self._type}wave_direction"})

    def get_current_wave_period(self) -> int | float:
        """
        Returns the current wave period (It refers to the time taken by two consecutive
        wave crests (or troughs) to pass a fixed point) in seconds(d) of the
        specified wave type at the specified coordinates.
        """
        return self._get_current_data({"current": f"{self._type}wave_period"})

    def get_hourly_wave_height(self) -> pd.Series:
        """
        Returns a pandas Series of hourly mean wave height in meters(m) of the
        specified wave type at the specified coordinates.
        """
        return self._get_periodical_data({"hourly": f"{self._type}wave_height"})

    def get_hourly_wave_direction(self) -> pd.Series:
        """
        Returns a pandas Series of hourly wave direction in degrees of the
        specified wave type at the specified coordinates.
        """
        return self._get_periodical_data({"hourly": f"{self._type}wave_direction"})

    def get_hourly_wave_period(self) -> pd.Series:
        """
        Returns a pandas Series of hourly wave period in seconds(s) of the
        specified wave type at the specified coordinates.
        """
        return self._get_periodical_data({"hourly": f"{self._type}wave_period"})

    def get_daily_max_wave_height(self) -> pd.Series:
        """
        Returns a pandas Series of daily maximum wave height in meters(m) of the
        specified wave type at the specified coordinates.
        """
        return self._get_periodical_data({"daily": f"{self._type}wave_height_max"})

    def get_daily_dominant_wave_direction(self) -> pd.Series:
        """
        Returns a pandas Series of daily dominant wave direction in degrees of the
        specified wave type at the specified coordinates.
        """
        return self._get_periodical_data(
            {"daily": f"{self._type}wave_direction_dominant"}
        )

    def get_daily_max_wave_period(self) -> pd.Series:
        """
        Returns a pandas Series of daily maximum wave period in seconds of the
        specified wave type at the specified coordinates.
        """
        return self._get_periodical_data({"daily": f"{self._type}wave_period_max"})
