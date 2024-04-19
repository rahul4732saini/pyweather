r"""
This module defines the AirQuality class facilitating the extraction of air quality data from
the Open-Meteo Air Quality API based on the latitudinal and longitudinal coordinates of the location.

The AirQuality class allows users to extract various types of air quality data, including 
current air quality data and up to upcoming 7-days hourly air quality forecast data.
"""

import atexit

import requests
import pandas as pd

from common import constants
from objects import BaseForecast


class AirQuality(BaseForecast):
    r"""
    AirQuality class to extract air quality data based on the latitude and longitude coordinates.
    It interacts with the Open-Meteo Air Quality API to fetch the current or up to upcoming 7-days
    hourly air quality forecast data.
    """

    _session = requests.Session()
    _api = constants.AIR_QUALITY_API

    # The maximum number of days in the future for forecast data extraction.
    _max_forecast_days = 7

    # Closes the request session upon exit.
    atexit.register(_session.close)

    @staticmethod
    def _verify_atmospheric_gas(gas: constants.GASES) -> None:
        r"""
        Verifies whether the specified atmospheric gas is supported by the Open-Meteo
        Air Quality API for the extraction of gaseous concentration in air.
        """

        if gas not in (
            "ozone",
            "carbon_monoxide",
            "nitrogen_dioxide",
            "sulphur_dioxide",
        ):
            raise ValueError(
                "Expected `gas` to be 'ozone', 'carbon_monoxide',"
                f"'nitrogen_dioxide' or 'sulphur_dioxide'; got {gas!r}."
            )

    @staticmethod
    def _verify_plant_species(plant: constants.PLANTS) -> None:
        r"""
        Verifies whether the specified plant species is supported by the Open-Meteo
        Air Quality API for the extraction of pollen grain concentration in air.
        """

        if plant not in ("alder", "birch", "grass", "mugwort", "olive", "ragweed"):
            raise ValueError(
                "Expected `plant` to be one of 'alder', 'birch', 'grass', 'mugwort',"
                f"'olive' or 'ragweed'; got {plant!r}."
            )

    def get_current_aqi(
        self, source: constants.AQI_SOURCES = "european"
    ) -> int | float:
        r"""
        Returns the current American/European Air Quality
        Index value at the specified coordinates.

        Params:
        - source: Source of the Air Quality Index; must be one of the following:
            - 'european' (Extracts the European Air Quality Index)
            - 'us' (Extracts the USA Air Quality Index)
        """

        if source not in ("european", "us"):
            raise ValueError(
                f"Expected `source` to be 'european' or 'us'; got {source!r}."
            )

        return self._get_current_data({"current": "european_aqi"})

    def get_current_ammonia_conc(self) -> int | float | None:
        r"""
        Returns the current concentration(micro g/m^3) of ammonia(NH3) in air.
        Only available for Europe. Returns None for Non-European regions.
        """
        return self._get_current_data({"current": "ammonia"})

    def get_current_dust_conc(self) -> int | float:
        r"""
        Returns the current concentration(micro g/m^3) of dust in air
        10 meters(m) above ground level at the specified coordinates.
        """
        return self._get_current_data({"current": "dust"})

    def get_current_gaseous_conc(self, gas: constants.GASES = "ozone") -> int | float:
        r"""
        Returns the current concentration(miro g/m^3) of the specified atmospheric
        gas in air 10 meters(m) above the ground level at the specified coordinates.

        Params:
        - gas (str): Gas whose concentration needs to be extracted; must be one of the following:
        ('ozone', 'carbon_monoxide', 'nitrogen_dioxide', 'sulphur_dioxide').
        """
        self._verify_atmospheric_gas(gas)
        return self._get_current_data({"current": gas})

    def get_current_pm2_5_conc(self) -> int | float:
        r"""
        Returns the current concentration(micro g/m^3) of particulate matter with diameter
        smaller than the 2.5 micro meter(m) in air 10 meters(m) above the ground level.
        """
        return self._get_current_data({"current": "pm2_5"})

    def get_current_pm10_conc(self) -> int | float:
        r"""
        Returns the current concentration(micro g/m^3) of particulate matter with diameter
        smaller than the 10 micro meter(m) in air 10 meters(m) above the ground level.
        """
        return self._get_current_data({"current": "pm10"})

    def get_current_pollen_conc(self, plant: constants.PLANTS) -> int | float | None:
        r"""
        Returns the current concentration(grains/m^3) of pollens of the specified
        plant. Only available for Europe as provided by CAMS European Air Quality
        forecast. Returns None for Non-European regions.

        Params:
        - plant (str): Plant whose pollen concentration can be extracted; must be one of
        ('alder', 'birch', 'grass', 'mugwort', 'olive', 'ragweed').
        """
        self._verify_plant_species(plant)
        return self._get_current_data({"current": f"{plant}_pollen"})

    def get_current_uv_index(self) -> int | float:
        r"""
        Returns the current Ultra-Violet radiation index value at the specified coordinates.
        """
        return self._get_current_data({"current": "uv_index"})

    def get_current_aerosol_optical_depth(self) -> int | float:
        r"""
        Returns the current aerosol optical depth at 550 nm at the specified coordinates.

        Aerosol optical depth (AOD) at 550 nm is a measure of the extinction of solar radiation
        at a wavelength of 550 nanometers (green-yellow region of the visible spectrum) due to
        aerosol particles in the atmosphere. It is commonly used as an indicator of haze or the
        presence of aerosols in the atmosphere.
        """
        return self._get_current_data({"current": "aerosol_optical_depth"})

    def get_hourly_dust_conc(self) -> pd.DataFrame:
        r"""
        Returns a pandas DataFrame of hourly concentration(micro g/m^3) data of dust
        in air 10 meters(m) above ground level at the specified coordinates.
        """
        return self._get_periodical_data({"hourly": "dust"})

    def get_hourly_uv_index(self) -> pd.DataFrame:
        r"""
        Returns a pandas DataFrmae of hourly Ultra-Violet
        radiation index data at the specified coordinates.
        """
        return self._get_periodical_data({"hourly": "uv_index"})

    def get_hourly_pm2_5_conc(self) -> pd.DataFrame:
        r"""
        Returns a pandas DataFrame of hourly concentration(micro g/m^3) data
        of particulate matter with diameter smaller than the 2.5 micro meter(m)
        in air 10 meters(m) above the ground level.
        """
        return self._get_periodical_data({"hourly": "pm2_5"})

    def get_hourly_pm10_conc(self) -> pd.DataFrame:
        r"""
        Returns a pandas DataFrame of hourly concentration(micro g/m^3)
        data of particulate matter with diameter smaller than the 10 micro
        meter(m) in air 10 meters(m) above the ground level.
        """
        return self._get_periodical_data({"hourly": "pm10"})

    def get_hourly_pollen_conc(self, plant: constants.PLANTS) -> pd.DataFrame:
        r"""
        Returns a pandas DataFrame of hourly concentration(grains/m^3) data of pollens
        of the specified plant. Only available for Europe as provided by CAMS European
        Air Quality forecast. Returns None for Non-European regions.

        Params:
        - plant (str): Plant whose pollen concentration can be retrieved, must be one of
        ('alder', 'birch', 'grass', 'mugwort', 'olive', 'ragweed').
        """
        self._verify_plant_species(plant)
        return self._get_periodical_data({"hourly": f"{plant}_pollen"})

    def get_hourly_aerosol_optical_depth(self) -> pd.DataFrame:
        r"""
        Returns a pandas DataFrame of hourly aerosol optical
        depth data at 550 nm at the specified coordinates.

        Aerosol optical depth (AOD) at 550 nm is a measure of the extinction of solar radiation
        at a wavelength of 550 nanometers (green-yellow region of the visible spectrum) due to
        aerosol particles in the atmosphere. It is commonly used as an indicator of haze or the
        presence of aerosols in the atmosphere.
        """
        return self._get_periodical_data({"hourly": "aerosol_optical_depth"})

    def get_hourly_gaseous_conc(self, gas: constants.GASES = "ozone") -> pd.DataFrame:
        r"""
        Returns a pandas DataFrame of hourly concentration(miro g/m^3) data of
        the specified atmospheric gas in air 10 meters(m) above ground level.

        Params:
        - gas (str): Gas whose concentration needs to be extracted, must be one of the following:
        ('ozone', 'carbon_monoxide', 'nitrogen_dioxide', 'sulphur_dioxide').
        """
        self._verify_atmospheric_gas(gas)
        return self._get_periodical_data({"hourly": gas})

    def get_hourly_ammonia_conc(self) -> pd.DataFrame:
        r"""
        Returns a pandas DataFrame of hourly concentration(micro g/m^3) data of ammonia(NH3)
        in air. Only available for Europe. Returns None for Non-European regions.
        """
        return self._get_periodical_data({"hourly": "ammonia"})