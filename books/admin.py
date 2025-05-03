from django.contrib import admin
from .models import Book, UserPreference, Review, Genre

# Register your models here.
admin.site.register(Book)
admin.site.register(UserPreference)
admin.site.register(Review)
admin.site.register(Genre)