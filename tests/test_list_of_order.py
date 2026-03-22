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

        payload = ORDER_PAYLOAD_1
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

