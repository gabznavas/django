from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpRequest, HttpResponseNotFound

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
    return render(request, 'recipes/pages/category.html', context={
        "recipes": recipes
    })


def recipes(request: HttpRequest, id: int):
    print(id)
    recipe = Recipe.objects.filter(id=id).first()
    if not recipe:
        return redirect(reverse('recipes:home'))
    return render(request, 'recipes/pages/recipe.html', context={
        "recipe": recipe,
        "is_detail_page": True
    })
