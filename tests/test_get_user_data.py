import httpx
from jsonschema import validate
from core.contracts import USER_DATA_SCHEME
import allure

BASE_URL = "https://reqres.in/"
LIST_USERS = "api/users?page=2"
SINGLE_USER = "api/users/2"
NOT_FOUND_USER = "api/users/23"
EMAIL_ENDS = "@reqres.in"
AVATAR_ENDS = "-image.jpg"
API_KEY = "reqres-free-v1"

@allure.suite('Проверка запросов данных пользователей')
@allure.title('Проверяем получение списка пользователей')
def test_list_users():
    headers = {
        "X-API-Key": API_KEY
    }
    with allure.step(f'Делаем запрос по адресу: {BASE_URL + LIST_USERS}'):
        response = httpx.get(BASE_URL + LIST_USERS, headers=headers)

    with allure.step('Проверяем код ответа'):
        assert response.status_code == 200

    data = response.json()['data']
    for item in data:
        with allure.step(f'Проверяем элемент из списка'):
            validate(item, USER_DATA_SCHEME)
            with allure.step('Проверяем окончание Email адреса'):
                assert item['email'].endswith(EMAIL_ENDS)
            with allure.step('Проверяем наличие id в ссылке на аватар'):
                assert str(item ['id']) in item['avatar']
            with allure.step('Проверяем окончание ссылки на аватар'):
                assert item['avatar'].endswith(str(item['id']) + AVATAR_ENDS)

@allure.title('Проверяем получение одного пользователя')
def test_single_user():
    headers = {
        "X-API-Key": API_KEY
    }
    with allure.step(f'Делаем запрос по адресу: {BASE_URL + SINGLE_USER}'):
        response = httpx.get(BASE_URL + SINGLE_USER, headers=headers)
    with allure.step('Проверяем код ответа'):
        assert response.status_code == 200

    data = response.json()['data']
    with allure.step('Проверяем окончание Email адреса'):
        assert data['email'].endswith(EMAIL_ENDS)
    with allure.step('Проверяем наличие id в ссылке на аватар'):
        assert str(data['id']) in data['avatar']
    with allure.step('Проверяем окончание ссылки на аватар'):
        assert data['avatar'].endswith(str(data['id']) + AVATAR_ENDS)

@allure.title('Проверяем ответ для несуществующего пользователя')
def test_user_not_found():
    headers = {
        "X-API-Key": API_KEY
    }
    with allure.step(f'Делаем запрос по адресу: {BASE_URL + NOT_FOUND_USER}'):
        response = httpx.get(BASE_URL + NOT_FOUND_USER, headers=headers)
    with allure.step('Проверяем код ответа'):
        assert response.status_code == 404

