from django.urls import path
from .views import BookListView, UserPreferenceView

urlpatterns = [
    path('books/', BookListView.as_view(), name='book_list'),
    path('preferences/', UserPreferenceView.as_view(), name='user_preferences')
]