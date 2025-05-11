from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from django.utils.text import slugify
from django.db.models import Q
from .models import Recipe, User, Category
from .serializers import RecipeSerializerRead, RecipeSerializerCreatePut
import math


class RecipeListCreateView(APIView):
    def post(self, request: Request):
        serializer = RecipeSerializerCreatePut(data=request.data)
        if not serializer.is_valid(raise_exception=False):
            return Response(serializer.errors, status=400)

        title = serializer.data['title']
        slug = slugify(serializer.data['title'])
        recipe = Recipe.objects.filter(Q(title=title) | Q(slug=slug)).first()
        if recipe is not None:
            return Response(
                {'details': 'already exists recipe with title'},
                status=400
            )

        author = User.objects.filter(
            id=serializer.data['author_id']).first()
        if author is None:
            return Response(
                {'details': 'Author not found'},
                status=404
            )

        category = Category.objects.filter(
            id=serializer.data['category_id']
        ).first()
        if category is None:
            return Response(
                {'details': 'category not found'},
                status=404
            )

        recipe = Recipe.objects.create(
            title=serializer.data['title'],
            description=serializer.data['description'],
            preparation_time=serializer.data['preparation_time'],
            preparation_time_unit=serializer.data['preparation_time_unit'],
            servings=serializer.data['servings'],
            servings_unit=serializer.data['servings_unit'],
            preparation_steps=serializer.data['preparation_steps'],
            slug=slug,
            category=category,
            author=author,
        )

        serializer = RecipeSerializerRead(recipe)
        data = serializer.data
        return Response(data, status=201)

    def get(self, request: Request):
        q = request.query_params.get('q', '').strip()
        try:
            page = max(int(request.query_params.get('page', 0)), 0)
            size = max(int(request.query_params.get('size', 10)), 1)
        except (ValueError, TypeError):
            return Response({'details': 'Invalid page or size.'}, status=400)

        if size > 50:
            return Response({'details': 'Invalid size length.'}, status=400)

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

        serializer = RecipeSerializerRead(recipes, many=True)
        return Response({
            'page': page,
            'size': size,
            'total': total,
            'pages': math.ceil(total / size),
            'data': serializer.data
        })


class RecipeGetPutDelete(APIView):
    def get(self, request: Request, recipe_id: int):
        recipe = Recipe.objects.filter(id=recipe_id, is_published=True).first()
        if recipe is None:
            return Response(None, status=404)
        serializer = RecipeSerializerRead(recipe)
        return Response(serializer.data)

    def put(self, request: Request, recipe_id: int):
        serializer = RecipeSerializerCreatePut(data=request.data)
        if not serializer.is_valid(raise_exception=False):
            return Response(serializer.errors, status=400)

        title = serializer.data['title']
        slug = slugify(serializer.data['title'])
        recipe = Recipe.objects.filter(Q(title=title) | Q(slug=slug)).first()
        if recipe is not None and recipe.id != recipe_id:
            return Response(
                {'details': 'already exists recipe with title'},
                status=400
            )

        author = User.objects.filter(
            id=serializer.data['author_id']).first()
        if author is None:
            return Response(
                {'details': 'Author not found'},
                status=404
            )

        category = Category.objects.filter(
            id=serializer.data['category_id']
        ).first()
        if category is None:
            return Response(
                {'details': 'category not found'},
                status=404
            )

        recipe = Recipe.objects.filter(id=recipe_id, is_published=True).first()

        recipe.title = serializer.data['title']
        recipe.description = serializer.data['description']
        recipe.preparation_time = serializer.data['preparation_time']
        recipe.preparation_time_unit = serializer.data['preparation_time_unit']
        recipe.servings = serializer.data['servings']
        recipe.servings_unit = serializer.data['servings_unit']
        recipe.preparation_steps = serializer.data['preparation_steps']
        recipe.slug = slug
        recipe.category = category
        recipe.author = author
        recipe.save()

        return Response(None, status=204)

    def delete(self, request: Request, recipe_id: int):
        recipe = Recipe.objects.filter(id=recipe_id, is_published=True).first()
        if recipe is None:
            return Response({'details': 'recipe not found'}, status=404)
        recipe.delete()
        return Response(None, status=204)
