from django.urls import path
from . import views

urlpatterns = [
    path('', views.RecipesList.as_view(), name='recipes_list'),
    path('recipe/<int:pk>/', views.RecipesDetail.as_view(), name='recipe_detail'),
]