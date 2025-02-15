from rest_framework import serializers
from .models import Book, UserPreference, Review

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class UserPreferenceSerializer(serializers.ModelSerializer):
    read_books = serializers.PrimaryKeyRelatedField(many=True, queryset=Book.objects.all())
    class Meta:
        model = UserPreference
        fields = ['preferred_genres','read_books']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'book', 'user', 'rating', 'review_text', 'sentiment_score']
        read_only_fields = ['id', 'user','book', 'sentiment_score']

    def create(self, validated_data):
        # Override create to ensure the user is automatically assigned
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
