from django.db import models

# Create your models here.
class Profile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    city = models.TextField(blank=False)
    email = models.EmailField()
    image = models.URLField(blank=True)