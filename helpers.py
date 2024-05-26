import allure
import requests
import random
from faker import Faker
import urls

@allure.step('Создаем нового курьера и возвращаем данные для авторизации')
def register_new_courier_and_return_login_password():
    fake = Faker()
    login_pass = []

    login = fake.name()
    password = fake.password(9)
    first_name = fake.first_name()

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)
    return login_pass

@allure.step('Генерируем данные для регистрации курьера')
def generate_new_courier_data():
    fake = Faker()
    payload = {
        "login": fake.email(),
        "password": fake.password(),
        "firstName": fake.first_name()
    }
    return payload


@allure.step('Создаем обязательные данные для заказа')
def generate_required_order_details():
    fake = Faker(['ru_RU'])
    payload = {
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
        "address": fake.address(),
        "metroStation": 4,
        "phone": fake.phone_number(),
        "rentTime": random.randint(1, 6),
        "deliveryDate": "2020-06-06",
        "comment": "Saske, come back to Konoha",

    }
    return payload


@allure.step('Удаляем созданного курьера')
def delete_courier(auth_data):
    response = requests.post(urls.MAIN_URL + urls.LOGIN_COURIER, data=auth_data)
    courier_id = str(response.json()['id'])
    del_response = requests.delete(urls.MAIN_URL + urls.DELETE_COURIER + courier_id, data={'id': courier_id})
    assert del_response.status_code == 200
