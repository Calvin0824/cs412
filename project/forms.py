from django import forms
from django.contrib.auth.models import User
from .models import Recipe, RecipeIngredient, Image, Profile1

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description']

class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'quantity']

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['img']

class ProfileForm(forms.ModelForm):
    """Form to create a Profile1."""
    class Meta:
        model = Profile1
        fields = ['name']
