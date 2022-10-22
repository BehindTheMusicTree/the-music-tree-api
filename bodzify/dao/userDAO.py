from django.contrib.auth.models import User

def get (username):
    return User.objects.get(username=username)

def create (username, email, password):
    return User.objects.create_user(username=username, email=email, password=password)