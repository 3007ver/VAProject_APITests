
import httpx
from jsonschema import validate
from core.contracts import RESOURCE_DATA_SCHEME
import allure

BASE_URL = "https://reqres.in/"
LIST_RESOURCE = "api/unknown"
SINGLE_RESOURCE = "api/unknown/2"
NOT_FOUND_RESOURCE = "api/unknown/23"
API_KEY = "reqres-free-v1"

@allure.suite('Проверка списка ресурсов')
@allure.title('Проверяем получения списка ресурсов')
def test_get_list_resource():
    headers = {
        "X-API-Key": API_KEY
    }
    with allure.step(f'Делаем запрос по адресу: {BASE_URL + LIST_RESOURCE}'):
        response = httpx.get(BASE_URL + LIST_RESOURCE, headers=headers)
    with allure.step('Проверяем код ответа'):
        assert response.status_code == 200

    data = response.json()['data']
    ids = [item['id'] for item in data]
    with allure.step('Проверяем уникальность id'):
        assert len(ids) == len(set(ids))

    for item in data:
        with allure.step(f'Проверяем элемент из списка'):
            validate(item, RESOURCE_DATA_SCHEME)
            with allure.step(f'Проверяем, что значение цвета начинается с #'):
                assert item['color'].startswith("#")
            with allure.step(f'Проверяем диапазон значений года'):
                assert 1900 < item['year'] < 2100
            with allure.step(f'Проверяем наличие дефисав значении'):
                assert "-" in item['pantone_value']

@allure.title('Проверяем получения ресурса')
def test_get_single_resource():
    headers = {
        "X-API-Key": API_KEY
    }
    with allure.step(f'Делаем запрос по адресу: {BASE_URL + SINGLE_RESOURCE}'):
        response = httpx.get(BASE_URL + SINGLE_RESOURCE, headers=headers)
    with allure.step('Проверяем код ответа'):
        assert response.status_code == 200

    data = response.json()['data']
    validate(data, RESOURCE_DATA_SCHEME)
    with allure.step(f'Проверяем, что значение цвета начинается с #'):
        assert data['color'].startswith("#")
    with allure.step(f'Проверяем диапазон значений года'):
        assert 1900 < data['year'] < 2100
    with allure.step(f'Проверяем наличие дефисав значении'):
        assert "-" in data['pantone_value']

@allure.title('Проверяем ответ для несуществующего ресурса')
def test_not_found_resource():
    headers = {
        "X-API-Key": API_KEY
    }
    with allure.step(f'Делаем запрос по адресу: {BASE_URL + NOT_FOUND_RESOURCE}'):
        response = httpx.get(BASE_URL + NOT_FOUND_RESOURCE, headers=headers)
    with allure.step('Проверяем код ответа'):
        assert response.status_code == 404


