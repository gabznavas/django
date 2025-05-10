from django.urls import reverse, resolve
from recipes import views
from recipes.models import Recipe
from .test_recipe_base import RecipeTestBase


class RecipeViewsTest(RecipeTestBase):
    def tearDown(self):
        return super().tearDown()

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
        for recipe in Recipe.objects.all():
            recipe.delete()
        response = self.client.get(reverse('recipes:home'))
        received = response.content.decode('utf-8')
        expected = 'No recipes found here'
        self.assertIn(expected, received)

    def test_recipe_home_template_loads_recipes(self):

        response = self.client.get(reverse('recipes:home'))
        template_expected = 'recipes/pages/home.html'
        self.assertTemplateUsed(response, template_expected)

    def test_recipe_home_template_loads_recipes_context(self):
        response = self.client.get(reverse('recipes:home'))
        context_recipes = response.context['recipes']
        self.assertEqual(self.recipe.title, context_recipes[0].title)
        self.assertEqual(self.recipe.author.username,
                         context_recipes[0].author.username)
        self.assertEqual(self.recipe.category.name,
                         context_recipes[0].category.name)
        self.assertEqual(self.recipe.description,
                         context_recipes[0].description)
        self.assertEqual(self.recipe.preparation_steps,
                         context_recipes[0].preparation_steps)
        self.assertEqual(self.recipe.preparation_steps_is_html,
                         context_recipes[0].preparation_steps_is_html)
        self.assertEqual(self.recipe.is_published,
                         context_recipes[0].is_published)
        self.assertEqual(self.recipe.preparation_time,
                         context_recipes[0].preparation_time)
        self.assertEqual(self.recipe.preparation_time_unit,
                         context_recipes[0].preparation_time_unit)
        self.assertEqual(self.recipe.servings, context_recipes[0].servings)
        self.assertEqual(self.recipe.servings_unit,
                         context_recipes[0].servings_unit)

    def test_recipe_home_template_loads_recipes_content(self):
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        recipes = response.context['recipes']
        self.assertEqual(1, len(recipes))
        self.assertIn(self.recipe.title, content)
        self.assertIn(self.recipe.category.name, content,
                      'category name not found')
        self.assertIn(self.recipe.description,
                      content, 'description not found')
        self.assertIn(str(self.recipe.preparation_time), content,
                      'preparation_time not found')
        self.assertIn(self.recipe.preparation_time_unit, content,
                      'preparation_time_unit not found')
        self.assertIn(str(self.recipe.servings), content, 'servings not found')
        self.assertIn(self.recipe.servings_unit, content,
                      'servings_unit not found')

    def test_recipe_category_view_returns_status_404_if_no_recipes_found(self):
        response = self.client.get(reverse('recipes:category', kwargs={
            "category_id": 999,
        }))
        received = response.status_code
        expected = 404
        self.assertEqual(expected, received, f'código deveria ser {expected}')
