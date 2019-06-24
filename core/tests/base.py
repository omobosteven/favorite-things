from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from core.models import Category, CategoryUser, FavoriteThing


class BaseViewTest(APITestCase):

    @staticmethod
    def create_category(user='', name='', default=False):
        category = Category.objects.create(name=name, default=default)
        CategoryUser.objects.create(user=user, category=category)
        return category

    @staticmethod
    def create_favorite_things(**kwargs):
        favorite_thing = FavoriteThing.objects.create(**kwargs)
        return favorite_thing

    def login_client(self, email='', password=''):
        data = {
            'email': email,
            'password': password
        }
        response = self.client.post(reverse('login_user'), data)
        return response

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

        # add category test data
        self.default_category_places = self.create_category(self.admin_user, 'places', True)
        self.default_category_food = self.create_category(self.admin_user, 'food', True)
        self.category_laptop = self.create_category(self.user, 'laptop')
        self.category_phone = self.create_category(self.user2, 'phone')

        # add favorite_thing test data
        self.user1_favorite_1 = self.create_favorite_things(
            title='rice', ranking=1, category=self.default_category_food, user=self.user)
        self.user1_favorite_2 = self.create_favorite_things(
            title='beans', ranking=2, category=self.default_category_food, user=self.user)
        self.user1_favorite_3 = self.create_favorite_things(
            title='bread', ranking=3, category=self.default_category_food, user=self.user)
        self.user1_favorite_4 = self.create_favorite_things(
            title='macbook_pro', ranking=1, category=self.category_laptop, user=self.user)
        self.user1_favorite_5 = self.create_favorite_things(
            title='hp_elite', ranking=2, category=self.category_laptop, user=self.user)
        self.user2_favorite_1 = self.create_favorite_things(
            title='samsung_a30', ranking=1, category=self.category_phone, user=self.user2)
        self.user2_favorite_2 = self.create_favorite_things(
            title='samsung_a80', ranking=2, category=self.category_phone, user=self.user2)
