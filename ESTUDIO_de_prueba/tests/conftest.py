import pytest
import sys
import os

# Add the parent directory to the Python path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

@pytest.fixture
def sample_data():
    """Fixture that provides sample data for tests"""
    return {
        'test_value': 42,
        'test_string': 'hello world',
        'test_list': [1, 2, 3, 4, 5]
    }

@pytest.fixture
def mock_config():
    """Fixture that provides mock configuration"""
    return {
        'api_key': 'test_api_key',
        'base_url': 'https://test.example.com',
        'timeout': 30
    }

@pytest.fixture(scope="session")
def setup_test_environment():
    """Session-scoped fixture for test environment setup"""
    # Setup code here
    yield
    # Teardown code here
    pass