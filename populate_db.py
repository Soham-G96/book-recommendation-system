import random
from django.contrib.auth.models import User
from books.models import Book, UserPreference
from django.db import transaction

def create_sample_data():
    with transaction.atomic():
        # Create users
        users = []
        for i in range(5):
            user, created = User.objects.get_or_create(username=f"user{i}", email=f"user{i}@test.com")
            if created:
                user.set_password("testpassword123")  # Setting a default password
                user.save()
            users.append(user)

        # Create books
        books = []
        for i in range(10):
            book, _ = Book.objects.get_or_create(
                title=f"Book {i}",
                author=f"Author {i}",
                genre=random.choice(["Fiction", "Sci-Fi", "Romance", "Mystery", "Fantasy"]),
                description=f"Description of Book {i}",
                rating=round(random.uniform(3, 5), 1)
            )
            books.append(book)

        # Assign user preferences
        for user in users:
            user_pref, _ = UserPreference.objects.get_or_create(user=user)
            user_pref.preferred_genres = random.choice(["Fiction", "Sci-Fi", "Romance", "Mystery", "Fantasy"])
            user_pref.save()

            # Assign read books
            user_pref.read_books.set(random.sample(books, 3))  # Assign 3 random books as read
            user_pref.save()

        print("Sample data added successfully!")

# Run the function
create_sample_data()
