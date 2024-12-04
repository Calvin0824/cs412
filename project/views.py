from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from .models import Recipe, RecipeIngredient, Image, Ingredient, Profile1
from .forms import RecipeForm, RecipeIngredientForm, ImageForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
class RecipesListView(ListView):
    model = Recipe
    template_name = 'project/recipes_list.html'
    context_object_name = 'recipes'
    
class RecipesDetailView(DetailView):
    model = Recipe
    template_name = 'project/recipe_detail.html'
    context_object_name = 'recipe'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        return context
    
class CreateRecipeView(LoginRequiredMixin,CreateView):
    """Create a new recipe."""
    model = Recipe
    template_name = "project/create_recipe_form.html"
    form_class = RecipeForm

    def get_object(self):
        """Returns the Profile1 object for the current user."""
        return Profile1.objects.get(user=self.request.user)

    def form_valid(self, form):
        """This is called if the form is valid."""
        profile = self.get_object()
        # Save the recipe first to ensure it gets an ID
        recipe = form.save()

        # Associate the recipe with the user's profile
        profile.uploaded_recipes.add(recipe)  # Associate the recipe with the user's profile.

        # Handle ingredients
        ingredients_data = self.request.POST.getlist('ingredient')
        quantities_data = self.request.POST.getlist('quantity')
        for ingredient_name, quantity in zip(ingredients_data, quantities_data):
            if ingredient_name.strip():
                ingredient, _ = Ingredient.objects.get_or_create(name=ingredient_name.strip())
                RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient, quantity=quantity)

        # Handle images
        files = self.request.FILES.getlist('images')
        for f in files:
            Image.objects.create(img=f, recipe=recipe)

        return super().form_valid(form)

    def get_success_url(self):
        """Return the URL to redirect to after processing the form."""
        return reverse('recipe_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        """Provide context for the template."""
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['profile'] = profile
        return context

    
class CreateProfileView(CreateView):
    """Create a new profile"""
    model = Profile1
    template_name = "project/create_profile_form.html"
    fields = ['name']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_creation_form'] = UserCreationForm()
        return context

    def form_valid(self, form):
        """This is called if the form is valid."""
        user_creation_form = UserCreationForm(self.request.POST)
        if user_creation_form.is_valid():
            user = user_creation_form.save()
            profile = form.instance
            profile.user = user
            profile.save()
            return super().form_valid(form)
        else:
            print(user_creation_form.errors)
            return self.form_invalid(form)
        
class ProfileView(DetailView):
    """Display a profile."""
    model = Profile1
    template_name = "project/profile.html"
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['uploaded'] = Recipe.objects.filter(uploaded_by=profile)
        context['completed'] = Recipe.objects.filter(completed_by=profile)
        return context
    
class ProfileListView(ListView):
    """Display a list of profiles."""
    model = Profile1
    template_name = "project/profile_list.html"
    context_object_name = 'profiles'