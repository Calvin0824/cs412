from django.urls import path
from . import views

urlpatterns = [
    path('', views.ShowAllProfileViews.as_view(), name='show_all_profiles'),
]