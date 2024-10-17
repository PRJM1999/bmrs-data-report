from api.data_objects import EnergyDataObject, EnergyDataPoint
from datetime import datetime, timedelta
import time
from typing import Tuple

def get_previous_day_uk() -> str:
    """
    Get the date of the previous day in UK time, in ISO format (YYYY-MM-DD).
    """
    # Get the current time in UTC
    utc_now = datetime.utcnow()
    
    # Convert UTC to UK time (considering daylight saving time)
    uk_offset = time.localtime().tm_hour - time.gmtime().tm_hour
    uk_time = utc_now + timedelta(hours=uk_offset)
    
    # Calculate the previous day
    previous_day = uk_time - timedelta(days=1)
    
    # Return the date in ISO format
    return previous_day.date().isoformat()


def calculate_daily_imbalance(energy_data: EnergyDataObject) -> Tuple[float, float]:
    """
    Calculates the total daily imbalance cost and daily imbalance unit rate.

    Args:
        energy_data: An EnergyDataObject containing the day's energy data.

    Returns:
        A tuple containing:
        - total_daily_imbalance_cost: The total cost of imbalances for the day.
        - daily_imbalance_unit_rate: The average cost per unit of imbalance volume.
    """
    total_imbalance_cost = 0.0
    total_imbalance_volume = 0.0

    for data_point in energy_data.data_points:
        # Calculate the imbalance cost for this settlement period
        imbalance_volume = abs(data_point.net_imbalance_volume)
        imbalance_price = max(data_point.system_buy_price, data_point.system_sell_price)
        period_imbalance_cost = imbalance_volume * imbalance_price

        # Accumulate the total cost and volume
        total_imbalance_cost += period_imbalance_cost
        total_imbalance_volume += imbalance_volume

    # Calculate the daily imbalance unit rate
    if total_imbalance_volume > 0:
        daily_imbalance_unit_rate = total_imbalance_cost / total_imbalance_volume
    else:
        daily_imbalance_unit_rate = 0.0

    return total_imbalance_cost, daily_imbalance_unit_rate


def find_highest_imbalance_hour(energy_data: EnergyDataObject) -> Tuple[int, float]:
    """
    Finds the hour with the highest absolute imbalance volume.

    Args:
        energy_data: An EnergyDataObject containing the day's energy data.

    Returns:
        A tuple containing the hour (0-23) and the highest absolute imbalance volume.
    """
    hourly_imbalance = [0] * 24
    for point in energy_data.data_points:
        hour = datetime.fromisoformat(point.start_time.rstrip('Z')).hour
        hourly_imbalance[hour] += abs(point.net_imbalance_volume)
    
    max_hour = max(range(24), key=lambda i: hourly_imbalance[i])
    return max_hour, hourly_imbalance[max_hour]