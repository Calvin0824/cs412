from django.db import models
from django.urls import reverse

# Create your models here.
class Profile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    city = models.TextField(blank=False)
    email = models.EmailField()
    image = models.URLField(blank=True)

    def get_status_messages(self):
        """Returns the status messages for this profile"""
        messages = StatusMessage.objects.filter(profile=self.profile)
        return messages
    
    def get_absolute_url(self):
        return reverse('show_profile', kwargs={'pk': self.pk})

class StatusMessage(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField(blank=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        '''Return the string representation of this status message.'''
        return f'{self.message}'