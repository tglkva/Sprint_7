import requests
import random
import string
import allure
from data import *



@allure.step('Удаление курьера')
def delete_courier(courier_id):
    url = f'https://qa-scooter.praktikum-services.ru/api/v1/courier/{courier_id}'
    
    try:
        response = requests.delete(url, timeout=5)
        return {
            'success': response.status_code == 200,
            'status_code': response.status_code,
            'response_data': response.json() if response.content else None
        }
    except Exception as e:
        return {
            'success': False,
            'status_code': None,
            'response_data': None,
            'error_message': str(e)
        }
    
@allure.step('Получение ID курьера')
def get_courier_id(login, password):
    payload = {"login": login, "password": password}
    try:
        response = requests.post(API_URL_LOGIN, json=payload, timeout=5)
        if response.status_code == 200:
            return response.json().get('id')
        return None
    except Exception:
        return None
    
@allure.step('Создание заказа')
def create_order(color=None):
    payload = ORDER_PAYLOAD_1
    
    if color is not None:
        payload['color'] = color

    response = requests.post(API_ORDER, json=payload, timeout=5)
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

@allure.step('Получение статуса и данных ответа')
def get_request_status_and_data(url, method='POST', payload=None, timeout=5):
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

    response_data = response.json()

    return {
        'status_code': response.status_code,
        'response_data': response_data,
        'success': True,
        'error': None
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