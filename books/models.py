from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import models
from textblob import TextBlob
from django.db.models import Avg
from nltk.sentiment import SentimentIntensityAnalyzer

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    description = models.TextField()
    rating = models.FloatField(default=0.0)
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)

    def update_rating(self):
        avg_rating = self.reviews.aggregate(avg_rating=Avg('sentiment_score'))['avg_rating']
        self.rating = avg_rating if avg_rating is not None else 0.0
        self.save()

    def __str__(self):
        return self.title
    
class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_genres = models.TextField() # To store genres as csv
    read_books = models.ManyToManyField(Book, blank=True, related_name='read_by_users')

    def __str__(self):
        return f'{self.user.username} Preferences'

#Rating Model - Book recommendation based on Collaborative Filtering    
# class Rating(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="book_rating")
#     rating = models.IntegerField(default=0) # Ratings from 1 to 5

#     def __str__(self):
#         return f"{self.user.username} rated {self.book.title} as {self.rating}/5"
    

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField(choices = [(i,i) for i in range(1,6)]) 
    review_text = models.TextField()
    sentiment_score = models.FloatField(default=0.0) 

    def save(self, *args, **kwargs):
        '''Automatically analyze sentiment when saving a review'''
        # If we are using TextBlob to calculate sentiments -
        # self.sentiment_score = TextBlob(self.review_text).sentiment.polarity
        sia = SentimentIntensityAnalyzer()
        self.sentiment_score = sia.polarity_scores(self.review_text)['compound']
        super().save(*args, **kwargs)
        self.book.update_rating() 

    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.rating} Stars)"