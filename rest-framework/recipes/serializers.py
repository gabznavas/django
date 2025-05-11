from rest_framework import serializers
from .models import Recipe


class RecipeSerializerRead(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        exclude = ['is_published']


class RecipeSerializerCreatePut(serializers.Serializer):
    title = serializers.CharField(
        required=True,
        allow_null=False,
        min_length=1,
        max_length=100
    )
    description = serializers.CharField(
        required=True,
        allow_null=False,
        min_length=1,
        max_length=100
    )
    preparation_time = serializers.IntegerField(
        required=True,
        allow_null=False,
        min_value=1,
        max_value=1000
    )
    preparation_time_unit = serializers.CharField(
        required=True,
        allow_null=False,
        min_length=1,
        max_length=50
    )
    servings = serializers.IntegerField(
        required=True,
        allow_null=False,
        min_value=1,
        max_value=1000
    )
    servings_unit = serializers.CharField(
        required=True,
        allow_null=False,
        min_length=1,
        max_length=50
    )
    preparation_steps = serializers.CharField(
        required=True,
        allow_null=False,
        min_length=1,
        max_length=500
    )
    category_id = serializers.IntegerField(
        required=True,
        allow_null=False,
        min_value=1,
        max_value=2_147_483_647
    )
    author_id = serializers.IntegerField(
        required=True,
        allow_null=False,
        min_value=1,
        max_value=2_147_483_647
    )
