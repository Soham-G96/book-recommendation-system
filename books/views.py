from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Book, UserPreference
from .serializers import BookSerializer, UserPreferenceSerializer


# Create your views here.

class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
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

    def get_queryset(self):
        """Fetch books based on the user's preferred genres."""
        user_preferences, created = UserPreference.objects.get_or_create(user=self.request.user)

        #Get preferred genres
        preferred_genres = user_preferences.preferred_genres.split(',') if user_preferences.preferred_genres else []

        # Find books that match the user's preferred genres, excluding books they've already read
        recommended_books = Book.objects.filter(genre__in=preferred_genres).exclude(id__in=user_preferences.read_books.all())

        return recommended_books