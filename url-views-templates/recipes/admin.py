from django.contrib import admin
from .models import Recipe, Category

# primeira forma de registrar
class CategoryAdmin(admin.ModelAdmin):
    ...
admin.site.register(Category, CategoryAdmin)

# segunda forma de registrar
@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    ...
