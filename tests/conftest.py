import sys
from pathlib import Path

# Add project root to Python path for module imports
root_dir = Path(__file__).parent.parent
src_dir = root_dir

sys.path.insert(0, str(src_dir))

import pytest
from api import app as flask_app

# Provide the Flask app instance for tests
@pytest.fixture
def app():
    return flask_app

# Set up an app context for tests that need it
@pytest.fixture
def app_context(app):
    with app.app_context():
        yield

# Provide a test client to simulate HTTP requests
@pytest.fixture
def client(app):
    return app.test_client()