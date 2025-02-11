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
    read_books = models.ManyToManyField(Book, blank=True, related_name='read_by_users')

    def __str__(self):
        return f'{self.user.username} Preferences'
    
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="book_rating")
    rating = models.IntegerField(default=0) # Ratings from 1 to 5

    def __str__(self):
        return f"{self.user.username} rated {self.book.title} as {self.rating}/5"