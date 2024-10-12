from django import forms
from .models import Profile, StatusMessage

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email', 'image']