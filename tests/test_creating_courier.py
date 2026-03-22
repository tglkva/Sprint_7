import requests
import random
import string
import pytest
import allure
from helpers import *
from data import *
from conftest import *

class TestCreatingCourier:
    
    @allure.title('Проверка успешного создания курьера')
    def test_creating_courier_success(registered_courier):

        courier_result = register_new_courier_and_return_login_password()

        login, password, first_name, creation_result = courier_result

        assert creation_result['success'] is True
        assert creation_result['status_code'] == 201
        assert 'ok' in creation_result['response_data']
        assert creation_result['response_data']['ok'] is True

        courier_id = get_courier_id(login, password)

        registered_courier.courier_id = courier_id
        registered_courier.login = login
        registered_courier.password = password


    @allure.title('Проверка невозможности создать дубликат курьера')

    def test_creating_duplicate_courier_failed(registered_courier):

        unique_courier_data = register_new_courier_and_return_login_password()

        login, password, first_name, _ = unique_courier_data  

        payload = {
            "login": login,
            "password": "another_password",
            "firstName": "Дубликат"
        }

        result = get_request_status_and_data(
            API_URL_CREATE_COURIER,
            method='POST',
            payload=payload
        )

        assert result['success'] is True
        assert result['status_code'] == 409


    @allure.title('Проверка невозможности создать курьера с одним из незаполненных обязательных полей')
    @allure.description('Попытка создать курьера не заполнив одно из обязательных полей (логин или пароль)')
    @pytest.mark.parametrize(
        'missing_field, expected_error_message, case_description',
        [
            ('login', 'Недостаточно данных для создания учетной записи', 'Отсутствует поле login'),
            ('password', 'Недостаточно данных для создания учетной записи', 'Отсутствует поле password'),
        ],
        ids=[
            'Missing login field',
            'Missing password field'
        ]
    )
    def test_create_courier_missing_required_fields(self, missing_field, expected_error_message, case_description):
        base_payload = {
            "login": "valid_login_123",
            "password": "valid_password_123",
            "firstName": "Тестовый"
        }

        payload = base_payload.copy()
        payload.pop(missing_field, None)  

        response = requests.post(
            API_URL_CREATE_COURIER,
            json=payload,
            timeout=5
        )

        assert response.status_code == 409
 