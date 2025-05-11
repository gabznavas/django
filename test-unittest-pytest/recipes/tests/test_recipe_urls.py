from django.test import TestCase
from django.urls import reverse


class RecipesURLsTest(TestCase):
    def test_recipe_home_url_is_correct(self):
        received = reverse('recipes:home')
        expected = '/'
        self.assertEqual(expected, received, 'path da home está errada!')

    def test_category_url_is_correct(self):
        received = reverse('recipes:category', kwargs={'category_id': 1})
        expected = '/recipes/category/1/'
        self.assertEqual(expected, received, 'path da category está errada!')

    def test_recipe_detail_url_is_correct(self):
        received = reverse('recipes:recipe', kwargs={'id': 1})
        expected = '/recipes/1/'
        self.assertEqual(expected, received, 'path da recipe está errada!')

    def test_recipe_search_url_is_correct(self):
        received = reverse('recipes:search')
        expected = '/recipes/search/'
        self.assertEqual(expected, received, 'path da search está errada!')
