from recipes.models import Category, Recipe, User
from django.test import TestCase


class RecipeTestBase(TestCase):
    def make_category(self, name: str = 'category 1'):
        return Category.objects.create(name=name)

    def make_author(self,
                    username='test',
                    password=123,
                    email='test@test.com'):
        return User.objects.create(
            username=username, password=password, email=email
        )

    def make_recipe(self,
                    title='any title',
                    author_data=None,
                    category_data=None,
                    description='any description',
                    preparation_steps='1. any step 2. any step',
                    preparation_steps_is_html=False,
                    is_published=True,
                    preparation_time=50,
                    preparation_time_unit='Horas',
                    servings=20,
                    servings_unit='Pessoas',

                    ):
        author = {}
        if author_data is None:
            author = self.make_author()
        else:
            author = self.make_author(**author_data)

        category = {}
        if category_data is None:
            category = self.make_category()
        else:
            category = self.make_category(**category_data)

        return Recipe.objects.create(
            title=title,
            author=author,
            category=category,
            description=description,
            preparation_steps=preparation_steps,
            preparation_steps_is_html=preparation_steps_is_html,
            is_published=is_published,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
        )
