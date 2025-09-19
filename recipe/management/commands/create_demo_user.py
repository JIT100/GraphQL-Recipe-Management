from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os


class Command(BaseCommand):
    help = 'Create or update a demo user from environment variables (DEMO_USERNAME, DEMO_PASSWORD, DEMO_EMAIL, DEMO_IS_SUPERUSER)'

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.environ.get('DEMO_USERNAME')
        password = os.environ.get('DEMO_PASSWORD')
        email = os.environ.get('DEMO_EMAIL', '')
        is_super = os.environ.get('DEMO_IS_SUPERUSER', 'False').lower() in ('1', 'true', 'yes')

        if not username or not password:
            # Don't treat missing demo credentials as an error; skip quietly in development.
            self.stdout.write(self.style.WARNING('DEMO_USERNAME or DEMO_PASSWORD not set; skipping demo user creation.'))
            return

        user, created = User.objects.update_or_create(
            username=username,
            defaults={'email': email}
        )
        user.set_password(password)
        user.is_superuser = is_super
        user.is_staff = is_super or user.is_staff
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f'Demo user "{username}" created.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Demo user "{username}" updated.'))
