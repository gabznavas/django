from django.test import TestCase
from django.urls import reverse


class RecipesURLsTest(TestCase):
    def test_recipe_home_url_is_correct(self):
        received = reverse('recipes:home')
        expected = '/'
        self.assertEqual(received, expected, 'path da home está errada!')

    def test_category_url_is_correct(self):
        received = reverse('recipes:category', args=(1,))
        expected = '/recipes/category/1/'
        self.assertEqual(received, expected, 'path da category está errada!')

    def test_recipe_url_is_correct(self):
        received = reverse('recipes:recipe', args=(1,))
        expected = '/recipes/1/'
        self.assertEqual(received, expected, 'path da recipe está errada!')
