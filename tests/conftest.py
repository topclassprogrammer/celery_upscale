from _pytest.fixtures import fixture
from api_client import APIClient
from config import API_URL


@fixture()
def api_client():
    return APIClient(API_URL)
