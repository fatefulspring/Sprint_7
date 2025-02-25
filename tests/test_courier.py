import requests
import pytest
import allure

from helpers.data import COURIER_MESSAGE_INVALID_LOGIN, COURIER_MESSAGE_EMPTY_FIELD
from helpers.utils import register_new_courier_and_return_login_password
from helpers.urls import COURIER_URL


@allure.feature('Курьер')
class TestCourier:
    @allure.title("Создание курьера")
    def test_create_courier(self):
        response = register_new_courier_and_return_login_password()
        assert response.status_code == 201
        assert response.json() == {'ok': True}

    @allure.title("Создание дубликата курьера")
    def test_create_duplicate_courier(self):
        login, password, first_name = register_new_courier_and_return_login_password(False)
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        response = requests.post(COURIER_URL, data=payload)
        assert response.status_code == 409
        assert response.json() == COURIER_MESSAGE_INVALID_LOGIN

    @allure.title("Создание курьера с пустыми полями")
    @pytest.mark.parametrize('field', ['login', 'password'])
    def test_create_courier_with_empty_field(self, field):
        payload = {
            "login": 'login',
            "password": 'password',
            "firstName": 'first_name'
        }
        payload.pop(field)
        response = requests.post(COURIER_URL, data=payload)
        assert response.status_code == 400
        assert response.json() == COURIER_MESSAGE_EMPTY_FIELD

