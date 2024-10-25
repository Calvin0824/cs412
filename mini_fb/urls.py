from django.urls import path
from . import views

urlpatterns = [
    path('', views.ShowAllProfileViews.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>/', views.ShowProfilePageView.as_view(), name='show_profile'),
    path('profile/create_profile/', views.CreateProfileView.as_view(), name='create_profile'),
    path('profile/<int:pk>/create_status/', views.CreateStatusView.as_view(), name='create_status'),
    path('profile/<int:pk>/update/', views.UpdateProfileView.as_view(), name='update_profile'),
    path('status/<int:pk>/delete/', views.DeleteStatusMessageView.as_view(), name='delete_status'),
    path('status/<int:pk>/update/', views.UpdateStatusMessageView.as_view(), name='update_status'),
    path('profile/<int:pk>/add_friend/<int:other_pk>', views.CreateFriendView.as_view(), name='create_friend'),
    path('profile/<int:pk>/friend_suggestions', views.ShowFriendSuggestionsView.as_view(), name='friend_suggestions'),
    path('profile/<int:pk>/news_feed', views.ShowNewsFeedView.as_view(), name='news_feed'),
]