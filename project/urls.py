from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.RecipesList.as_view(), name='recipes_list'),
    path('recipe/<int:pk>/', views.RecipesDetail.as_view(), name='recipe_detail'),
    path('create/', views.CreateProfileView.as_view(), name='create_profile'),
    path('login/', LoginView.as_view(template_name='project/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='project/logged_out.html'), name='logout'),
]