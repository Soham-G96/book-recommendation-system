from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from .models import Book, UserPreference, Rating
from .serializers import BookSerializer, UserPreferenceSerializer
from rest_framework.response import Response
from rest_framework.views import APIView


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

    # Code to Implement the Genre Based Recommendation Logic 
    # def get_queryset(self):
    #     """Fetch books based on the user's preferred genres."""
    #     user_preferences, created = UserPreference.objects.get_or_create(user=self.request.user)

    #     #Get preferred genres
    #     preferred_genres = user_preferences.preferred_genres.split(',') if user_preferences.preferred_genres else []

    #     # Find books that match the user's preferred genres, excluding books they've already read
    #     recommended_books = Book.objects.filter(genre__in=preferred_genres).exclude(id__in=user_preferences.read_books.all())

    #     return recommended_books
    def get_queryset(self):
        ''' Collaborative Filtering: Recommend books based on user ratings and similar users'''
        user = self.request.user

        #Step 1: Find books the user has rated highly (atleast above 3 stars)
        user_ratings = Rating.objects.filter(user=user, rating__gte=3).values_list('book', flat=True)
        print(user_ratings)
        #Step 2: Find users who rated those books highly
        similar_users = Rating.objects.filter(book__in=user_ratings, rating__gte=3).values_list('user', flat=True)
        print(similar_users)
        # Step 3: Find books that these similar users have rated highly
        recommended_books = Rating.objects.filter(user__in=similar_users, rating__gte=3 ).values_list('book', flat=True).distinct()
        print(Book.objects.filter(id__in=recommended_books).exclude(id__in=user_ratings))
        #Step 4: Return recommended books
        return Book.objects.filter(id__in=recommended_books).exclude(id__in=user_ratings)
    

class RateBookView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, book_id):
        ''' Allows user to rate book.'''
        book = Book.objects.get(id=book_id)
        rating_value = request.data.get('rating')

        if not (1 <= int(rating_value) <=5):
            return Response({"error": "Rating should be between 1 and 5."}, status=status.HTTP_400_BAD_REQUEST)
        
        rating, created = Rating.objects.update_or_create(user=request.user, book=book, defaults={'rating': rating_value})
        return Response({"message":"Rating submitted successfully!"}, status=status.HTTP_200_OK)