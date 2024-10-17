from flask import Flask 
from flask_restful import Api
from flask_cors import CORS
from api.endpoints import DailyImbalance, HighestImbalanceHour
import logging

# Create App
app = Flask(__name__)
api = Api(app)

# Enable CORS
CORS(app)

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Add resources to the API
api.add_resource(DailyImbalance, '/daily_imbalance')
api.add_resource(HighestImbalanceHour, '/highest_imbalance_hour')

@app.route('/')
def index():
    """
    Test route to check server is running.
    """
    return "Server is running"