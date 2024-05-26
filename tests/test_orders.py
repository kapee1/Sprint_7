import allure
import pytest
import requests
import urls
import helpers


class TestOrderCreation:

    @allure.title('Создание нового заказа без заполнения необязательного поля "цвет"')
    def test_new_order_without_colour_creates_successfully(self):
        payload = helpers.generate_required_order_details()
        response = requests.post(urls.MAIN_URL+urls.CREATE_ORDER, data=payload)
        assert response.status_code == 201 and 'track' in response.json()

    @allure.title('Создание нового заказа с различными вариантами поля "цвет"')
    @pytest.mark.parametrize('color', ["BLACK", 'GREY', 'BLACK, GREY'])
    def test_new_order_with_any_colors_creates_successfully(self, color):
        payload = helpers.generate_required_order_details()
        payload.setdefault(color, []).append(color)
        response = requests.post(urls.MAIN_URL + urls.CREATE_ORDER, data=payload)
        assert response.status_code == 201 and 'track' in response.json()


class TestOrdersList:

    @allure.title('Получения списка заказов использую разное количество выводимых результатов')
    @pytest.mark.parametrize('limit', [1, 10, 30])
    def test_get_list_of_limited_quantity_of_orders(self, limit):
        response = requests.get(urls.MAIN_URL + urls.GET_ORDERS_LIST+f'?limit={limit}&page=0')
        assert response.status_code == 200 and response.json()['pageInfo']['limit'] == limit


