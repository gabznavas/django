from rest_framework import serializers
from .models import Recipe


class RecipeSerializerRead(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        exclude = ['is_published']


class RecipeSerializerCreatePut(serializers.Serializer):
    title = serializers.CharField(max_length=65)
    description = serializers.CharField(max_length=165)
    preparation_time = serializers.IntegerField()
    preparation_time_unit = serializers.CharField(max_length=65)
    servings = serializers.IntegerField()
    servings_unit = serializers.CharField(max_length=65)
    preparation_steps = serializers.CharField(max_length=500)
    category_id = serializers.IntegerField()
    author_id = serializers.IntegerField()
