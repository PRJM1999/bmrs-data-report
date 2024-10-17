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
    valid_date = (date.today() - timedelta(days=2)).isoformat()
    mock_response = Mock()
    mock_response.status_code = 200

    # Generate 48 data points
    data_points = []
    start_time = datetime.fromisoformat(valid_date)
    for i in range(1, 49):
        data_points.append({
            "settlementPeriod": i,
            "startTime": (start_time + timedelta(minutes=30 * (i-1))).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "systemSellPrice": 50.0 + i,
            "systemBuyPrice": 60.0 + i,
            "netImbalanceVolume": 100.0 + i,
        })

    mock_response.json.return_value = {"data": data_points}
    mock_get.return_value = mock_response

    # Act
    energy_data = fetcher.fetch_energy_data(valid_date)

    # Assert
    assert isinstance(energy_data, EnergyDataObject)
    assert energy_data.settlement_date == valid_date
    assert len(energy_data.data_points) == 48

    # Check the first and last data points
    assert energy_data.data_points[0].settlement_period == 1
    assert energy_data.data_points[0].start_time == start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    assert energy_data.data_points[0].system_sell_price == 51.0
    assert energy_data.data_points[0].system_buy_price == 61.0
    assert energy_data.data_points[0].net_imbalance_volume == 101.0

    assert energy_data.data_points[-1].settlement_period == 48
    assert energy_data.data_points[-1].start_time == (start_time + timedelta(minutes=30 * 47)).strftime("%Y-%m-%dT%H:%M:%SZ")
    assert energy_data.data_points[-1].system_sell_price == 98.0
    assert energy_data.data_points[-1].system_buy_price == 108.0
    assert energy_data.data_points[-1].net_imbalance_volume == 148.0

@patch("api.data_retrieval.requests.get")
def test_fetch_energy_data_future_date(mock_get, fetcher):
    # Arrange
    future_date = (date.today() + timedelta(days=1)).isoformat()

    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        fetcher.fetch_energy_data(future_date)

    assert "Requested date must be at least one day in the past" in str(exc_info.value)

    # Ensure that the API was not called
    mock_get.assert_not_called()


# Integration Tests

def test_fetch_energy_data_integration(fetcher):
    # Arrange
    valid_date = (date.today() - timedelta(days=2)).isoformat()

    # Act
    energy_data = fetcher.fetch_energy_data(valid_date)

    # Assert
    assert isinstance(energy_data, EnergyDataObject)
    assert energy_data.settlement_date == valid_date
    assert len(energy_data.data_points) > 0
    assert len(energy_data.data_points) == 48 