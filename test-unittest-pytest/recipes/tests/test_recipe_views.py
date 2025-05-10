from django.test import TestCase
from django.urls import reverse


class RecipesURLsTest(TestCase):
    def test_recipe_home_url_is_correct(self):
        received = reverse('recipes:home')
        expected = '/'
        self.assertEqual(received, expected, 'path da home está errada!')

    def test_category_url_is_correct(self):
        received = reverse('recipes:category', kwargs={'category_id': 1})
        expected = '/recipes/category/1/'
        self.assertEqual(received, expected, 'path da category está errada!')

    def test_recipe_detail_url_is_correct(self):
        received = reverse('recipes:recipe', kwargs={'id': 1})
        expected = '/recipes/1/'
        self.assertEqual(received, expected, 'path da recipe está errada!')

    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))
        received = response.status_code
        expected = 200
        self.assertEqual(received, expected, f'código deveria ser {expected}')

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        template_expected = 'recipes/pages/home.html'
        self.assertTemplateUsed(response, template_expected)
