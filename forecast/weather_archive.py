r"""
This module defines the Archive class facilitating the retrieval of historical weather data from
the Open-Meteo Weather History API based on latitudinal and longitudinal coordinates of the location.

The Archive class allows users to extract vaious types of historical weather data information
ranging from the year 1940 till the present.
"""

from datetime import date, datetime

import requests
import pandas as pd

from common import constants
from objects import BaseWeather


class Archive(BaseWeather):
    r"""
    Archive class to extract historical weather data based on latitude and longitude coordinates of
    the location within the specified date range. It interacts with the Open-Meteo Weather History
    API to fetch the weather data ranging from 1940 till the present.

    Date parameters must be date or datetime objects or strings
    formatted in the ISO-8601 date format (YYYY-MM-DD).

    Params:
    - lat (int | float): Latitudinal coordinates of the location.
    - long (int | float): Longitudinal coordinates of the location.
    - start_date (str | date | datetime): Initial date for the weather data.
    - end_date(str | date | datetime): Final date for the weather data.
    """

    _session = requests.Session()
    _api = constants.WEATHER_HISTORY_API

    def __init__(
        self,
        lat: int | float,
        long: int | float,
        start_date: str | date | datetime,
        end_date: str | date | datetime,
    ) -> None:
        super().__init__(lat, long)

        self.start_date = start_date
        self.end_date = end_date

        self._params |= {"start_date": start_date, "end_date": end_date}

    @staticmethod
    def _resolve_date(target: str | date | datetime, var: str) -> date:
        r"""
        [PRIVATE] Verifies the supplied date argument, resolves it into a
        string formatted date object with ISO-8601 format (YYYY-MM-DD).

        The `var` parameter has to be the name of the actual date parameter
        (`start_date` or `end_date`) for reference in custom error messages.
        """

        if not isinstance(target, date | datetime):
            try:
                target = datetime.strptime(target, r"%Y-%m-%d").date()

            except (ValueError, TypeError):
                raise ValueError(f"Invalid value for `{var}` parameter.")

        if isinstance(target, datetime):
            target = target.date()

        assert target <= date.today(), ValueError(
            f"`{var}` must not be some date in the future."
        )

        return target

    @property
    def start_date(self) -> str:
        return self._start_date.strftime(r"%Y-%m-%d")

    @start_date.setter
    def start_date(self, __value: str | date | datetime) -> None:
        self._start_date = self._resolve_date(__value, "start_date")

    @property
    def end_date(self) -> str:
        return self._end_date.strftime(r"%Y-%m-%d")

    @end_date.setter
    def end_date(self, __value: str | date | datetime) -> None:
        end_date: date = self._resolve_date(__value, "end_date")

        assert end_date > self._start_date, ValueError(
            f"`end_date` must be greater or equal to `start_date`."
        )

        self._end_date = end_date

    def get_hourly_temperature(
        self, unit: constants.TEMPERATURE_UNITS = "celsius"
    ) -> pd.DataFrame:
        r"""
        Returns a pandas DataFrame of temperature data 2 meters(m) above the ground
        level at the specified coordinates within the supplied date range.

        Params:
        - unit: Temperature unit, must be 'celsius' or 'fahrenheit'.
        """

        if unit not in ("celsius", "fahrenheit"):
            raise ValueError(
                f"Expected `unit` to be 'celsius' or 'fahrenheit', got {unit!r}."
            )

        return self.get_periodical_data(
            {"hourly": "temperature_2m", "temperature_unit": unit}
        )

    def get_hourly_relative_humidity(self) -> pd.DataFrame:
        r"""
        Returns a pandas DataFrame of hourly relative humidity percentage(%)
        data at the specified coordinates within the date range.
        """
        return self.get_periodical_data({"hourly": "relative_humidity_2m"})

    def get_periodic_weather_code(self, frequency: constants.FREQUENCY) -> pd.DataFrame:
        r"""
        Returns a pandas DataFrame of hourly weather code data with its corresponding
        description at the specified coordinates within the supplied date range.

        Params:
        - frequency: Frequency of the data distribution, must be 'daily' or 'hourly'.

        Columns:
        - time: time of the forecast data in ISO 8601 format (YYYY-MM-DDTHH-MM).
        - data: weather code at the corresponding hour.
        - description: description of the corresponding weather code.
        """

        if frequency not in ("hourly", "daily"):
            raise ValueError(
                f"Expected `frequency` to be 'hourly' or 'daily', got {frequency!r}."
            )

        data: pd.DataFrame = self.get_periodical_data({frequency: "weather_code"})

        # Creating a new column 'description' mapped to the
        # description of the corresponding weather code.
        data["description"] = data["data"].map(
            lambda x: constants.WEATHER_CODES[str(x)]
        )

        return data

    def get_hourly_total_cloud_cover(self) -> pd.DataFrame:
        r"""
        Returns a pandas DataFrame of hourly total cloud cover percentage(%) data
        at the specified coordinates within the supplied date range.
        """
        return self.get_periodical_data({"hourly": "cloud_cover"})

    def get_hourly_cloud_cover(
        self, level: constants.CLOUD_COVER_LEVEL = "low"
    ) -> pd.DataFrame:
        r"""
        Returns a pandas DataFrame of hourly cloud cover percentage(%) data
        at the specified level and coordinates within the supplied date range.

        Params:
        - level (str): Altitude level of the desired cloud coverage, must be
        one of the following:
            - 'low' (clouds and fog up to an altitude of 3 km.)
            - 'mid' (clouds at an altitude between 3 km and 8 km.)
            - 'high' (clouds at an altitude higher than 8 km.)
        """

        if level not in ("low", "mid", "high"):
            raise ValueError(
                f"Expected `level` to be 'low', 'mid' or 'high'. Got {level!r}."
            )

        return self.get_periodical_data({"hourly": f"cloud_cover_{level}"})

    def get_hourly_apparent_temperature(
        self, unit: constants.TEMPERATURE_UNITS = "celsius"
    ) -> pd.DataFrame:
        r"""
        Returns a pandas DataFrame of apparent temperature data at
        the specified coordinates within the supplied date range.

        Params:
        - unit: Temperature unit, must be 'celsius' or 'fahrenheit'.
        """

        if unit not in ("celsius", "fahrenheit"):
            raise ValueError(
                f"Expected `unit` to be 'celsius' or 'fahrenheit', got {unit!r}."
            )

        return self.get_periodical_data(
            {"hourly": "apparent_temperature", "temperature_unit": unit}
        )

    def get_hourly_dew_point(
        self, unit: constants.TEMPERATURE_UNITS = "celsius"
    ) -> pd.DataFrame:
        r"""
        Returns a pandas DataFrame of hourly dew point data 2 meters(m) above the
        ground level at the specified coordinates within the date range.

        Params:
        - unit: Temperature unit, must be 'celsius' or 'fahrenheit'.
        """

        if unit not in ("celsius", "fahrenheit"):
            raise ValueError(
                f"Expected `unit` to be 'celsius' or 'fahrenheit', got {unit!r}."
            )

        return self.get_periodical_data(
            {"hourly": "dew_point_2m", "temperature_unit": unit}
        )

    def get_hourly_precipitation(
        self, unit: constants.PRECIPITATION_UNITS = "mm"
    ) -> pd.DataFrame:
        r"""
        Returns a pandas DataFrame of hourly precipitation (sum of rain, showers, and snowfall)
        data at the specified coordinates within the supplied date range.

        Params:
        - unit: Precipitation unit, must be 'mm' or 'inch'.
        """

        if unit not in ("mm", "inch"):
            raise ValueError(f"Expected `unit` to be 'mm' or 'inch', got {unit!r}.")

        return self.get_periodical_data(
            {"hourly": "precipitation", "precipitation_unit": unit}
        )

    def get_hourly_wind_speed(
        self,
        altitude: constants.ARCHIVE_WIND_ALTITUDES = 10,
        unit: constants.WIND_SPEED_UNITS = "kmh",
    ) -> pd.DataFrame:
        r"""
        Returns a pandas DataFrame of hourly wind speed data at the specified
        altitude and coorindates within the supplied date range.

        Params:
        - altitude (int): Altitude from the ground level in meters(m), must be 10 or 100.
        - unit (str): Wind speed unit, must be one of the following:
            - 'kmh' (kilometers per hour)
            - 'mph' (miles per hour)
            - 'ms' (meter per second)
            - 'kn' (knots)
        """

        if altitude not in (10, 100):
            raise ValueError(f"Expected `altitute` to be 10 or 100, got {altitude}.")

        if unit not in ("kmh", "mph", "ms", "kn"):
            raise ValueError(
                f"Expected `unit` to be 'kmh', 'mph', 'ms' or 'kn', got {unit!r}."
            )

        return self.get_periodical_data(
            {"hourly": f"wind_speed_{altitude}m", "wind_speed_unit": unit}
        )

    def get_hourly_wind_direction(
        self,
        altitude: constants.ARCHIVE_WIND_ALTITUDES = 10,
    ) -> pd.DataFrame:
        r"""
        Returns a pandas DataFrame of hourly wind direction data at the
        specified altitude and coorindates within the supplied date range.

        Params:
        - altitude (int): Altitude from the ground level in meters(m), must be 10 or 100.
        """

        if altitude not in (10, 100):
            raise ValueError(f"Expected `altitute` to be 10 or 100, got {altitude}.")

        return self.get_periodical_data({"hourly": f"wind_direction_{altitude}"})

    def get_hourly_wind_gusts(
        self,
        altitude: constants.ARCHIVE_WIND_ALTITUDES = 10,
        unit: constants.WIND_SPEED_UNITS = "kmh",
    ) -> pd.DataFrame:
        r"""
        Returns a pandas DataFrame of hourly wind gusts data at the specified
        altitude and coorindates within the supplied date range.

        Params:
        - altitude (int): Altitude from the ground level in meters(m), must be 10 or 100.
        - unit (str): Wind speed unit, must be one of the following:
            - 'kmh' (kilometers per hour)
            - 'mph' (miles per hour)
            - 'ms' (meter per second)
            - 'kn' (knots)
        """

        if altitude not in (10, 100):
            raise ValueError(f"Expected `altitute` to be 10 or 100, got {altitude}.")

        if unit not in ("kmh", "mph", "ms", "kn"):
            raise ValueError(
                f"Expected `unit` to be 'kmh', 'mph', 'ms' or 'kn', got {unit!r}."
            )

        return self.get_periodical_data(
            {"hourly": f"wind_gusts_{altitude}m", "wind_speed_unit": unit}
        )

    def get_hourly_soil_temperature(
        self, depth: int, unit: constants.TEMPERATURE_UNITS = "celsius"
    ) -> pd.DataFrame:
        r"""
        Returns a pandas DataFrame of hourly soil temperature data at the specified
        depth and coordinates in the specified unit within the supplied date range.

        Params:
        - depth (int): Desired depth of the temperature data within the ground level in
        centimeters(m). Temperature is extracted as a part of a range of depth. Available
        depth ranges are 0-7cm, 7-28cm, 28-100cm, 100-255cm. The supplied depth must fall
        in the range of 0 and 255.
        - unit: Temperature unit, must be 'celsius' or 'fahrenheit'.
        """

        if unit not in ("celsius", "fahrenheit"):
            raise ValueError(
                f"Expected `unit` to be 'celsius' or 'fahrenheit', got {unit!r}."
            )

        for key, value in constants.ARCHIVE_SOIL_DEPTH.items():
            if depth in key:

                # The range is represented in a string format as being
                # a supported type for requesting the API.
                depth_range: str = value
                break

        else:
            raise ValueError(
                f"Expected `depth` to be in the range of 0 and 255, got {depth}."
            )

        return self.get_periodical_data(
            {"hourly": f"soil_temperature_{depth_range}cm", "temperature_unit": unit},
        )

    def get_daily_temperature(
        self,
        type: constants.DAILY_WEATHER_REQUEST_TYPES,
        unit: constants.TEMPERATURE_UNITS = "celsius",
    ) -> pd.DataFrame:
        r"""
        Returns a pandas DataFrame of daily max temperature data 2 meters(m) above the
        ground level at the specified coordinates within the supplied date range.

        Params:
        - type: Specifies the type of daily temperature to be retrieved,
        must be 'min', 'max' or 'mean'.
            - 'min': Daily minimum temperature.
            - 'max': Daily maximum temperature.
            - 'mean': Daily mean temperature.
        - unit: Temperature unit, must be 'celsius' or 'fahrenheit'.
        """

        if type not in ("max", "min", "mean"):
            raise ValueError(f"Expected `type` to be 'min' or 'max', got {type!r}.")

        if unit not in ("celsius", "fahrenheit"):
            raise ValueError(
                f"Expected `unit` to be 'celsius' or 'fahrenheit', got {unit!r}."
            )

        return self.get_periodical_data(
            {"daily": f"temperature_2m_{type}", "temperature_unit": unit}
        )

    def get_daily_apparent_temperature(
        self,
        type: constants.DAILY_WEATHER_REQUEST_TYPES,
        unit: constants.TEMPERATURE_UNITS = "celsius",
    ) -> pd.DataFrame:
        r"""
        Returns a pandas DataFrame of daily max apparent temperature data 2 meters(m) above
        the ground level at the specified coordinates within the supplied date range.

        Params:
        - type: Specifies the type of daily apparent temperature to be retrieved,
        must be 'min', 'max' or 'mean'.
            - 'min': Daily minimum apparent temperature.
            - 'max': Daily maximum apparent temperature.
            - 'mean': Daily mean apparent temperature.
        - unit: Temperature unit, must be 'celsius' or 'fahrenheit'.
        """

        if type not in ("max", "min", "mean"):
            raise ValueError(f"Expected `type` to be 'min' or 'max', got {type!r}.")

        if unit not in ("celsius", "fahrenheit"):
            raise ValueError(
                f"Expected `unit` to be 'celsius' or 'fahrenheit', got {unit!r}."
            )

        return self.get_periodical_data(
            {"daily": f"apparent_temperature_{type}", "temperature_unit": unit}
        )

    def get_daily_dominant_wind_direction(self) -> pd.DataFrame:
        r"""
        Returns a pandas DataFrame of daily dominant wind direction in degrees data 10 meters(m)
        above the ground level at the specified coordinates within the supplied date range.
        """
        return self.get_periodical_data({"daily": "wind_direction_10m_dominant"})
