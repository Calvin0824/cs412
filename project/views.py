from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Recipe

# Create your views here.
class RecipesList(ListView):
    model = Recipe
    template_name = 'project/recipes_list.html'
    context_object_name = 'recipes'
    
class RecipesDetail(DetailView):
    model = Recipe
    template_name = 'project/recipe_detail.html'
    context_object_name = 'recipe'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        
        return context