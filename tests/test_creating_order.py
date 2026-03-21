import requests
import random
import string
import pytest
import allure
from helpers import *
from data import *
from conftest import *

class TestCreatingOrder:


    @allure.title('Проверка создания заказа с возможностью выбора разных цветов')
    @pytest.mark.parametrize(
        'color_value, expected_color',
        [
            (None, []),
            (['black'], ['black']),
            (['grey'], ['grey']),
            (['black', 'grey'], ['black', 'grey'])
        ],
        ids=[
            'No color selected',
            'Only black color',
            'Only grey color',
            'Black and grey colors'
        ]
    )


    def test_create_order_with_different_colors_success(self,color_value, expected_color):
        result = create_order(color=color_value)


        assert result['success'] is True, f"Заказ не создан: {result.get('error_message', '')}"

        order_track = result['order_id']
        assert order_track is not None

        response_data = result['response_data']
        if 'color' in response_data:
            assert response_data['color'] == expected_color, (
                f"Неверный цвет в заказе. Ожидалось: {expected_color}, получено: {response_data['color']}"
            )