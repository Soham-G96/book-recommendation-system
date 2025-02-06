from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import models


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    description = models.TextField()
    rating = models.FloatField(default=0.0)
    cover_image = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
    
class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_genres = models.TextField() # To store genres as csv
    read_books = models.ManyToManyField(Book, related_name='read_by_users')

    def __str__(self):
        return f'{self.user.username} Preferences'