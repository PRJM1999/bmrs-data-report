from api.data_retrieval import EnergyDataFetcher, ElexonBrmsFetcher, EnergyDataObject, EnergyDataPoint
import pytest
from unittest.mock import patch, Mock
from datetime import datetime, date, timedelta
import requests
from requests.exceptions import RequestException

@pytest.fixture
def fetcher():
    return ElexonBrmsFetcher()

# Unit Tests

@patch("api.data_retrieval.requests.get")
def test_fetch_energy_data_success(mock_get, fetcher):
    # Arrange
    valid_date = (date.today() - timedelta(days=1)).isoformat()
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "data": [
            {
                "settlementPeriod": 1,
                "startTime": "2023-05-18T00:00:00Z",
                "systemSellPrice": 50.0,
                "systemBuyPrice": 60.0,
                "netImbalanceVolume": 100.0,
            }
        ]
    }
    mock_get.return_value = mock_response

    # Act
    energy_data = fetcher.fetch_energy_data(valid_date)

    # Assert
    assert isinstance(energy_data, EnergyDataObject)
    assert energy_data.settlement_date == valid_date
    assert len(energy_data.data_points) == 1
    assert energy_data.data_points[0].settlement_period == 1
    assert energy_data.data_points[0].start_time == "2023-05-18T00:00:00Z"
    assert energy_data.data_points[0].system_sell_price == 50.0
    assert energy_data.data_points[0].system_buy_price == 60.0
    assert energy_data.data_points[0].net_imbalance_volume == 100.0

@patch("api.data_retrieval.requests.get")
def test_fetch_energy_data_not_found(mock_get, fetcher):
    # Arrange
    future_date = (date.today() + timedelta(days=1)).isoformat()
    mock_response = Mock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    # Act
    energy_data = fetcher.fetch_energy_data(future_date)

    # Assert
    assert energy_data is None


# Integration Tests

def test_fetch_energy_data_integration(fetcher):
    # Arrange
    valid_date = (date.today() - timedelta(days=1)).isoformat()

    # Act
    energy_data = fetcher.fetch_energy_data(valid_date)

    # Assert
    assert isinstance(energy_data, EnergyDataObject)
    assert energy_data.settlement_date == valid_date
    assert len(energy_data.data_points) > 0