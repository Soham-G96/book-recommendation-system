from django.urls import path
from .views import BookListCreateView, BookDetailView, UserPreferenceView, BookRecommendationView, ReviewView, ReviewDetailView, GenreListView

urlpatterns = [
    path('genres/', GenreListView.as_view(), name='genre_list'),
    path('books/', BookListCreateView.as_view(), name='book_list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('preferences/', UserPreferenceView.as_view(), name='user_preferences'),
    path('recommendations/', BookRecommendationView.as_view(), name='book_recommendations'),
    path('books/<int:book_id>/reviews/', ReviewView.as_view(), name='book_reviews'),
    path('books/<int:book_id>/reviews/my/', ReviewDetailView.as_view(), name='my_review'),
]