import requests
import random
import string
import pytest
import allure
from helpers import *
from data import *
from conftest import *
from helpers import *



class TestCourierAuthorization:

    @allure.title('Проверка успешной авторизации курьера')
    @allure.description('Создание и авторизация курьера с верно заполненными полями логин и пароль')

    def test_courier_can_authorize_successfully(self, registered_courier):

        courier_data = register_new_courier_and_return_login_password()


        login, password, first_name = courier_data[:3]

        registered_courier['login'] = login
        registered_courier['password'] = password

        auth_result = get_courier_auth_result(login, password)

        assert auth_result['success'] is True
        assert auth_result['status_code'] == 200
        assert 'id' in auth_result['response_data']



    @pytest.mark.parametrize(
        'missing_field, expected_keywords, case_description',
        [
            ('login', ['Недостаточно данных', 'для входа'], 'Отсутствует поле login'),
            ('password', ['Недостаточно данных', 'для входа'], 'Отсутствует поле password'),
        ],
        ids=[
            'Missing login field',
            'Missing password field'
        ]
    )

    @allure.title('Проверка невозможности авторизации с отсутствующими обязательными полями')
    @allure.description('Попытка авторизации с незаполненными полями логин или пароль')

    def test_authorize_missing_required_fields(self, missing_field, expected_keywords, case_description):
        base_payload = {
            "login": "valid_login_123",
            "password": "valid_password_123"
        }

        payload = base_payload.copy()
        payload.pop(missing_field, None)  

        response = requests.post(
            API_URL_LOGIN,
            json=payload,
            timeout=10
        )

        assert response.status_code == 400

    @pytest.mark.parametrize(
        'incorrect_field, incorrect_value, expected_keywords, case_description',
        [
            ('login', 'nonexistent_login', ['Учётная запись', 'не найдена'], 'Неправильный логин'),
            ('password', 'wrong_password', ['Учётная запись', 'не найдена'], 'Неправильный пароль'),
        ],
        ids=[
            'Incorrect login',
            'Incorrect password'
        ]
    )
    @allure.title('Проверка невозможности авторизации с неправильными учетными данными')

    def test_authorize_with_incorrect_credentials(self, incorrect_field, incorrect_value, expected_keywords, case_description):

        courier_data = register_new_courier_and_return_login_password()


        valid_login, valid_password, first_name = courier_data[:3]

        test_login = incorrect_value if incorrect_field == 'login' else valid_login
        test_password = incorrect_value if incorrect_field == 'password' else valid_password


        auth_result = get_courier_auth_result(test_login, test_password)

        assert auth_result['success'] is True
        assert auth_result['status_code'] == 404

    @allure.title('Проверка авторизации несуществующего курьера')
    def test_authorize_nonexistent_courier(self):
    
        nonexistent_login = "nonexistent_user_123"
        nonexistent_password = "random_password_456"

        auth_result = get_courier_auth_result(nonexistent_login, nonexistent_password)

        assert auth_result['success'] is True
        assert auth_result['status_code'] == 404