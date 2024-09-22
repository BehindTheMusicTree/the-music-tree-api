import sys
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Check if the database is initialized with users'

    def handle(self, *args, **kwargs):
        user_count = User.objects.count()
        if user_count > 0:
            self.stdout.write(self.style.SUCCESS('Users found in the database.'))
            sys.exit(0)
        else:
            self.stdout.write(self.style.ERROR('No users found in the database. Data should be initialized.'))
            sys.exit(1)
