from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Profile, StatusMessage, Image
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
        context['friends'] = profile.get_friends()
        
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
    
class CreateStatusView(LoginRequiredMixin,CreateView):
    """Create a new status message"""
    model = StatusMessage
    template_name = "mini_fb/create_status_form.html"
    form_class = StatusMessageForm


    def form_valid(self, form):
        """This is called if the form is valid."""
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        form.instance.profile = profile
        sm = form.save()
        files = self.request.FILES.getlist('files')
        for f in files:
            img = Image(img=f, message=sm)
            img.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        """Return the URL to redirect to after processing the form."""
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        context['profile'] = profile
        
        return context
    
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """Update a profile"""
    model = Profile
    template_name = "mini_fb/update_profile_form.html"
    fields = ['city', 'email', 'image']

    def get_success_url(self):
        """Return the URL to redirect to after processing the form."""
        return reverse('show_profile', kwargs={'pk': self.object.pk})

class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    """Delete a status message"""
    model = StatusMessage
    template_name = "mini_fb/delete_status_form.html"

    def get_success_url(self):
        """Return the URL to redirect to after processing the form."""
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})

    def get_context_data(self, **kwargs):
        """Add profile to the context to use in the template"""
        context = super().get_context_data(**kwargs)
        context['profile'] = self.object.profile 
        return context
    
class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    """Update a status message"""
    model = StatusMessage
    template_name = "mini_fb/update_status_form.html"
    fields = ['message']

    def get_success_url(self):
        """Return the URL to redirect to after processing the form."""
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})

    def get_context_data(self, **kwargs):
        """Add profile to the context to use in the template"""
        context = super().get_context_data(**kwargs)
        context['profile'] = self.object.profile 
        return context

class CreateFriendView(LoginRequiredMixin, View):
    
    def dispatch(self, request, *args, **kwargs):
        profile = Profile.objects.get(pk=kwargs['pk'])
        friend = Profile.objects.get(pk=kwargs['other_pk'])
        profile.add_friend(friend)
        return redirect('show_profile', pk=profile.pk)
    
class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "mini_fb/friend_suggestions.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        context['friends'] = profile.get_friend_suggestions()
        context['profile'] = profile
        return context
    
class ShowNewsFeedView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "mini_fb/news_feed.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        statuses = profile.get_news_feed()
        context['statuses'] = statuses
        context['profile'] = profile
        return context