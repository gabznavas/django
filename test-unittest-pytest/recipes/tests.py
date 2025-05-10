from django.test import TestCase
from django.urls import reverse


class RecipesURLsTest(TestCase):
    def test_recipe_home_url_is_correct(self):
        received = reverse('recipes:home')
        expected = '/'
        self.assertEqual(received, expected, 'path da home está errada!')
