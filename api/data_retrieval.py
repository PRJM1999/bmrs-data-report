"""Module for retrieving energy data from various sources."""
from abc import ABC, abstractmethod
from typing import Optional
import requests
from requests.exceptions import RequestException
from api.data_objects import EnergyDataObject, EnergyDataPoint
from datetime import datetime


class EnergyDataFetcher(ABC):
    """Abstract base class for energy data fetchers."""

    @abstractmethod
    def fetch_energy_data(self, date: str) -> Optional[EnergyDataObject]:
        """
        Fetch energy data for a given date.
        This method must be implemented by all subclasses.

        Args:
            date (str): The settlement date in ISO format (YYYY-MM-DD).

        Returns:
            Optional[EnergyDataObject]: The energy data for the specified date, or None if not found.

        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
        """
        raise NotImplementedError("Subclasses must implement the fetch_energy_data method.")


class ElexonBrmsFetcher(EnergyDataFetcher):
    """Fetches energy data from the Elexon BMRS API."""

    _API_BASE_URL = "https://data.elexon.co.uk/bmrs/api/v1"

    def fetch_energy_data(self, date: str) -> Optional[EnergyDataObject]:
        """
        Fetch energy data for a given date from the Elexon BMRS API.

        Args:
            date (str): The settlement date in ISO format (YYYY-MM-DD).

        Returns:
            Optional[EnergyDataObject]: The energy data for the specified date, or None if not found.

        Raises:
            RequestException: If there is an error making the API request.
            ValueError: If the API response contains unexpected data.
        """
        # Check if the requested date is at least one day in the past
        try:
            requested_date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Invalid date format. Please use YYYY-MM-DD.")

        today = datetime.now().date()
        if requested_date >= today:
            raise ValueError("Requested date must be at least one day in the past.")
        
        endpoint = f"/balancing/settlement/system-prices/{date}"
        params = {"format": "json"}
        url = f"{self._API_BASE_URL}{endpoint}"

        try:
            response = requests.get(url, params=params)

            if response.status_code == 404:
                return None
        
            response.raise_for_status()

            data = response.json()["data"]
            energy_data = EnergyDataObject(date)

            for item in data:
                try:
                    data_point = EnergyDataPoint(
                        item["settlementPeriod"],
                        item["startTime"],
                        item["systemSellPrice"],
                        item["systemBuyPrice"],
                        item["netImbalanceVolume"],
                    )
                    energy_data.data_points.append(data_point)
                    print(item["startTime"])
                except KeyError as e:
                    raise ValueError(f"Unexpected data format in API response: {e}")
            
            # Check  expected number of data points
            if len(energy_data.data_points) != 48:
                raise ValueError(f"Incomplete data: received {len(energy_data.data_points)} data points instead of 48.")

            return energy_data

        except RequestException as e:
            if e.response is not None and e.response.status_code == 404:
                return None
            raise