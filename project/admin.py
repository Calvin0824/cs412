from django.contrib import admin
from .models import Ingredient, Recipe, RecipeIngredient, Profile1, Image

# Register your models here.
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(RecipeIngredient)
admin.site.register(Profile1)
admin.site.register(Image)