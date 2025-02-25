import requests
import allure

from helpers.data import COURIER_MESSAGE_LOGIN_NOT_FOUND, COURIER_MESSAGE_EMPTY_LOGIN
from helpers.utils import register_new_courier_and_return_login_password
from helpers.urls import COURIER_LOGIN_URL


@allure.feature('Login')
class TestLogin:

    @allure.title("Успешный логин")
    def test_login_courier(self):
        login, password, _ = register_new_courier_and_return_login_password(False)
        payload = {
            "login": login,
            "password": password,
        }
        response = requests.post(COURIER_LOGIN_URL, data=payload)
        assert response.status_code == 200
        assert 'id' in response.json()

    @allure.title("Логин с пустым поле login")
    def test_login_with_empty_login(self):
        payload = {
            "password": 'password'
        }
        response = requests.post(COURIER_LOGIN_URL, data=payload)
        assert response.status_code == 400
        assert response.json() == COURIER_MESSAGE_EMPTY_LOGIN

    @allure.title("Логин с пустым password")
    def test_login_with_empty_password(self):
        payload = {
            "login": 'login'
        }
        response = requests.post(COURIER_LOGIN_URL, data=payload)
        assert response.status_code == 504

    @allure.title("Логин с неверными данными")
    def test_login_with_invalid_date(self):
        payload = {
            "login": 'login',
            "password": 'password'
        }
        response = requests.post(COURIER_LOGIN_URL, data=payload)
        assert response.status_code == 404
        assert response.json() == COURIER_MESSAGE_LOGIN_NOT_FOUND
