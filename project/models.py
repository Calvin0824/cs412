from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    def get_image(self):
        '''Returns the images for this recipe'''
        images = Image.objects.filter(recipe=self)
        return images
    
    def get_ingredients(self):
        """Returns all ingredients with quantities for this recipe."""
        return RecipeIngredient.objects.filter(recipe=self)

class Image(models.Model):
    img = models.ImageField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='images')

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=100)

    class Meta:
        unique_together = ('recipe', 'ingredient')

    def __str__(self):
        return f"{self.quantity} of {self.ingredient.name} for {self.recipe.name}"


class Profile1(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    uploaded_recipes = models.ManyToManyField(Recipe, related_name="uploaded_by", blank=True, null=True)
    completed_recipes = models.ManyToManyField(Recipe, related_name="completed_by", blank=True, null=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        '''Return the URL to display this profile'''
        # return reverse('recipe_list', kwargs={'pk': self.pk})
        return reverse('recipe_list')