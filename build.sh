#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input

# Create superuser if it doesn't exist
echo "Creating superuser..."
echo "ADMIN_USERNAME: $ADMIN_USERNAME"
echo "ADMIN_EMAIL: $ADMIN_EMAIL"
echo "ADMIN_PASSWORD: [REDACTED]"

python manage.py shell <<EOF
import os
from django.contrib.auth import get_user_model
User = get_user_model()

username = os.environ.get('ADMIN_USERNAME', 'unclebrew')
email = os.environ.get('ADMIN_EMAIL', 'unclebrew@gmail.com')
password = os.environ.get('ADMIN_PASSWORD', '123456789')

print(f"Environment variables:")
print(f"ADMIN_USERNAME: {username}")
print(f"ADMIN_EMAIL: {email}")
print(f"Looking for user: {username}")

try:
    if not User.objects.filter(username=username).exists():
        print("Creating new superuser...")
        user = User.objects.create_superuser(username, email, password)
        print(f"Superuser created successfully: {user.username}")
    else:
        print('Superuser already exists')
        user = User.objects.get(username=username)
        print(f"Found existing user: {user.username}")
except Exception as e:
    print(f"Error creating superuser: {e}")
    # Fallback: try with hardcoded values
    if not User.objects.filter(username='unclebrew').exists():
        print("Trying fallback with hardcoded values...")
        User.objects.create_superuser('unclebrew', 'unclebrew@gmail.com', '123456789')
        print("Fallback superuser created")
EOF