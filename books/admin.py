from django.contrib import admin
from .models import Book, UserPreference, Rating

# Register your models here.
admin.site.register(Book)
admin.site.register(UserPreference)
admin.site.register(Rating)