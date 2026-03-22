import pytest
import requests
from helpers import *
from data import *




@pytest.fixture
def registered_courier():

    payload = {
        'courier_id': None,
        'login': None,
        'password': None
    }
    yield payload

    if payload['courier_id'] is not None:
        result = delete_courier(payload['courier_id'])

@pytest.fixture
def delete_test_data(self):
    self.created_couriers = []
    yield

    for courier_id in self.created_couriers:
        delete_result = delete_courier(courier_id)
        if not delete_result['success']:
            print(f'Не удалось удалить курьера с ID {courier_id}')

