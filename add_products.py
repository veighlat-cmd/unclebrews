#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from myapp.models import Category, Product
from myapp.catalog import CATALOG

def add_products():
    print("Adding products to Uncle Brews...")
    
    # Create categories
    categories = {
        'Iced Coffee': Category.objects.get_or_create(
            name='Iced Coffee',
            defaults={'description': 'Refreshing iced coffee beverages'}
        )[0],
        'Frappuccino': Category.objects.get_or_create(
            name='Frappuccino',
            defaults={'description': 'Blended coffee drinks'}
        )[0],
        'Signature Latte': Category.objects.get_or_create(
            name='Signature Latte',
            defaults={'description': 'Premium latte creations'}
        )[0],
        'Frappe': Category.objects.get_or_create(
            name='Frappe',
            defaults={'description': 'Chilled blended beverages'}
        )[0],
        'Milk Tea': Category.objects.get_or_create(
            name='Milk Tea',
            defaults={'description': 'Classic milk tea in various sizes'}
        )[0],
    }
    
    # Build products from central CATALOG
    for category_name, conf in CATALOG.items():
        cat = categories[category_name]

        # Case A: uniform price per category
        if 'products' in conf:
            price = float(conf['price'])
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
                print(f"Added: {product_name} - ₱{price:.2f}")

        # Case B: per-item price list
        if 'products_with_prices' in conf:
            for product_name, price in conf['products_with_prices']:
                Product.objects.get_or_create(
                    name=product_name,
                    defaults={
                        'description': f'{product_name} from our {category_name} collection',
                        'price': float(price),
                        'category': cat,
                        'stock': 50,
                        'is_available': True,
                    }
                )
                print(f"Added: {product_name} - ₱{float(price):.2f}")
    
    print("\n✅ All products added successfully!")
    print(f"Total products: {Product.objects.count()}")
    print(f"Total categories: {Category.objects.count()}")

if __name__ == '__main__':
    add_products()
