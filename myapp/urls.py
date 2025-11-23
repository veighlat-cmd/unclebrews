from django.urls import path
from . import views

urlpatterns = [
    # Landing page for non-authenticated users
    path('', views.landing_page, name='landing_page'),
    path('home/', views.home, name='home'),
    
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Products
    path('products/', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('category/<int:category_id>/', views.category_products, name='category_products'),
    
    # Cart and checkout
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<int:product_id>/', views.update_cart, name='update_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),

    # Customer orders
    path('orders/', views.order_list, name='order_list'),
    path('order/<uuid:order_id>/', views.customer_order_detail, name='order_detail'),
    path('payment-instructions/<uuid:order_id>/', views.payment_instructions, name='payment_instructions'),
    
    # User profile
    path('profile/', views.profile, name='profile'),

    # Staff admin login / order management
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    path('manage_orders/', views.manage_orders, name='manage_orders'),
    path('manage_orders/add/', views.add_order, name='manage_order_add'),
    path('manage_orders/<uuid:order_id>/view/', views.order_detail, name='manage_order_detail'),
    path('manage_orders/<uuid:order_id>/edit/', views.edit_order, name='manage_order_edit'),
    path('manage_orders/<uuid:order_id>/delete/', views.delete_order, name='manage_order_delete'),
    
    # Staff admin product management
    path('manage_products/', views.manage_products, name='manage_products'),
    path('manage_products/add/', views.add_product, name='manage_product_add'),
    path('manage_products/<int:product_id>/edit/', views.edit_product, name='manage_product_edit'),
    path('manage_products/<int:product_id>/delete/', views.delete_product, name='manage_product_delete'),
]
