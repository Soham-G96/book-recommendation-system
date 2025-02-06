from rest_framework import serializers
from .models import Book, UserPreference

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class UserPreferenceSerializer(serializers.ModelSerializer):
    read_books = serializers.PrimaryKeyRelatedField(many=True, queryset=Book.objects.all())
    class Meta:
        model = UserPreference
        fields = ['preferred_genres','read_books']