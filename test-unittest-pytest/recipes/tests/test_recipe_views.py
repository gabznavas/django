from django.test import TestCase
from django.urls import reverse, resolve
from recipes import views
from recipes.models import Category, Recipe, User


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

    def test_recipe_home_template_loads_recipes(self):
        category = Category.objects.create(name='category 1')
        user = User.objects.create(
            username='test', password=123, email='test@test.com'
        )
        Recipe.objects.create(
            title='any title',
            author=user,
            category=category,
            description='any description',
            preparation_steps=50,
            preparation_steps_is_html=False,
            is_published=True,
            preparation_time=50,
            preparation_time_unit='Horas',
            servings=20,
            servings_unit='Pessoas',
        )
        response = self.client.get(reverse('recipes:home'))
        template_expected = 'recipes/pages/home.html'
        self.assertTemplateUsed(response, template_expected)

    def test_recipe_home_template_loads_recipes_context(self):
        category = Category.objects.create(name='category 1')
        user = User.objects.create(
            username='test', password=123, email='test@test.com'
        )
        recipe = Recipe.objects.create(
            title='any title',
            author=user,
            category=category,
            description='any description',
            preparation_steps='1. any 2. any',
            preparation_steps_is_html=False,
            is_published=True,
            preparation_time=50,
            preparation_time_unit='Horas',
            servings=20,
            servings_unit='Pessoas',
        )
        response = self.client.get(reverse('recipes:home'))
        context_recipes = response.context['recipes']
        self.assertEqual(recipe.title, context_recipes[0].title)
        self.assertEqual(recipe.author.username,
                         context_recipes[0].author.username)
        self.assertEqual(recipe.category.name,
                         context_recipes[0].category.name)
        self.assertEqual(recipe.description, context_recipes[0].description)
        self.assertEqual(recipe.preparation_steps,
                         context_recipes[0].preparation_steps)
        self.assertEqual(recipe.preparation_steps_is_html,
                         context_recipes[0].preparation_steps_is_html)
        self.assertEqual(recipe.is_published, context_recipes[0].is_published)
        self.assertEqual(recipe.preparation_time,
                         context_recipes[0].preparation_time)
        self.assertEqual(recipe.preparation_time_unit,
                         context_recipes[0].preparation_time_unit)
        self.assertEqual(recipe.servings, context_recipes[0].servings)
        self.assertEqual(recipe.servings_unit,
                         context_recipes[0].servings_unit)

    def test_recipe_home_template_loads_recipes_context(self):
        category = Category.objects.create(name='category 1')
        user = User.objects.create(
            username='test', password=123, email='test@test.com'
        )
        recipe = Recipe.objects.create(
            title='any title',
            author=user,
            category=category,
            description='any description',
            preparation_steps='1. any 2. any',
            preparation_steps_is_html=False,
            is_published=True,
            preparation_time=50,
            preparation_time_unit='Horas',
            servings=20,
            servings_unit='Pessoas',
        )
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        self.assertIn(recipe.title, content)
        self.assertIn(recipe.category.name, content,
                      'category name not found')
        self.assertIn(recipe.description, content, 'description not found')
        self.assertIn(str(recipe.preparation_time), content,
                      'preparation_time not found')
        self.assertIn(recipe.preparation_time_unit, content,
                      'preparation_time_unit not found')
        self.assertIn(str(recipe.servings), content, 'servings not found')
        self.assertIn(recipe.servings_unit, content,
                      'servings_unit not found')

    def test_recipe_category_view_returns_status_404_if_no_recipes_found(self):
        response = self.client.get(reverse('recipes:category', kwargs={
            "category_id": 999,
        }))
        received = response.status_code
        expected = 404
        self.assertEqual(expected, received, f'código deveria ser {expected}')
