from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create admin user for deployment'

    def handle(self, *args, **options):
        User = get_user_model()
        username = 'unclebrew'
        email = 'unclebrew@gmail.com'
        password = '123456789'

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully'))
        else:
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" password updated'))
