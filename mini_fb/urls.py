from django.urls import path
from . import views

urlpatterns = [
    path(r'', views.ShowAllProfileViews.as_view(), name='show_all_profiles'),
    path(r'profile/<int:pk>/', views.ShowProfilePageView.as_view(), name='show_profile'),
    path(r'profile/create_profile/', views.CreateProfileView.as_view(), name='create_profile'),
    path(r'profile/<int:pk>/create_status/', views.CreateStatusView.as_view(), name='create_status'),
    path(r'profile/<int:pk>/update/', views.UpdateProfileView.as_view(), name='update_profile'),
]