from django.test import TestCase
from django.urls import reverse, resolve
from recipes import views


class RecipeViewsTest(TestCase):
    def test_recipe_home_views_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(
            views.home,
            view.func,
            'home esta usando a view errada'
        )

    def test_recipe_category_views_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(
            views.category,
            view.func,
            'category esta usando a view errada'
        )

    def test_recipe_detail_views_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(
            views.recipes,
            view.func,
            'recipe esta usando a view errada'
        )

    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))
        received = response.status_code
        expected = 200
        self.assertEqual(expected, received, f'código deveria ser {expected}')

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        template_expected = 'recipes/pages/home.html'
        self.assertTemplateUsed(response, template_expected)

    def test_recipe_home_template_shows_no_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        received = response.content.decode('utf-8')
        expected = 'No recipes found here'
        self.assertIn(expected, received)

    def test_recipe_category_view_returns_status_404_if_no_recipes_found(self):
        response = self.client.get(reverse('recipes:category', kwargs={
            "category_id": 999,
        }))
        received = response.status_code
        expected = 404
        self.assertEqual(expected, received, f'código deveria ser {expected}')
