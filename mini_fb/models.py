from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    city = models.TextField(blank=False)
    email = models.EmailField()
    image = models.URLField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_status_messages(self):
        '''Returns the status messages for this profile'''
        messages = StatusMessage.objects.filter(profile=self.profile)
        return messages
    
    def get_absolute_url(self):
        '''Return the URL to display this profile'''
        return reverse('show_profile', kwargs={'pk': self.pk})
    
    def get_friends(self):
        '''Returns the friends of this profile'''
        friends1 = Friend.objects.filter(profile1=self).values_list('profile2', flat=True)
        friends2 = Friend.objects.filter(profile2=self).values_list('profile1', flat=True)

        ids = list(friends1) + list(friends2)
        profiles = Profile.objects.filter(id__in=ids)
        return list(profiles)
    
    def add_friend(self, other):
        '''Add a friend to this profile'''
        if self != other:
            if other not in self.get_friends():
                Friend.objects.create(profile1=self, profile2=other)

    def get_friend_suggestions(self):
        '''Returns friend suggestions for this profile'''
        friends = self.get_friends()
        friends.append(self)
        suggestions = Profile.objects.exclude(id__in=[f.id for f in friends])
        return suggestions
    
    def get_news_feed(self):
        '''Returns the news feed for this profile'''
        friends = self.get_friends()
        friends.append(self)
        messages = StatusMessage.objects.filter(profile__in=friends).order_by('-timestamp')
        return list(messages)

class StatusMessage(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField(blank=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        '''Return the string representation of this status message.'''
        return f'{self.message}'
    
    def get_images(self):
        '''Returns the images for this status message'''
        images = Image.objects.filter(message=self)
        return images
    
class Image(models.Model):
    img = models.ImageField()
    message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE, related_name='images')
    uploaded = models.DateTimeField(auto_now_add=True)


class Friend(models.Model):
    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile1')
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile2')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''Return the string representation of this friend relation.'''
        return f'{self.profile1} & {self.profile2}'