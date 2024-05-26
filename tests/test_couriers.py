import allure
import requests
import helpers
import urls
from helpers import register_new_courier_and_return_login_password


class TestCourierCreation:
    @allure.title('Создание нового курьера')
    def test_create_new_courier_success(self):
        payload = helpers.generate_new_courier_data()
        response = requests.post(urls.MAIN_URL+urls.CREATE_COURIER, data=payload)
        helpers.delete_courier({'login': payload['login'], 'password': payload['password']})
        assert response.status_code == 201 and response.json() == {'ok': True}

    @allure.title('Невозможно создать дубликат уже существующего курьера')
    def test_creating_duplicate_courier_failed(self):
        payload = helpers.generate_new_courier_data()
        requests.post(urls.MAIN_URL + urls.CREATE_COURIER, data=payload)
        response = requests.post(urls.MAIN_URL + urls.CREATE_COURIER, data=payload)
        assert (response.status_code == 409 and
                response.json()["message"] == 'Этот логин уже используется. Попробуйте другой.')

    @allure.title('Невозможно создать курьера без обязательного поля login')
    def test_creating_courier_without_login_failed(self):
        payload = {'login': '', 'password': '21', 'firstName': 'kapee'}
        response = requests.post(urls.MAIN_URL + urls.CREATE_COURIER, data=payload)
        assert (response.status_code == 400 and
                response.json()['message'] == "Недостаточно данных для создания учетной записи")

    @allure.title('Невозможно создать курьера без обязательного поля password')
    def test_creating_courier_without_password_failed(self):
        payload = {'login': 'kapee?', 'password': '', 'firstName': 'kapee'}
        response = requests.post(urls.MAIN_URL + urls.CREATE_COURIER, data=payload)
        assert (response.status_code == 400 and
                response.json()['message'] == "Недостаточно данных для создания учетной записи")


class TestCourierLogin:

    @allure.title('Успешная авторизация зарегистрированного курьера')
    def test_courier_login_successfully(self):
        new_courier_data = helpers.register_new_courier_and_return_login_password()
        auth_data = {'login': new_courier_data[0], 'password': new_courier_data[1]}
        response = requests.post(urls.MAIN_URL + urls.LOGIN_COURIER, data=auth_data)
        helpers.delete_courier(auth_data)
        assert response.status_code == 200 and 'id' in response.json()

    @allure.title('Невозможно авторизоваться без указанного логина')
    def test_courier_login_without_login_failed(self):
        new_courier_data = register_new_courier_and_return_login_password()
        auth_data = {'login': '', 'password': new_courier_data[1]}
        response = requests.post(urls.MAIN_URL + urls.LOGIN_COURIER, data=auth_data)
        assert response.status_code == 400 and response.json()['message'] == 'Недостаточно данных для входа'

    @allure.title('Невозможно авторизоваться без указанного пароля')
    def test_courier_login_without_password_failed(self):
        new_courier_data = register_new_courier_and_return_login_password()
        auth_data = {'login': new_courier_data[0], 'password': ''}
        response = requests.post(urls.MAIN_URL + urls.LOGIN_COURIER, data=auth_data)
        assert response.status_code == 400 and response.json()['message'] == 'Недостаточно данных для входа'

    @allure.title('Невозможно авторизоваться используя несуществующие данные учетной записи')
    def test_courier_login_with_non_existing_data_failed(self):
        auth_data = {'login': 'DoctorHouseMD', 'password': 'Gregory'}
        response = requests.post(urls.MAIN_URL + urls.LOGIN_COURIER, data=auth_data)
        assert response.status_code == 404 and response.json()['message'] == 'Учетная запись не найдена'


