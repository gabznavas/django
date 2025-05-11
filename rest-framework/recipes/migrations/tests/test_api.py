from django.urls import reverse
from .test_recipe_base import RecipeTestBase
from datetime import datetime
import json
from parameterized import parameterized

test_cases_out_range = [
    ("title", '', 'This field may not be blank.'),
    ("description", '', 'This field may not be blank.'),
    ("preparation_steps", '', 'This field may not be blank.'),
    ("preparation_time_unit", '', 'This field may not be blank.'),
    ("servings_unit", '', 'This field may not be blank.'),
    ("author_id", 0, 'Ensure this value is greater than or equal to 1.'),
    ("category_id", 0, 'Ensure this value is greater than or equal to 1.'),
    ("preparation_time", 0,
     'Ensure this value is greater than or equal to 1.'),
    ("servings", 0, 'Ensure this value is greater than or equal to 1.'),

    ("title", 'a'*101, 'Ensure this field has no more than 100 characters.'),
    ("description", 'a'*101,
     'Ensure this field has no more than 100 characters.'),
    ("preparation_steps",  'a'*501,
     'Ensure this field has no more than 500 characters.'),
    ("preparation_time_unit", 'a'*51,
     'Ensure this field has no more than 50 characters.'),
    ("servings_unit", 'a'*51,
     'Ensure this field has no more than 50 characters.'),
    ("author_id", 2_147_483_648,
     'Ensure this value is less than or equal to 2147483647.'),
    ("category_id", 2_147_483_648,
     'Ensure this value is less than or equal to 2147483647.'),

]

test_cases_none = [
    ("title", 'This field is required.'),
    ("description", 'This field is required.'),
    ("preparation_steps",  'This field is required.'),
    ("preparation_time_unit", 'This field is required.'),
    ("servings_unit", 'This field is required.'),
    ("author_id", 'This field is required.'),
    ("category_id", 'This field is required.'),
]


class TestListRecipes(RecipeTestBase):
    def setUp(self):
        self.url = 'recipe-list-create'

    def test_success(self):
        self.make_recipe()
        response = self.client.get(reverse(self.url))
        self.assertIsNotNone(response.data)
        self.assertEqual(response.data['page'], 0)
        self.assertEqual(response.data['page_size'], 10)
        self.assertEqual(response.data['total_pages'], 1)
        self.assertEqual(response.data['total_elements'], 1)
        self.assertEqual(response.data['total_pages'], 1)
        self.assertIsNotNone(response.data['data'])
        self.assertEqual(len(response.data['data']), 1)
        self.assertEqual(response.status_code, 200)

    def test_list_empty(self):
        response = self.client.get(reverse(self.url))
        self.assertIsNotNone(response.data)
        self.assertEqual(response.data['page'], 0)
        self.assertEqual(response.data['page_size'], 10)
        self.assertEqual(response.data['total_pages'], 0)
        self.assertEqual(response.data['total_elements'], 0)
        self.assertEqual(response.data['total_pages'], 0)
        self.assertIsNotNone(response.data['data'])
        self.assertEqual(len(response.data['data']), 0)
        self.assertEqual(response.status_code, 200)

    def test_page_size_is_bigger(self):
        url_with_params = f'{reverse(self.url)}?page=0&size=51'
        response = self.client.get(url_with_params)
        self.assertEqual(response.data, {'details': 'Invalid size length.'})
        self.assertEqual(response.status_code, 400)


class TestGetRecipe(RecipeTestBase):
    def test_success(self):
        recipe = self.make_recipe()
        url = reverse('recipe-get-update-delete',
                      kwargs={'recipe_id': recipe.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_recipe_not_found(self):
        url = reverse('recipe-get-update-delete',
                      kwargs={'recipe_id': 1})
        response = self.client.get(url)
        self.assertEqual(response.data, None)
        self.assertEqual(response.status_code, 404)


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

    @parameterized.expand(test_cases_out_range)
    def test_should_return_bad_request_when_field_is_out_range(self,
                                                               field,
                                                               value,
                                                               details
                                                               ):
        payload = self.make_valid_payload()
        payload[field] = value

        response = self.client.post(self.url, payload)

        self.assertEqual(
            response.json(),
            {field: [details]},
            f'falhou no field {field}, valus {value}, details {details}'
        )
        self.assertEqual(response.status_code, 400)

    @parameterized.expand(test_cases_none)
    def test_should_return_bad_request_when_field_is_none(self,
                                                          field,
                                                          details):
        payload = self.make_valid_payload()
        payload.pop(field)

        response = self.client.post(self.url, payload)

        self.assertEqual(
            response.json(),
            {field: [details]},
            f'falhou no field {field}, details {details}'
        )
        self.assertEqual(response.status_code, 400)


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
        url = reverse('recipe-get-update-delete',
                      kwargs={'recipe_id': recipe.id})
        response = self.client.put(
            url, data=json.dumps(payload), headers=self.headers)

        self.assertEqual(response.status_code, 204)
        self.assertIsNone(response.data)

    @parameterized.expand(test_cases_out_range)
    def test_should_return_bad_request_when_field_is_out_range(self,
                                                               field,
                                                               value,
                                                               details):
        recipe = self.make_recipe()
        payload = self.make_valid_payload()
        payload[field] = value

        url = reverse('recipe-get-update-delete',
                      kwargs={'recipe_id': recipe.id})
        response = self.client.put(
            url, data=json.dumps(payload), headers=self.headers)

        self.assertEqual(
            response.json(),
            {field: [details]},
            f'falhou no field {field}, valus {value} details {details}'
        )
        self.assertEqual(response.status_code, 400)

    @parameterized.expand(test_cases_none)
    def test_should_return_bad_request_when_field_is_none(self,
                                                          field,
                                                          details):
        recipe = self.make_recipe()
        payload = self.make_valid_payload()
        payload.pop(field)

        url = reverse('recipe-get-update-delete',
                      kwargs={'recipe_id': recipe.id})
        response = self.client.put(
            url, data=json.dumps(payload), headers=self.headers)

        self.assertEqual(
            response.json(),
            {field: [details]},
            f'falhou no field {field}, details {details}'
        )
        self.assertEqual(response.status_code, 400)


class TestDeleteRecipe(RecipeTestBase):
    def test_success(self):
        recipe = self.make_recipe()
        url = reverse('recipe-get-update-delete',
                      kwargs={'recipe_id': recipe.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertIsNone(response.data)

    def test_not_found(self):
        url = reverse('recipe-get-update-delete',
                      kwargs={'recipe_id': 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, {'details': 'recipe not found'})
