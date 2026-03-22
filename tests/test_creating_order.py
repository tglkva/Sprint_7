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
            (['BLACK'], ['BLACK']),
            (['GREY'], ['GREY']),
            (['BLACK', 'GREY'], ['BLACK', 'GREY'])
        ],
        ids=[
            'No color selected',
            'Only black color',
            'Only grey color',
            'Black and grey colors'
        ]
    )
    def test_create_order_with_different_colors_success(self, color_value, expected_color):
        result = create_order(color=color_value)

        assert result.get('success') is True

        order_track = result.get('order_id')
        assert order_track is not None

        response_data = result.get('response_data', {})
        assert isinstance(response_data, dict)

        actual_color = response_data.get('color', [])

        assert actual_color == expected_color