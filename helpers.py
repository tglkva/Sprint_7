import requests
import random
import string
import allure
from data import *

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
        print(f"✓ Курьер успешно создан: логин='{login}'")
        return [login, password, first_name, result]
    else:
        error_msg = result.get('error', f'Статус {result["status_code"]}')
        print(f"✗ Ошибка регистрации курьера: {error_msg}")
        return None

@allure.step('Удаление курьера')
def delete_courier(courier_id):

    url = f'https://qa-scooter.praktikum-services.ru/api/v1/courier/{courier_id}'
    payload = {
        'id': str(courier_id)
    }
    try:
        response = requests.delete(url, json=payload, timeout=5)

        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data.get('ok') is True:
                    return {
                'success': True,
                'status_code': response.status_code,
                'response_data': response_data
            }
                else:
                    error_msg = response_data.get('message', 'Unknown error')
                    return {
                'success': False,
                'status_code': response.status_code,
                'response_data': response_data,
                'error_message': error_msg
            }
            except ValueError:  
                return {
                    'success': False,
            'status_code': response.status_code,
            'response_data': None,
            'error_message': 'Invalid JSON response'
        }
        else:
            try:
                response_data = response.json()
                error_msg = response_data.get('message', f'HTTP {response.status_code}')
            except ValueError:
                error_msg = f'HTTP {response.status_code}, invalid JSON'
            return {
                'success': False,
                'status_code': response.status_code,
                'response_data': response_data if 'response_data' in locals() else None,
                'error_message': error_msg
            }
    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'status_code': None,
            'response_data': None,
            'error_message': f'Request failed: {str(e)}'
        }

@allure.step('Получение ID курьера')
def get_courier_id(login, password):

    payload = {
        "login": login,
        "password": password
    }

    try:
        response = requests.post(API_URL_LOGIN, json=payload, timeout=5)

        if response.status_code == 200:
            data = response.json()
            courier_id = data.get('id')

            if courier_id is not None:
                return courier_id
            else:
                return None
        else:
            return None

    except Exception as e:
        print(f"✗ Произошла ошибка: {e}")
        return None
    
@allure.step('Создание заказа')
def create_order(color=None):
    payload = {
        'firstName': 'Иван',
        'lastName': 'Иванов',
        'address': 'Проспект мира 30',
        'metroStation': 1,
        'phone': '89654567865',
        'rentTime': 1,
        'deliveryDate': '2026-03-25',  
        'comment': 'Тестовый заказ'
    }

    if color is not None:
        payload['color'] = color

    try:
        response = requests.post(
            API_ORDER,
            json=payload,
            timeout=5
        )
        response_data = response.json()

        if 'color' not in response_data:
            response_data['color'] = color if color is not None else []

        if response.status_code == 201:
            return {
                'success': True,
                'status_code': response.status_code,
                'response_data': response_data,
                'order_id': response_data.get('track')
            }
        else:
            return {
                'success': False,
                'status_code': response.status_code,
                'error_message': f"Неожиданный статус: {response.status_code}",
                'response_data': response_data
            }

    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'error_message': f"Ошибка сети: {e}"
        }
    except ValueError:
        return {
            'success': False,
            'error_message': "Ответ API не является валидным JSON"
        }

@allure.step('Получение статуса и данных ответа')
def get_request_status_and_data(url, method='POST', payload=None, timeout=5):
   
    try:
        if method.upper() == 'GET':
            response = requests.get(url, timeout=timeout)
        elif method.upper() == 'POST':
            response = requests.post(url, json=payload, timeout=timeout)
        elif method.upper() == 'DELETE':
            response = requests.delete(url, timeout=timeout)
        else:
            return {
                'status_code': None,
                'response_data': None,
                'success': False,
                'error': f'Метод {method} не поддерживается'
            }

        try:
            response_data = response.json()
        except ValueError:
            response_data = {}

        return {
            'status_code': response.status_code,
            'response_data': response_data,
            'success': True,
            'error': None
        }

    except requests.exceptions.RequestException as e:
        return {
            'status_code': None,
            'response_data': None,
            'success': False,
            'error': str(e)
        }
@allure.step('Авторизация курьера')
def get_courier_auth_result(login, password):
    payload = {
        "login": login,
        "password": password
    }
    try:
        response = requests.post(
            API_URL_LOGIN,
            json=payload,
            timeout=5
        )
        return {
            'success': True,
            'status_code': response.status_code,
            'response_data': response.json()
        }
    except requests.exceptions.RequestException as e:
        return {'success': False, 'error': str(e)}
    except ValueError:
        return {'success': False, 'error': 'Invalid JSON response'}