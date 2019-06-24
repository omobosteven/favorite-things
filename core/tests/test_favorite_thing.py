from django.urls import reverse
from rest_framework import status
from .base import BaseViewTest
from rest_framework import serializers


class FavoriteThingTest(BaseViewTest):

    def test_unauthenticated_user_category(self):
        """
        Ensure that an authenticated user can't create favorite thing
        """
        data = {'title': 'test', 'ranking': 1, 'category': 1}
        response = self.client.post(reverse('favorite-thing'), data)
        print(response)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_favorite_thing_category_user(self):
        """
        Ensure that category is associated with or belongs to user
        """
        self.login_client('test@test.com', 'pass1234')

        data = {'title': 'test', 'ranking': 1, 'category': self.category_phone.pk}
        response = self.client.post(reverse('favorite-thing'), data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['category'], 'Category unavailable - object not found')

    def test_favorite_thing_invalid_metadata(self):
        """
        Ensure that users enters valid JSON type for metadata
        """
        self.login_client('test@test.com', 'pass1234')

        data = {'title': 'chicken', 'metadata': 'beans',
                'ranking': 4, 'category': self.default_category_food.pk}
        response = self.client.post(reverse('favorite-thing'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRaises(serializers.ValidationError)

    def test_favorite_thing_first_ranking(self):
        """
        Ensures that ranking is ordered when creating first favorite thing
        """
        self.login_client('test@test.com', 'pass1234')
        data = {'title': 'web', 'ranking': 400, 'category': self.default_category_places.pk}
        response = self.client.post(reverse('favorite-thing'), data)
        self.assertEqual(response.data['ranking'], 1)

    def test_user_create_favorite_thing(self):
        """
        Ensure that user can create favorite things
        """
        self.login_client('test@test.com', 'pass1234')

        data = {'title': 'chicken', 'metadata': {'type': 'roasted'},
                'ranking': 4, 'category': self.default_category_food.pk}
        response = self.client.post(reverse('favorite-thing'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'chicken')
        self.assertEqual(response.data['ranking'], 4)

    def test_favorite_thing_last_ranking(self):
        """
        Ensures that ranking is ordered when creating new favorite thing
        """
        self.login_client('test@test.com', 'pass1234')
        data = {'title': 'chicken', 'metadata': {'type': 'roasted'},
                'ranking': 400, 'category': self.default_category_food.pk}
        response = self.client.post(reverse('favorite-thing'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['ranking'], 4)

    def test_favorite_thing_duplicate(self):
        """
        Ensure that duplicate favorite thing are not created
        """
        self.login_client('test@test.com', 'pass1234')
        data = {'title': 'bread', 'ranking': 2, 'category': self.default_category_food.pk}
        response = self.client.post(reverse('favorite-thing'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRaises(serializers.ValidationError)

    def test_favorite_thing_ranking_reordering(self):
        """
        Ensures that ranking is re_ordered when creating new favorite thing with existing ranking
        """
        self.login_client('test@test.com', 'pass1234')
        data = {'title': 'chicken', 'metadata': {'type': 'roasted'},
                'ranking': 2, 'category': self.default_category_food.pk}
        response = self.client.post(reverse('favorite-thing'), data)
        response_list = self.client.get(reverse('favorite-things-category',
                                                None, {self.default_category_food.pk}))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_list.data[0]['ranking'], 1)
        self.assertEqual(response.data['ranking'], 2)
        self.assertEqual(response_list.data[1]['title'], 'chicken')
        self.assertEqual(response_list.data[-2]['ranking'], 3)
        self.assertEqual(response_list.data[-1]['ranking'], 4)

    def test_list_user_favorite_things_category(self):
        """
        Ensure that user get a list of favorite things in a category
        """
        self.login_client('test@test.com', 'pass1234')
        response = self.client.get(reverse('favorite-things-category', None, {self.default_category_food.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_list_user_favorite_things(self):
        """
        Ensure that user get a list of the favorite things
        """
        self.login_client('test@test.com', 'pass1234')
        response = self.client.get(reverse('favorite-thing'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_detail_favorite_things(self):
        """
        Ensure that use can view a favorite thing detail
        """
        self.login_client('test@test.com', 'pass1234')
        response = self.client.get(reverse('favorite-thing-detail', None, {self.user1_favorite_1.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'rice')

    def test_detail_favorite_things_not_user(self):
        """
        Ensure user cannot view detail of another users favorite things
        """
        self.login_client('test@test.com', 'pass1234')
        response = self.client.get(reverse('favorite-thing-detail', None, {self.user2_favorite_1.pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Not found.')

    def test_favorite_things_update(self):
        """
        Ensure user can update a favorite thing
        """
        self.login_client('test@test.com', 'pass1234')
        data = {'title': 'chicken', 'ranking': 1, 'category': self.default_category_food.pk}
        response = self.client.put(
            reverse('favorite-thing-detail', None, {self.user1_favorite_1.pk}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'chicken')

    def test_favorite_things_update_not_user(self):
        """
        Ensure user cannot update a favorite thing not created
        """
        self.login_client('test@test.com', 'pass1234')
        data = {'title': 'chicken', 'ranking': 1, 'category': self.default_category_food.pk}
        response = self.client.put(
            reverse('favorite-thing-detail', None, {self.user2_favorite_1.pk}), data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Not found.')

    def test_favorite_things_update_category_not_user(self):
        """
        Ensure user cannot update a favorite thing to a category not created
        """
        self.login_client('test@test.com', 'pass1234')
        data = {'title': 'chicken', 'ranking': 1, 'category': self.category_phone .pk}
        response = self.client.put(
            reverse('favorite-thing-detail', None, {self.user1_favorite_1.pk}), data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Category unavailable - object not found')

    def test_favorite_things_update_reorder_ranking(self):
        """
        Ensure ranking is reordered when ranking is updated with a ranking greater than instance
        """
        self.login_client('test@test.com', 'pass1234')
        data = {'ranking': 2}
        response = self.client.patch(
            reverse('favorite-thing-detail', None, {self.user1_favorite_1.pk}), data)
        response_list = self.client.get(reverse('favorite-things-category',
                                                None, {self.default_category_food.pk}))
        print(response_list.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['ranking'], 2)
        self.assertEqual(response_list.data[1]['title'], self.user1_favorite_1.title)
        self.assertEqual(response_list.data[-1]['ranking'], 3)
        self.assertEqual(response_list.data[0]['ranking'], 1)

    def test_favorite_things_update_reorder_ranking_less(self):
        """
        Ensure ranking is reordered when ranking is updated with a ranking less than instance
        """
        self.login_client('test@test.com', 'pass1234')
        data = {'ranking': 1}
        response = self.client.patch(
            reverse('favorite-thing-detail', None, {self.user1_favorite_3.pk}), data)
        response_list = self.client.get(reverse('favorite-things-category',
                                                None, {self.default_category_food.pk}))
        self.assertEqual(response.data['ranking'], 1)
        self.assertEqual(response_list.data[0]['title'], self.user1_favorite_3.title)

    def test_favorite_things_update_reorder_ranking_sequence(self):
        """
        Ensure ranking is reordered sequentially when ranking is updated
        with a ranking greater than last instance
        """
        self.login_client('test@test.com', 'pass1234')
        data = {'ranking': 10}
        response = self.client.patch(
            reverse('favorite-thing-detail', None, {self.user1_favorite_2.pk}), data)
        response_list = self.client.get(reverse('favorite-things-category',
                                                None, {self.default_category_food.pk}))
        self.assertEqual(response.data['ranking'], 3)
        self.assertEqual(response_list.data[-1]['ranking'], 3)

    def test_favorite_things_update_duplicate(self):
        """
        Ensure that duplicate favorite thing are not created
        """
        self.login_client('test@test.com', 'pass1234')
        data = {'title': 'beans', 'ranking': 2}
        response = self.client.patch(
            reverse('favorite-thing-detail', None, {self.user1_favorite_1.pk}), data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRaises(serializers.ValidationError)

    def test_favorite_things_delete(self):
        """
        Ensure that favorite thing is deleted and reordered
        """
        self.login_client('test@test.com', 'pass1234')
        response = self.client.delete(reverse('favorite-thing-detail', None, {self.user1_favorite_2.pk}))
        response_list = self.client.get(reverse('favorite-things-category',
                                                None, {self.default_category_food.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response_list.data[-1]['ranking'], 2)
