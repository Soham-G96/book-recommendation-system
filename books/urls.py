from django.urls import path
from .views import BookListCreateView, BookDetailView, UserPreferenceView

urlpatterns = [
    path('books/', BookListCreateView.as_view(), name='book_list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('preferences/', UserPreferenceView.as_view(), name='user_preferences')
]