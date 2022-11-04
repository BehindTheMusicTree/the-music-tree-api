from django.contrib.auth.models import User

class UserDAO:
    def exists (username):
        return User.objects.filter(username=username).exists()

    def create (username, email, password):
        return User.objects.create_user(username=username, email=email, password=password)