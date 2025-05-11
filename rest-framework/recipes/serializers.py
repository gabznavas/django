from rest_framework import serializers


class RecipeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=150)
    description = serializers.CharField(max_length=150)
