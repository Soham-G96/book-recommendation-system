from rest_framework import serializers
from .models import Book, UserPreference, Rating

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class UserPreferenceSerializer(serializers.ModelSerializer):
    read_books = serializers.PrimaryKeyRelatedField(many=True, queryset=Book.objects.all())
    class Meta:
        model = UserPreference
        fields = ['preferred_genres','read_books']

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'