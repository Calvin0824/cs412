from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView
from .models import Profile

class ShowAllProfileViews(ListView):
    """Shows all the profiles"""
    model = Profile
    template_name = "mini_fb/show_all_profiles.html"
    context_object_name = "profiles"

class ShowProfilePageView(DetailView):
    """Shows the profile page"""
    model = Profile
    template_name = "mini_fb/show_profile.html"
    context_object_name = "profile"

class CreateView(CreateView):
    """Create a new profile"""
    model = Profile
    template_name = "mini_fb/create_profile_form.html"
    fields = ['first_name', 'last_name', 'city', 'email', 'image']

    def form_valid(self, form):
        """This is called if the form is valid."""
        form.save()
        return super().form_valid(form)