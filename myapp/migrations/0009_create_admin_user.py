from django.db import migrations
from django.contrib.auth import get_user_model

def create_admin_user(apps, schema_editor):
    User = get_user_model()
    if not User.objects.filter(username='unclebrew').exists():
        User.objects.create_superuser('unclebrew', 'unclebrew@gmail.com', '123456789')

class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_remove_order_product_name_alter_order_order_code'),
    ]

    operations = [
        migrations.RunPython(create_admin_user),
    ]
