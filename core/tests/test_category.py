from django.urls import reverse
from rest_framework import status
from .base import BaseViewTest


class CategoryTest(BaseViewTest):

    def test_unauthenticated_user_category(self):
        """
        Ensure that an authenticated user can't create category
        """
        data = {'name': 'test'}
        response = self.client.post(reverse('create_list_category'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_create_category(self):
        """
        Ensure that an authenticated user can create category
        """
        self.login_client('test@test.com', 'pass1234')
        data = {'name': 'test'}
        response = self.client.post(reverse('create_list_category'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'test')
        self.assertEqual(response.data['default'], False)

    def test_admin_create_category(self):
        """
        Ensure that an admin can create default categories
        """
        self.login_client('admin@test.com', 'pass1234')
        data = {'name': 'people'}
        response = self.client.post(reverse('create_list_category'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'people')
        self.assertEqual(response.data['default'], True)

    def test_user_recreate_default(self):
        """
        Ensure user cant recreate a default category
        """
        self.login_client('test@test.com', 'pass1234')
        data = {'name': 'places'}
        response = self.client.post(reverse('create_list_category'), data)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_user_recreate_category(self):
        """
        Ensure user cant recreate a category
        """
        self.login_client('test@test.com', 'pass1234')
        data = {'name': 'laptop'}
        response = self.client.post(reverse('create_list_category'), data)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_user_adding_category(self):
        """
        Ensure user is added to existing category
        """
        self.login_client('test@test.com', 'pass1234')
        data = {'name': 'phone'}
        response = self.client.post(reverse('create_list_category'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Category added successfully')

    def test_get_user_category(self):
        """
        Ensure that users get default and created category
        """
        self.login_client('test@test.com', 'pass1234')
        response = self.client.get(reverse('create_list_category'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

