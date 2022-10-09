from django.db import models
from django.contrib.auth.models import User

class SongDB(models.Model):
    path = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)