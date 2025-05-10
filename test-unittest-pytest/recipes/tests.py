from django.test import TestCase
from django.urls import reverse, resolve
from . import views


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


class RecipeViewsTest(TestCase):
    def test_recipe_home_views_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(
            view.func,
            views.home,
            'home esta usando a view errada'
        )

    def test_recipe_category_views_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(
            view.func,
            views.category,
            'category esta usando a view errada'
        )

    def test_recipe_detail_views_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(
            view.func,
            views.recipes,
            'recipe esta usando a view errada'
        )
