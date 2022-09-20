from django.contrib.auth.models import User

def CreateUser (name, email, password):
    user = User.objects.create_user(name, email, password)
    return user.id