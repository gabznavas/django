from django.urls import reverse
from .test_recipe_base import RecipeTestBase
from datetime import datetime
import json


class TestListRecipes(RecipeTestBase):
    def test_success(self):
        url = reverse('recipe-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestGetRecipe(RecipeTestBase):
    def test_success(self):
        recipe = self.make_recipe()
        url = reverse('recipe-detail-update-delete',
                      kwargs={'recipe_id': recipe.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestCreateRecipe(RecipeTestBase):
    def setUp(self):
        super().setUp()
        self.url = reverse('recipe-list-create')

    def make_valid_payload(self):
        return {
            'title': 'any title',
            'author_id': self.make_author().id,
            'category_id': self.make_category().id,
            'description': 'any description',
            'preparation_steps': 'any preparation_steps',
            'preparation_time': 10,
            'preparation_time_unit': 'minutes',
            'servings': 2,
            'servings_unit': 'people',
        }

    def test_success(self):
        payload = self.make_valid_payload()
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], payload['title'])
        self.assertEqual(response.data['author'], payload['author_id'])
        self.assertEqual(response.data['category'], payload['category_id'])
        self.assertEqual(response.data['description'], payload['description'])
        self.assertEqual(
            response.data['preparation_steps'], payload['preparation_steps'])
        self.assertEqual(
            response.data['preparation_time'], payload['preparation_time'])
        self.assertEqual(
            response.data[
                'preparation_time_unit'],
            payload['preparation_time_unit']
        )
        self.assertEqual(response.data['servings'], payload['servings'])
        self.assertEqual(
            response.data['servings_unit'], payload['servings_unit'])
        self.assertIsInstance(datetime.fromisoformat(
            response.data['created_at']), datetime)
        self.assertIsInstance(datetime.fromisoformat(
            response.data['updated_at']), datetime)


class TestUpdateRecipe(RecipeTestBase):
    def setUp(self):
        super().setUp()
        self.headers = {'Content-Type': 'application/json'}

    def make_valid_payload(self):
        return {
            'title': 'updated title',
            'author_id': self.make_author(username='updated_author').id,
            'category_id': self.make_category(name='updated_category').id,
            'description': 'updated description',
            'preparation_steps': 'updated preparation_steps',
            'preparation_time': 15,
            'preparation_time_unit': 'minutes',
            'servings': 4,
            'servings_unit': 'people',
        }

    def test_success(self):
        recipe = self.make_recipe()
        payload = self.make_valid_payload()
        url = reverse('recipe-detail-update-delete',
                      kwargs={'recipe_id': recipe.id})
        response = self.client.put(
            url, data=json.dumps(payload), headers=self.headers)

        self.assertEqual(response.status_code, 204)
        self.assertIsNone(response.data)


class TestDeleteRecipe(RecipeTestBase):
    def test_success(self):
        recipe = self.make_recipe()
        url = reverse('recipe-detail-update-delete',
                      kwargs={'recipe_id': recipe.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertIsNone(response.data)
