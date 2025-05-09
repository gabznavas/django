from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, Http404

from .models import Recipe

from utils.recipes.factory import make_recipe

def home(request: HttpRequest):
    recipes = Recipe.objects.filter(is_published=True)
    return render(request, 'recipes/pages/home.html', context={
        "recipes": recipes
    })

def recipes(request: HttpRequest, id: int):
    print(id)
    recipe = Recipe.objects.filter(id=id).first()
    if not recipe:
        return Http404()
    return render(request, 'recipes/pages/recipe.html', context={
        "recipe": recipe,
        "is_detail_page": True
    })
