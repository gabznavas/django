from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpRequest
from .models import Recipe
from django.db.models import Q


def home(request: HttpRequest):
    search = request.GET.get('search', '')
    print(search)
    recipes = Recipe.objects.filter(
        Q(is_published=True) & (
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(preparation_time_unit__icontains=search) |
            Q(servings_unit__icontains=search)
        )
    ).order_by('-id')
    return render(request, 'recipes/pages/home.html', context={
        "recipes": recipes
    })


def category(request: HttpRequest, category_id: int):
    query = Recipe.objects.filter(
        category__id=category_id,
        is_published=True
    ).order_by('-id')
    recipes = get_list_or_404(query)
    category = recipes[0].category
    return render(request, 'recipes/pages/category.html', context={
        "recipes": recipes,
        'title': f'{category.name} - Category',
    })


def recipes(request: HttpRequest, id: int):
    query = Recipe.objects.filter(id=id, is_published=True)
    recipe = get_object_or_404(query)
    return render(request, 'recipes/pages/recipe.html', context={
        "recipe": recipe,
        "is_detail_page": True
    })
