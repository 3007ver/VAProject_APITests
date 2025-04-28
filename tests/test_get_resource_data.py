
import httpx
from jsonschema import validate
from core.contracts import RESOURCE_DATA_SCHEME

BASE_URL = "https://reqres.in/"
LIST_RESOURCE = "api/unknown"
SINGLE_RESOURCE = "api/unknown/2"
NOT_FOUND_RESOURCE = "api/unknown/23"
API_KEY = "reqres-free-v1"

def test_get_list_resource():
    headers = {
        "X-API-Key": API_KEY
    }
    response = httpx.get(BASE_URL + LIST_RESOURCE, headers=headers)
    assert response.status_code == 200
    data = response.json()['data']

    ids = [item['id'] for item in data]
    assert len(ids) == len(set(ids))

    for item in data:
        validate(item, RESOURCE_DATA_SCHEME)
        assert item['color'].startswith("#")
        assert 1900 < item['year'] < 2100
        assert "-" in item['pantone_value']

def test_get_single_resource():
    headers = {
        "X-API-Key": API_KEY
    }
    response = httpx.get(BASE_URL + SINGLE_RESOURCE, headers=headers)
    assert response.status_code == 200
    data = response.json()['data']

    validate(data, RESOURCE_DATA_SCHEME)
    assert data['color'].startswith("#")
    assert 1900 < data['year'] < 2100
    assert "-" in data['pantone_value']

def test_not_found_resource():
    headers = {
        "X-API-Key": API_KEY
    }
    response = httpx.get(BASE_URL + NOT_FOUND_RESOURCE, headers=headers)
    assert response.status_code == 404


