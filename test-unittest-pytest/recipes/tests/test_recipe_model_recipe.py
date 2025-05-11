from .test_recipe_base import RecipeTestBase
from django.core.exceptions import ValidationError
from parameterized import parameterized
from recipes.models import Recipe


class RecipeModelTest(RecipeTestBase):

    def setUp(self):
        self.recipe = self.make_recipe()

    @parameterized.expand([
        ('title', 65),
        ('description', 165),
        ('preparation_time_unit', 65),
        ('servings_unit', 65),
    ])
    def test_recipe_fields_raise_validation_error_if_exceed_max_length(
        self,
        field,
        max_length
    ):
        """
            Testa se os campos textuais lançam ValidationError ao
            ultrapassar o tamanho máximo
        """
        more_length = 1
        value = 'A' * (max_length + more_length)
        setattr(self.recipe, field, value)

        with self.assertRaises(ValidationError) as context:
            self.recipe.full_clean()

        self.assertIn(field, context.exception.message_dict)

    def test_recipe_preparation_steps_is_html_is_false_by_default(self):
        recipe = self.make_recipe_no_default()
        self.assertFalse(
            recipe.preparation_steps_is_html,
            'Passos de preparação não está False'
        )
        self.assertFalse(
            recipe.is_published,
            'Publicação está ativa'
        )

    def make_recipe_no_default(self):
        recipe = Recipe(
            category=self.make_category(name='Test Default Category'),
            author=self.make_author(username='Test Default Category'),
            title='Recipe Title 2',
            description='Recipe Description',
            slug='recipe-slug',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=5,
            servings_unit='porções',
            preparation_steps='Recipe preparation steps',
        )
        recipe.full_clean()
        recipe.save()
        return recipe
