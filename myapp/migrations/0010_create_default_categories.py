from django.db import migrations

def create_default_categories(apps, schema_editor):
    Category = apps.get_model('myapp', 'Category')
    
    categories = [
        {'name': 'Coffee', 'description': 'Hot and cold coffee beverages'},
        {'name': 'Tea', 'description': 'Various tea selections'},
        {'name': 'Pastries', 'description': 'Fresh baked goods'},
        {'name': 'Snacks', 'description': 'Light snacks and treats'},
    ]
    
    for cat_data in categories:
        Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )

def reverse_categories(apps, schema_editor):
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('myapp', '0009_create_admin_user'),
    ]

    operations = [
        migrations.RunPython(create_default_categories, reverse_categories),
    ]