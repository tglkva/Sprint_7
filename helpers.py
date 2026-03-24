import requests
import random
import string
import allure
from data import *
from logical_modules import *

@allure.step('Создание нового курьера')
# метод регистрации нового курьера возвращает список из логина и пароля
# если регистрация не удалась, возвращает пустой список
def register_new_courier_and_return_login_password():
    # метод генерирует строку, состоящую только из букв нижнего регистра, в качестве параметра передаём длину строки
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    # создаём список, чтобы метод мог его вернуть
    login_pass = []

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

    result = get_request_status_and_data(
        'https://qa-scooter.praktikum-services.ru/api/v1/courier',
        method='POST',
        payload=payload
    )

    if result['success'] and result['status_code'] == 201:
        return [login, password, first_name, result]
    else:
        error_msg = result.get('error', f'Статус {result["status_code"]}')
        return None

