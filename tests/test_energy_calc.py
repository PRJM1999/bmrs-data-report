import pytest
from datetime import datetime, timedelta, date
from unittest.mock import patch
from api.data_objects import EnergyDataObject, EnergyDataPoint
from api.energy_calc import get_previous_day_uk, calculate_daily_imbalance, find_highest_imbalance_hour


@pytest.fixture
def sample_energy_data():
    return EnergyDataObject(
        settlement_date=date(2023, 5, 1),
        data_points=[
            EnergyDataPoint(
                settlement_period=0,
                start_time="2023-05-01T00:00:00Z",
                system_sell_price=10.0,
                system_buy_price=15.0,
                net_imbalance_volume=-50.0
            ),
            EnergyDataPoint(
                settlement_period=1,
                start_time="2023-05-01T00:30:00Z",
                system_sell_price=12.0,
                system_buy_price=18.0,
                net_imbalance_volume=30.0
            ),
            EnergyDataPoint(
                settlement_period=2,
                start_time="2023-05-01T01:00:00Z",
                system_sell_price=11.0,
                system_buy_price=16.0,
                net_imbalance_volume=40.0
            )
        ]
    )


def test_get_previous_day_uk():
    with patch('api.energy_calc.datetime') as mock_datetime, \
         patch('api.energy_calc.time') as mock_time:
        # Mock the current time
        mock_datetime.utcnow.return_value = datetime(2023, 5, 2, 12, 0, 0)
        mock_time.localtime.return_value.tm_hour = 13
        mock_time.gmtime.return_value.tm_hour = 12

        result = get_previous_day_uk()
        assert result == "2023-05-01"

def test_calculate_daily_imbalance(sample_energy_data):
    total_cost, unit_rate = calculate_daily_imbalance(sample_energy_data)
    
    # Calculate expected values
    expected_cost = 1680
    expected_volume = 50 + 30 + 40
    expected_rate = expected_cost / expected_volume

    assert pytest.approx(total_cost, 0.01) == expected_cost
    assert pytest.approx(unit_rate, 0.01) == expected_rate


def test_find_highest_imbalance_hour(sample_energy_data):
    max_hour, max_volume = find_highest_imbalance_hour(sample_energy_data)

    assert max_hour == 0  # The highest imbalance is in hour 0
    assert pytest.approx(max_volume, 0.01) == 80.0  # 50 + 30 MWh


def test_calculate_daily_imbalance_zero():
    zero_data = EnergyDataObject(
        settlement_date=date(2023, 5, 1),
        data_points=[
            EnergyDataPoint(
                settlement_period=1,
                start_time="2023-05-01T00:00:00Z",
                system_sell_price=10.0,
                system_buy_price=15.0,
                net_imbalance_volume=0.0
            )
        ]
    )
    total_cost, unit_rate = calculate_daily_imbalance(zero_data)
    assert total_cost == 0
    assert unit_rate == 0