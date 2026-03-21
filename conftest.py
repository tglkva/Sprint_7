import pytest
import requests
from helpers import *
from data import *




@pytest.fixture
def registered_courier():
    class CourierContainer:
        def __init__(self):
            self.courier_id = None
            self.login = None
            self.password = None

    container = CourierContainer()
    yield container

    # Очистка после теста
    if container.courier_id is not None:
        result = delete_courier(container.courier_id)
        if result['success']:
            print(f"Курьер ID '{container.courier_id}' успешно удалён")
        else:
            print(
                f"Проблема при удалении курьера ID '{container.courier_id}': "
                f"{result['error_message']}"
            )


@pytest.fixture
def delete_test_data(self):
    self.created_couriers = []
    yield

    for courier_id in self.created_couriers:
        delete_result = delete_courier(courier_id)
        if not delete_result['success']:
            print(f'Не удалось удалить курьера с ID {courier_id}')

