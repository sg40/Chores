from django.core.management.base import BaseCommand
from chores.models import User

class Command(BaseCommand):
    help = 'Create a user for testing'

    def add_arguments(self, parser):
        parser.add_argument('--name', type=str, help='User name', default='Test User')
        parser.add_argument('--email', type=str, help='User email', default='test@example.com')
        parser.add_argument('--password', type=str, help='User password', default='password123')
        parser.add_argument('--admin', action='store_true', help='Make user an admin')

    def handle(self, *args, **options):
        name = options['name']
        email = options['email']
        password = options['password']
        admin = options['admin']

        # Check if user already exists
        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.WARNING(f'User with email {email} already exists.')
            )
            return

        # Create user
        user = User(name=name, email=email, admin=admin)
        user.set_password(password)
        user.save()

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created user "{name}" with email "{email}" (admin: {admin})'
            )
        )

# Usage: python3 manage.py create_user --name "User Name" --email "user@example.com" --password "password123" [--admin]
