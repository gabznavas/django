from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpRequest, Http404

from .models import Recipe, Category

from utils.recipes.factory import make_recipe

def home(request: HttpRequest):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    return render(request, 'recipes/pages/home.html', context={
        "recipes": recipes
    })

def category(request: HttpRequest, category_id: int):
    recipes = Recipe.objects.filter(
        category__id=category_id
    ).order_by('-id')
    
    if len(recipes) == 0:
        raise Http404('Not found')

    return render(request, 'recipes/pages/category.html', context={
        "recipes": recipes,
        'title': f'{title} - Category',
    })


def recipes(request: HttpRequest, id: int):
    recipe = Recipe.objects.filter(id=id).first()
    if not recipe:
        raise 
    return render(request, 'recipes/pages/recipe.html', context={
        "recipe": recipe,
        "is_detail_page": True
    })
