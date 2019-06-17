from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from core.models import Category, CategoryUser


class BaseViewTest(APITestCase):

    def create_category(self, user='', name='', default=False):
        category = Category.objects.create(name=name, default=default)
        CategoryUser.objects.create(user=user, category=category)

    def setUp(self):
        # create a admin user
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@test.com',
            password='pass1234',
        )

        # create a user
        self.user = get_user_model().objects.create_user(
            email='test@test.com',
            password='pass1234'
        )

        # create a user
        self.user2 = get_user_model().objects.create_user(
            email='test2@test.com',
            password='pass1234'
        )

        # add test data
        self.create_category(self.admin_user, 'places', True)
        self.create_category(self.user, 'laptop')
        self.create_category(self.user2, 'phone')

    def login_client(self, email='', password=''):
        data = {
            'email': email,
            'password': password
        }
        response = self.client.post(reverse('login_user'), data)
        return response
