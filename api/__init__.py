from flask import Flask 
from flask_cors import CORS
import logging

# Create App
app = Flask(__name__)

# Enable CORS
CORS(app)

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/')
def index():
    """
    Test route to check server is running.
    """
    return "Server is running"