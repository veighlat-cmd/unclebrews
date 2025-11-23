#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# Create superuser if it doesn't exist
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username=os.environ.get('ADMIN_USERNAME', 'admin')).exists():
    User.objects.create_superuser(
        os.environ.get('ADMIN_USERNAME', 'unclebrew'),
        os.environ.get('ADMIN_EMAIL', 'unclebrew@gmail.com'),
        os.environ.get('ADMIN_PASSWORD', '123456789')
    )
    print(f"Superuser created: username={os.environ.get('ADMIN_USERNAME', 'admin')}")
else:
    print('Superuser already exists')
EOF