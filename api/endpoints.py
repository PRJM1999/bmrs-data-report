from flask_restful import Resource
from flask import jsonify
import logging
from api.energy_calc import get_previous_day_uk, calculate_daily_imbalance, find_highest_imbalance_hour
from api.data_retrieval import ElexonBrmsFetcher

class DailyImbalance(Resource):
    def get(self):
        """
        Get the total daily imbalance cost and daily imbalance unit rate for the previous day in UK time.
        """
        fetcher = ElexonBrmsFetcher()
        previous_day = get_previous_day_uk()

        try:
            energy_data = fetcher.fetch_energy_data(previous_day)
            if energy_data is None:
                logging.warning(f"No data available for {previous_day}")
                return {"error": "No data available for the previous day"}, 404

            total_cost, daily_rate = calculate_daily_imbalance(energy_data)

            response = {
                "date": previous_day,
                "total_daily_imbalance_cost": round(total_cost, 2),
                "daily_imbalance_unit_rate": round(daily_rate, 2)
            }
            logging.info(f"Daily imbalance calculated for {previous_day}: {response}")
            return response

        except ValueError as e:
            logging.error(f"ValueError in daily_imbalance: {str(e)}")
            return {"error": str(e)}, 400
        except Exception as e:
            logging.error(f"Unexpected error in daily_imbalance: {str(e)}")
            return {"error": "An unexpected error occurred"}, 500

class HighestImbalanceHour(Resource):
    def get(self):
        """
        Report which hour had the highest absolute imbalance volumes for the previous day in UK time.
        """
        fetcher = ElexonBrmsFetcher()
        previous_day = get_previous_day_uk()

        try:
            energy_data = fetcher.fetch_energy_data(previous_day)
            if energy_data is None:
                logging.warning(f"No data available for {previous_day}")
                return {"error": "No data available for the previous day"}, 404

            max_hour, max_volume = find_highest_imbalance_hour(energy_data)

            response = {
                "date": previous_day,
                "highest_imbalance_hour": max_hour,
                "highest_imbalance_volume": round(max_volume, 2)
            }
            logging.info(f"Highest imbalance hour calculated for {previous_day}: {response}")
            return response

        except ValueError as e:
            logging.error(f"ValueError in highest_imbalance_hour: {str(e)}")
            return {"error": str(e)}, 400
        except Exception as e:
            logging.error(f"Unexpected error in highest_imbalance_hour: {str(e)}")
            return {"error": "An unexpected error occurred"}, 500