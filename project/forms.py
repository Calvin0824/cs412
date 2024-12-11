# File: forms.py
# Author: Calvin Li (calvinli@bu.edu), 12/3/2024
# Description: This file contains all the forms for the project app

from django import forms
from django.contrib.auth.models import User
from .models import Recipe, RecipeIngredient, Image, Profile1

class RecipeForm(forms.ModelForm):
    """Form to create a Recipe."""
    class Meta:
        model = Recipe
        fields = ['name', 'description']

class RecipeIngredientForm(forms.ModelForm):
    """Form to create a recipe and ingredient relation."""
    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'quantity']

class ImageForm(forms.ModelForm):
    """Form to create an Image."""
    class Meta:
        model = Image
        fields = ['img']

class ProfileForm(forms.ModelForm):
    """Form to create a Profile1."""
    class Meta:
        model = Profile1
        fields = ['name']
