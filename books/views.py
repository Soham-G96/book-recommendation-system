from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from .models import Book, UserPreference, Review, Genre
from .serializers import BookSerializer, UserPreferenceSerializer, ReviewSerializer, GenreSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Avg
from django.shortcuts import get_object_or_404
# Create your views here.

class GenreListView(generics.ListAPIView):
    queryset = Genre.objects.all().order_by('name')
    serializer_class = GenreSerializer
class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    print("table name - ", Genre._meta.db_table)
    # print("queryset - ",queryset.values_list('pk','title'))
    serializer_class = BookSerializer 
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    print("queryset - ",(queryset.count()))
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

class UserPreferenceView(generics.RetrieveUpdateAPIView):
    serializer_class = UserPreferenceSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'user' # telling DRF NOT to use 'pk' (RetrieveUpdateAPIView)

    def get_object(self):
        """ Fetch user preferences based on the logged-in user, create if not found."""
        return UserPreference.objects.get_or_create(user=self.request.user)[0]


class BookRecommendationView(generics.ListAPIView):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    # Code to Implement the Genre Based Recommendation Logic 
    # def get_queryset(self):
    #     """Fetch books based on the user's preferred genres."""
    #     user_preferences, created = UserPreference.objects.get_or_create(user=self.request.user)

    #     #Get preferred genres
    #     preferred_genres = user_preferences.preferred_genres.split(',') if user_preferences.preferred_genres else []

    #     # Find books that match the user's preferred genres, excluding books they've already read
    #     recommended_books = Book.objects.filter(genre__in=preferred_genres).exclude(id__in=user_preferences.read_books.all())

    #     return recommended_books
    # def get_queryset(self):
    #     ''' Collaborative Filtering: Recommend books based on user ratings and similar users'''
    #     user = self.request.user

    #     #Step 1: Find books the user has rated highly (atleast above 3 stars)
    #     user_ratings = Rating.objects.filter(user=user, rating__gte=3).values_list('book', flat=True)
    #     print(user_ratings)
    #     #Step 2: Find users who rated those books highly
    #     similar_users = Rating.objects.filter(book__in=user_ratings, rating__gte=3).values_list('user', flat=True)
    #     print(similar_users)
    #     # Step 3: Find books that these similar users have rated highly
    #     recommended_books = Rating.objects.filter(user__in=similar_users, rating__gte=3 ).values_list('book', flat=True).distinct()
    #     print(Book.objects.filter(id__in=recommended_books).exclude(id__in=user_ratings))
    #     #Step 4: Return recommended books
    #     return Book.objects.filter(id__in=recommended_books).exclude(id__in=user_ratings)

    # NLP
    def get_queryset(self):
        user_pref, _ = UserPreference.objects.get_or_create(user = self.request.user)
        preferred_genres = user_pref.preferred_genres.split(',')

        recommended_books = Book.objects.filter(genre__in=preferred_genres)
        recommended_books = recommended_books.annotate(avg_sentiment=Avg('reviews__sentiment_score'))

        return recommended_books.order_by('-avg_sentiment', '-rating')
    
class ReviewView(generics.ListCreateAPIView):
    # Handles creating and listing reviews for books
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get all reviews for a specific book
        book_id = self.kwargs.get('book_id')
        return Review.objects.filter(book_id=book_id)
    
    def perform_create(self, serializer):
        # Ensure a user can only leave one review per book
        book_id = self.kwargs.get('book_id')
        book = get_object_or_404(Book, id=book_id)
        existing_review = Review.objects.filter(user=self.request.user, book=book)

        if existing_review.exists():
            raise ValidationError("You have already reviewed this book.")
        serializer.save(user=self.request.user, book=book)

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    # Allows users to update or delete their own review

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Ensure users can only modify their own reviews.

        book_id = self.kwargs.get('book_id')
        review = get_object_or_404(Review, book_id=book_id, user=self.request.user)
        return review