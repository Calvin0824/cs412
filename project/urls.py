# File: urls.py
# Author: Calvin Li (calvinli@bu.edu), 12/3/2024
# Description: This file contains all the urls for the project app

from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.RecipesListView.as_view(), name='recipes_list'),
    path('recipe/<int:pk>/', views.RecipesDetailView.as_view(), name='recipe_detail'),
    path('create/', views.CreateProfileView.as_view(), name='create_profile'),
    path('profile/', views.ProfileListView.as_view(), name='profile_list'),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile_detail'),
    path('recipe/create/', views.CreateRecipeView.as_view(), name='create_recipe'),
    path('login/', LoginView.as_view(template_name='project/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='project/logged_out.html'), name='logout'),
]