import requests
import random
import string
import pytest
import time
import allure
from data import *



class TestCreateOrderAndVerifyInList:

    @allure.title('Проверка наличия заказа в теле ответа при получении списка заказов')

    def test_create_order_and_verify_in_list(self):
        payload = {
            "firstName": "Иван",
            "lastName": "Иванов",
            "address": "Проспект мира 40",
            "metroStation": 4,
            "phone": "+7 867 334 38 90",
            "rentTime": 5,
            "deliveryDate": "2026-03-27",
            "comment": " ",
            "color": ["BLACK"]
        }

        create_resp = requests.post(
            API_ORDER,
            json=payload,
            timeout=30
        )
        assert create_resp.status_code == 201


        list_resp = requests.get(
            API_ORDER,
            timeout=30
        )

        assert list_resp.status_code == 200, f"Ожидали 200, получили {list_resp.status_code}"

        data = list_resp.json()
        assert "orders" in data, "В ответе отсутствует поле 'orders'"

