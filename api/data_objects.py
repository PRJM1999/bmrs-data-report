from dataclasses import dataclass
from typing import List

@dataclass
class EnergyDataPoint:
    """Represents a single energy data point."""
    settlement_period: int
    start_time: str
    system_sell_price: float
    system_buy_price: float
    net_imbalance_volume: float

@dataclass
class EnergyDataObject:
    """Represents energy data for a specific date."""
    settlement_date: str
    data_points: List[EnergyDataPoint]