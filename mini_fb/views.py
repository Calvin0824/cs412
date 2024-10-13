from typing import Any
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView
from .models import Profile, StatusMessage
from django.urls import reverse
from .forms import StatusMessageForm

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        context['statuses'] = profile.statusmessage_set.all()
        
        return context

class CreateProfileView(CreateView):
    """Create a new profile"""
    model = Profile
    template_name = "mini_fb/create_profile_form.html"
    fields = ['first_name', 'last_name', 'city', 'email', 'image']

    def form_valid(self, form):
        """This is called if the form is valid."""
        form.save()
        return super().form_valid(form)
    
class CreateStatusView(CreateView):
    """Create a new status message"""
    model = StatusMessage
    template_name = "mini_fb/create_status_form.html"
    form_class = StatusMessageForm


    def form_valid(self, form):
        """This is called if the form is valid."""
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        form.instance.profile = profile
        return super().form_valid(form)
    
    def get_success_url(self):
        """Return the URL to redirect to after processing the form."""
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        context['profile'] = profile
        
        return context