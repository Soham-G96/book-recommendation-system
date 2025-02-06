from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Book, UserPreference
from .serializers import BookSerializer, UserPreferenceSerializer


# Create your views here.

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class UserPreferenceView(generics.RetrieveUpdateAPIView):
    queryset = UserPreference.objects.all()
    serializer_class = UserPreferenceSerializer
    permission_classes = [IsAuthenticated]

