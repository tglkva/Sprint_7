import pytest
import requests
from helpers import *
from data import *




@pytest.fixture
def registered_courier():
    courier_result = register_new_courier_and_return_login_password()

    login, password, first_name, result = courier_result

    payload = {
        'courier_id': result.get('id'),
        'login': login,
        'password': password,
        'first_name': first_name
    }
    yield payload  
    delete_courier(payload['courier_id'])



