import requests
import random
import string
import pytest
import allure

BASE_URL = 'https://qa-scooter.praktikum-services.ru'


# метод регистрации нового курьера возвращает список из логина и пароля
# если регистрация не удалась, возвращает пустой список
def register_new_courier_and_return_login_password(return_response=True):
    # метод генерирует строку, состоящую только из букв нижнего регистра, в качестве параметра передаём длину строки
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    # генерируем логин, пароль и имя курьера
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    # собираем тело запроса
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    # отправляем запрос на регистрацию курьера и сохраняем ответ в переменную response
    response = requests.post(f'{BASE_URL}/api/v1/courier', data=payload)
    if return_response:
        return response

    if response.status_code == 201:
        return login, password, first_name


@allure.feature("Создание курьера")
def test_create_courier():
    response = register_new_courier_and_return_login_password()
    assert response.status_code == 201
    assert response.json() == {'ok': True}


@allure.feature("Создание дубликата курьера")
def test_create_duplicate_courier():
    login, password, first_name = register_new_courier_and_return_login_password(False)
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(f'{BASE_URL}/api/v1/courier', data=payload)
    assert response.status_code == 409
    assert response.json() == {
        "code": 409,
        "message": "Этот логин уже используется. Попробуйте другой."
    }


@allure.feature("Создание курьера с пустыми полями")
@pytest.mark.parametrize('field', ['login', 'password'])
def test_create_courier_with_empty_field(field):
    payload = {
        "login": 'login',
        "password": 'password',
        "firstName": 'first_name'
    }
    payload.pop(field)
    response = requests.post(f'{BASE_URL}/api/v1/courier', data=payload)
    assert response.status_code == 400
    assert response.json() == {'code': 400, 'message': 'Недостаточно данных для создания учетной записи'}


@allure.feature("Логин курьера")
def test_login_courier():
    login, password, _ = register_new_courier_and_return_login_password(False)
    payload = {
        "login": login,
        "password": password,
    }
    response = requests.post(f'{BASE_URL}/api/v1/courier/login', data=payload)
    assert response.status_code == 200
    assert 'id' in response.json()


@allure.feature("Логин курьера с пустыми полями")
@pytest.mark.parametrize('field, error_code, message',
                         [('login', 400, {'code': 400, 'message': 'Недостаточно данных для входа'}),
                          ('password', 504, None)])
def test_login_with_empty_field(field, error_code, message):
    payload = {
        "login": 'login',
        "password": 'password'
    }
    payload.pop(field)
    response = requests.post(f'{BASE_URL}/api/v1/courier/login', data=payload)
    assert response.status_code == error_code
    if message:
        assert response.json() == message


@allure.feature("Логин курьера с неверными данными")
def test_login_with_invalid_date():
    payload = {
        "login": 'login',
        "password": 'password'
    }
    response = requests.post(f'{BASE_URL}/api/v1/courier/login', data=payload)
    assert response.status_code == 404
    assert response.json() == {'code': 404, 'message': 'Учетная запись не найдена'}


@allure.feature("Создание заказа")
@pytest.mark.parametrize("color", [["BLACK"], ["GREY"], ["BLACK", "GREY"], []])
def test_create_order(color):
    payload = {
        "firstName": "Naruto",
        "lastName": "Uchiha",
        "address": "Konoha, 142 apt.",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2020-06-06",
        "comment": "Saske, come back to Konoha",
        "color": color
    }

    response = requests.post(f'{BASE_URL}/api/v1/orders', json=payload)
    assert response.status_code == 201
    assert 'track' in response.json()


@allure.feature("Получение списка заказов")
def test_get_order_list():
    response = requests.get(f'{BASE_URL}/api/v1/orders')
    assert response.status_code == 200
    assert 'orders' in response.json()
    order = response.json()['orders'][0]
    assert order.keys() == {'id', 'courierId', 'firstName', 'lastName', 'address', 'metroStation', 'phone', 'rentTime',
                            'deliveryDate', 'track', 'color', 'comment', 'createdAt', 'updatedAt', 'status'}
