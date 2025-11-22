"""
Central product catalog – easy-to-find list of product names (and prices).
Edit this file to change the official product names shown across the site.

Usage:
- The seed script (add_products.py) reads from CATALOG to create/update products.
- You can add/remove items here; then re-run add_products.py to sync the DB.
"""

from decimal import Decimal


# Per-category product lists. Update names here.
CATALOG = {
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
    # Milk Tea has different prices per size; specify explicitly.
    "Milk Tea": {
        "products_with_prices": [
            ("Milk Tea - Small", Decimal("39.00")),
            ("Milk Tea - Medium", Decimal("49.00")),
            ("Milk Tea - Large", Decimal("59.00")),
        ]
    },
}


