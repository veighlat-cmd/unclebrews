from django.db import migrations
from decimal import Decimal

def populate_products(apps, schema_editor):
    Category = apps.get_model('myapp', 'Category')
    Product = apps.get_model('myapp', 'Product')
    
    # Create categories and products from catalog
    catalog = {
        "Iced Coffee": {
            "price": Decimal("59.00"),
            "products": [
                "Iced Americano",
                "Iced Latte", 
                "Iced Mocha",
                "Iced Caramel",
                "Iced Vanilla",
                "Iced Hazelnut",
                "Iced Cinnamon",
            ],
        },
        "Frappuccino": {
            "price": Decimal("69.00"),
            "products": [
                "Mocha Frappuccino",
                "Caramel Frappuccino",
                "Vanilla Frappuccino", 
                "Strawberry Frappuccino",
                "Chocolate Frappuccino",
            ],
        },
        "Signature Latte": {
            "price": Decimal("49.00"),
            "products": [
                "Classic Latte",
                "Hazelnut Latte",
                "Vanilla Latte",
                "Cinnamon Latte",
                "Caramel Latte",
                "Mocha Latte",
                "Pumpkin Spice Latte",
                "Peppermint Latte",
            ],
        },
        "Frappe": {
            "price": Decimal("59.00"),
            "products": [
                "Coffee Frappe",
                "Mocha Frappe",
                "Caramel Frappe",
                "Vanilla Frappe",
                "Chocolate Frappe",
                "Strawberry Frappe",
                "Oreo Frappe",
                "Cookies and Cream Frappe",
            ],
        },
        "Milk Tea": {
            "products_with_prices": [
                ("Milk Tea - Small", Decimal("39.00")),
                ("Milk Tea - Medium", Decimal("49.00")),
                ("Milk Tea - Large", Decimal("59.00")),
            ]
        },
    }
    
    for category_name, conf in catalog.items():
        cat, created = Category.objects.get_or_create(
            name=category_name,
            defaults={'description': f'{category_name} beverages'}
        )
        
        # Case A: uniform price per category
        if 'products' in conf:
            price = conf['price']
            for product_name in conf['products']:
                Product.objects.get_or_create(
                    name=product_name,
                    defaults={
                        'description': f'{product_name} from our {category_name} collection',
                        'price': price,
                        'category': cat,
                        'stock': 50,
                        'is_available': True,
                    }
                )
        
        # Case B: per-item price list
        if 'products_with_prices' in conf:
            for product_name, price in conf['products_with_prices']:
                Product.objects.get_or_create(
                    name=product_name,
                    defaults={
                        'description': f'{product_name} from our {category_name} collection',
                        'price': price,
                        'category': cat,
                        'stock': 50,
                        'is_available': True,
                    }
                )

def reverse_products(apps, schema_editor):
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('myapp', '0010_create_default_categories'),
    ]

    operations = [
        migrations.RunPython(populate_products, reverse_products),
    ]