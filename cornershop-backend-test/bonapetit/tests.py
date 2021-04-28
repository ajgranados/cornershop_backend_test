import json
from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient, URLPatternsTestCase

from .models import User, Person, Menu
from . import views
import uuid
from datetime import date

class UserTest(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('', include('bonapetit.urls')),
    ]

    def setUp(self):
        person1 = Person.objects.create(first_name = "Antonio", second_name = "Jesus", last_name = "Granados", email = "antonio.granados@gmail.com")
        person2 = Person.objects.create(first_name="Miguel", second_name="Jorge", last_name="Suarez", email="miguel.suarez@gmail.com")

        self.user1 = User.objects.create_user(
            email = 'test1@test.com',
            password = 'test',
            person = person1,
            role = 2
        )

        self.admin = User.objects.create_superuser(
            email = 'admin@test.com',
            password = 'admin',
            person = person2,
        )

    def test_login(self):
        data = {
            'email': 'admin@test.com',
            'password': 'admin'
        }
        response = self.client.post("/authenticate", data, format='json')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['success'], True)
        self.assertTrue('access' in response_data)

    def test_user_registration(self):
        data = {
            'email': 'test2@test.com',
            'password': 'test',
            "person": {
                "first_name": "test name",
                "second_name": "test second",
                "last_name": "test third",
                "email": "ttest2@test.com"
            },
            "role": 2
        }
        response = self.client.post("/user", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_all_users(self):
        data = {'email': 'test1@test.com', 'password': 'test'}
        response = self.client.post("/authenticate", data)
        login_response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in login_response_data)
        token = login_response_data['access']

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = client.get("/user")
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class MenuTest(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('', include('bonapetit.urls')),
    ]

    def setUp(self):
        person1 = Person.objects.create(first_name = "Antonio", second_name = "Jesus", last_name = "Granados", email = "antonio.granados@gmail.com")
        person2 = Person.objects.create(first_name="Miguel", second_name="Jorge", last_name="Suarez", email="miguel.suarez@gmail.com")

        self.user1 = User.objects.create_user(
            email = 'test1@test.com',
            password = 'test',
            person = person1,
            role = 2
        )

        self.admin = User.objects.create_superuser(
            email = 'admin@test.com',
            password = 'admin',
            person = person2,
        )

    def test_error_employee_trying_menu_creation(self):
        data = {'email': 'test1@test.com', 'password': 'test'}
        response = self.client.post("/authenticate", data)
        login_response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in login_response_data)
        token = login_response_data['access']

        data = {
            'name': 'Especial de navidad',
            'available_date': '2021-04-30',
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = client.post("/menu", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test__menu_creation(self):
        data = {'email': 'admin@test.com', 'password': 'admin'}
        response = self.client.post("/authenticate", data)
        login_response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in login_response_data)
        token = login_response_data['access']

        data = {
            'name': 'Especial de navidad',
            'available_date': date.today(),
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = client.post("/menu", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_all_menus(self):
        data = {'email': 'admin@test.com', 'password': 'admin'}
        response = self.client.post("/authenticate", data)
        login_response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in login_response_data)
        token = login_response_data['access']

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = client.get("/menu")
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class MenuOptionTest(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('', include('bonapetit.urls')),
    ]

    def setUp(self):
        person1 = Person.objects.create(first_name = "Antonio", second_name = "Jesus", last_name = "Granados", email = "antonio.granados@gmail.com")
        person2 = Person.objects.create(first_name="Miguel", second_name="Jorge", last_name="Suarez", email="miguel.suarez@gmail.com")

        self.user1 = User.objects.create_user(
            email = 'test1@test.com',
            password = 'test',
            person = person1,
            role = 2
        )

        self.admin = User.objects.create_superuser(
            email = 'admin@test.com',
            password = 'admin',
            person = person2,
        )

        menu = Menu(name = "Especial de navidad", available_date = "2021-04-30")
        Menu.objects.create(name = "Especial de navidad", available_date = "2021-04-30", uuid=uuid.uuid4())

    def test_error_employee_trying_menu_option_creation(self):
        data = {'email': 'test1@test.com', 'password': 'test'}
        response = self.client.post("/authenticate", data)
        login_response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in login_response_data)
        token = login_response_data['access']

        data = {
            'name': 'Sopa de Verdura',
            'ingredients': 'calabaza, zanahorita, etc',
            "menu": 1
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = client.post("/menuoption", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_all_menu_option(self):
        data = {'email': 'admin@test.com', 'password': 'admin'}
        response = self.client.post("/authenticate", data)
        login_response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in login_response_data)
        token = login_response_data['access']

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = client.get("/menuoption")
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)