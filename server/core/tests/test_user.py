from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from .base import BaseViewTest


class UserAuthTests(BaseViewTest):

    def test_new_user_invalid_email(self):
        """
        Test creating user without email raises error
        """
        with self.assertRaises(ValueError) as msg:
            get_user_model().objects.create_user(None, 'pass1234')
        self.assertEqual(str(msg.exception),
                         'Customer must have an email address')

    def test_post_and_register_user(self):
        """
        Ensure that we can successfully create a user
        """
        data = {
            'firstname': 'test',
            'lastname': 'user',
            'email': 'user@test.com',
            'password': 'pass1234'
        }
        response = self.client.post(reverse('create_user'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['firstname'], 'test')

    def test_post_login_user(self):
        """
        Ensure that user are successfully logged in
        """
        data = {
            'email': 'admin@test.com',
            'password': 'pass1234'
        }
        response = self.client.post(reverse('login_user'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'],
                         'Welcome back, Login successfully')

    def test_post_login_invalid_user(self):
        """
        Ensure that user should not log in with wrong credentials
        """
        data = {
            'email': 'invalid@test.com',
            'password': 'password'
        }
        response = self.client.post(reverse('login_user'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Wrong email or password')
