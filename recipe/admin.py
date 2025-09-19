from django.contrib import admin
from .models import Ingredient, Recipe

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id','name')

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id','name')
