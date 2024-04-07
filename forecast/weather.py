r"""
This module defines the Weather class facilitating the retrieval of weather data from
the Open-Meteo Weather API based on latitudinal and longitudinal coordinates of the location.

The Weather class allows users to extract various types of weather information, including 
current weather data, upcoming 7-days hourly weather forecast data, and upcoming 7-days 
daily weather forecast data.
"""

from typing import Any

import requests

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

    __slots__ = "_lat", "_long", "_params"

    _api = constants.WEATHER_API
    _session = requests.Session()

    def __init__(self, lat: int | float, long: int | float) -> None:

        # Verifying the supplied `lat` and `long` arguments.
        assert -90 <= lat <= 90, ValueError(
            f"`lat` must be in the range of -90 and 90. Got {lat}"
        )
        assert -180 <= long <= 180, ValueError(
            f"`long` must be in the range of -180 and 180. Got {long}"
        )

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

    def get_current_temperature(
        self,
        altitude: constants.ALTITUDE = 2,
        unit: constants.TEMPERATURE_UNITS = "celcius",
    ) -> float:
        r"""
        Returns the current temperature in the supplied temperature unit
        at the supplied altitude in meters(m) from the ground level.

        Params:
        - altitude (int): Altitude from the ground level. Must be in (2, 80, 120, 180).
        - unit (str): Temperature unit. Must be 'celcius' or 'fahrenheit'.
        """

        if altitude not in (2, 80, 120, 180):
            raise ValueError(f"`altitude` must be in (2, 80, 120, 180). Got {altitude}")

        if unit not in ("celcius", "fahrenheit"):
            raise ValueError(
                f"`unit` must be in 'celcius' or 'fahrenheit'. Got '{unit}'"
            )

        params: dict[str, Any] = self._params | {
            "current": f"temperature_{altitude}m",
            "temperature_unit": unit,
        }
        temperature: float = tools.get_current_data(self._session, self._api, params)

        return temperature

    def get_current_weather_code(self) -> tuple[int, str]:
        r"""
        Returns a tuple comprising the weather code followed
        by a string description of the weather code.
        """

        params: dict[str, Any] = self._params | {"current": "weather_code"}

        weather_code: int = tools.get_current_data(self._session, self._api, params)
        description: str = constants.WEATHER_CODES[str(weather_code)]

        return weather_code, description

    def get_current_total_cloud_cover(self) -> int | float:
        r"""
        Returns the total cloud cover in percentage(%) at the supplied coordinates.
        """

        params: dict[str, Any] = self._params | {"current": "cloud_cover"}
        cloud_cover: int | float = tools.get_current_data(
            self._session, self._api, params
        )

        return cloud_cover

    def get_current_cloud_cover(
        self, level: constants.CLOUD_COVER_LEVEL = "low"
    ) -> int | float:
        r"""
        Returns the cloud cover in percentage(%) at the supplied level and coordinates.

        Params:
        - level (str): Altitude level of the desired cloud coverage. Level supplied must be
        one of the following:
            - 'low' (clouds and fog upto an altitude of 3 km.)
            - 'mid' (clouds at an altitude between 3 km and 8 km.)
            - 'high' (clouds at an altitude higher than 8 km.)
        """

        if level not in ("low", "mid", "high"):
            raise ValueError(
                f"`level` must be in ('low', 'mid', 'high'). Got '{level}'."
            )

        params: dict[str, Any] = self._params | {"current": f"cloud_cover_{level}"}
        cloud_cover: int | float = tools.get_current_data(
            self._session, self._api, params
        )

        return cloud_cover
