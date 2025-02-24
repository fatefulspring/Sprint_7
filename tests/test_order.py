import requests
import pytest
import allure
from copy import copy

from .data import ORDER_CREATE_PAYLOAD, ORDER_LIST_KEYS
from .urls import ORDER_URL


@allure.feature('Заказ')
class TestOrder:

    @allure.title("Создание заказа")
    @pytest.mark.parametrize("color", [["BLACK"], ["GREY"], ["BLACK", "GREY"], []])
    def test_create_order(self, color):
        payload = copy(ORDER_CREATE_PAYLOAD)
        payload['color'] = color

        response = requests.post(ORDER_URL, json=payload)
        assert response.status_code == 201
        assert 'track' in response.json()

    @allure.title("Получение списка заказов")
    def test_get_order_list(self):
        response = requests.get(ORDER_URL)
        assert response.status_code == 200
        assert 'orders' in response.json()
        order = response.json()['orders'][0]
        assert order.keys() == ORDER_LIST_KEYS
