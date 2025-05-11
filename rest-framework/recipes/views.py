from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from django.db.models import Q
from .models import Recipe
from .serializers import RecipeSerializer
import math


@api_view(['GET'])
def recipe_list(request: Request):
    q = request.query_params.get('q', '').strip()
    try:
        page = max(int(request.query_params.get('page', 0)), 0)
        size = max(int(request.query_params.get('size', 10)), 1)
    except (ValueError, TypeError):
        return Response({'detail': 'Invalid page or size.'}, status=400)

    if size > 50:
        return Response({'detail': 'Invalid size length.'}, status=400)

    queryset = Recipe.objects.filter(is_published=True)

    if q:
        queryset = queryset.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(preparation_time_unit__icontains=q) |
            Q(servings_unit__icontains=q)
        )

    total = queryset.count()
    start = page * size
    end = start + size
    recipes = queryset[start:end]

    serializer = RecipeSerializer(recipes, many=True)
    return Response({
        'page': page,
        'size': size,
        'total': total,
        'pages': math.ceil(total / size),
        'data': serializer.data
    })


@api_view(['GET'])
def recipe_detail(request: Request, id: int):
    recipe = Recipe.objects.filter(id=id, is_published=True).first()
    if recipe is None:
        return Response(None, status=404)

    serializer = RecipeSerializer(recipe)
    return Response(serializer.data)
