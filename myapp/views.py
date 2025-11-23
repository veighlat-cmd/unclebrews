from decimal import Decimal

from django import forms as django_forms
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from django.db import transaction
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.forms import inlineformset_factory
from .models import Category, Product, Customer, Order, OrderItem, Review, Payment
from .forms import (
    UserRegistrationForm, CustomerProfileForm, AddToCartForm,
    CheckoutForm, ReviewForm, ProductSearchForm, OrderAdminForm, ProductAdminForm
)

import json

OrderItemFormSet = inlineformset_factory(
    Order,
    OrderItem,
    fields=['product', 'quantity', 'price'],
    extra=1,
    can_delete=True,
    widgets={
        'product': django_forms.Select(attrs={'class': 'form-select'}),
        'quantity': django_forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        'price': django_forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
    }
)


def _calculate_items_total(order, items=None):
    items = items if items is not None else order.items.all()
    total = Decimal('0.00')
    for item in items:
        total += Decimal(item.subtotal)
    return total


def _recalculate_order_total(order):
    total = _calculate_items_total(order)
    order.total_amount = total
    order.save(update_fields=['total_amount'])


def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_staff:
                messages.success(request, "Logged in as admin.")
                return redirect("manage_orders")
            messages.success(request, "Logged in successfully.")
            return redirect("product_list")

        messages.error(request, "Invalid username or password.")

    return render(request, "myapp/admin_login.html")
def landing_page(request):
    """Landing page for non-authenticated users"""
    if request.user.is_authenticated:
        return redirect('/products/')
    return render(request, 'myapp/landing_page.html')

@login_required
def home(request):
    """Home page with featured products and categories"""
    categories = Category.objects.all()[:6]
    featured_products = Product.objects.filter(is_available=True, stock__gt=0)[:8]
    
    context = {
        'categories': categories,
        'featured_products': featured_products,
    }
    return render(request, 'myapp/home.html', context)

def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'myapp/register.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages

def user_login(request):
    """
    User login view that always redirects to product page after login.
    """
    if request.method == 'POST':
        identifier = request.POST.get('email')  # field still named email in form
        password = request.POST.get('password')

        if not identifier or not password:
            messages.error(request, 'Please provide both email/username and password.')
            return render(request, 'myapp/login.html')

        user_obj = None
        if '@' in identifier:
            try:
                user_obj = User.objects.get(email__iexact=identifier)
            except User.DoesNotExist:
                pass
        else:
            try:
                user_obj = User.objects.get(username__iexact=identifier)
            except User.DoesNotExist:
                pass

        if not user_obj:
            messages.error(request, 'Invalid credentials.')
            return render(request, 'myapp/login.html')

        user = authenticate(username=user_obj.username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                messages.success(request, 'Welcome back Admin!')
                return redirect('manage_orders')
            messages.success(request, f'Welcome back, {user.first_name}!')
            return redirect('product_list')
        else:
            messages.error(request, 'Invalid email or password.')

    # GET request
    return render(request, 'myapp/login.html')


def user_logout(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('landing_page')


def admin_logout(request):
    """Staff logout redirecting to admin login"""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')

@login_required
def product_list(request):
    """Product listing with search and filtering"""
    products = Product.objects.filter(is_available=True)
    search_form = ProductSearchForm(request.GET)
    
    if search_form.is_valid():
        search = search_form.cleaned_data.get('search')
        category = search_form.cleaned_data.get('category')
        
        if search:
            products = products.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )
        
        if category:
            products = products.filter(category=category)
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_form': search_form,
        'categories': Category.objects.all(),
    }
    return render(request, 'myapp/product_list.html', context)

@login_required
def product_detail(request, product_id):
    """Product detail view with reviews"""
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all()
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    if request.method == 'POST' and request.user.is_authenticated:
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.product = product
            review.customer = request.user.customer
            review.save()
            messages.success(request, 'Review submitted successfully!')
            return redirect('product_detail', product_id=product.id)
    else:
        review_form = ReviewForm()
    
    context = {
        'product': product,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'review_form': review_form,
        'add_to_cart_form': AddToCartForm(),
    }
    return render(request, 'myapp/product_detail.html', context)

@login_required
def add_to_cart(request, product_id):
    """Add product to cart"""
    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            product = get_object_or_404(Product, id=product_id)
            quantity = form.cleaned_data['quantity']
            
            # Get or create cart session
            cart = request.session.get('cart', {})
            product_id_str = str(product_id)
            
            if product_id_str in cart:
                cart[product_id_str]['quantity'] += quantity
            else:
                cart[product_id_str] = {
                    'quantity': quantity,
                    'price': float(product.price),
                    'name': product.name,
                    'image': product.image.url if product.image else '',
                }
            
            request.session['cart'] = cart
            request.session.modified = True
            
            messages.success(request, f'{product.name} added to cart!')
            return redirect('cart')
    
    return redirect('product_detail', product_id=product_id)

@login_required
def cart(request):
    """Shopping cart view"""
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    
    for product_id, item_data in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            if product.in_stock:
                subtotal = item_data['quantity'] * item_data['price']
                total += subtotal
                cart_items.append({
                    'product': product,
                    'quantity': item_data['quantity'],
                    'price': item_data['price'],
                    'subtotal': subtotal,
                })
        except Product.DoesNotExist:
            # Remove invalid products from cart
            del cart[product_id]
    
    request.session['cart'] = cart
    request.session.modified = True
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'myapp/cart.html', context)

@login_required
def update_cart(request, product_id):
    """Update cart item quantity"""
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 0))
        cart = request.session.get('cart', {})
        product_id_str = str(product_id)
        
        if quantity > 0:
            cart[product_id_str]['quantity'] = quantity
        else:
            del cart[product_id_str]
        
        request.session['cart'] = cart
        request.session.modified = True
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False})

@login_required
def remove_from_cart(request, product_id):
    """Remove item from cart"""
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        del cart[product_id_str]
        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request, 'Item removed from cart!')
    
    return redirect('cart')

@login_required
def checkout(request):
    """Checkout process"""
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, 'Your cart is empty!')
        return redirect('product_list')
    
    # Get cart items with full product information
    cart_items = []
    total = 0
    
    for product_id, item_data in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            item_data['product'] = product
            item_data['name'] = product.name
            cart_items.append(item_data)
            total += item_data['quantity'] * item_data['price']
        except Product.DoesNotExist:
            continue
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Create order
            order = form.save(commit=False)
            # Ensure customer profile exists for this user
            customer_obj, _ = Customer.objects.get_or_create(user=request.user)
            order.customer = customer_obj
            order.payment_method = form.cleaned_data['payment_method']
            order.save()
            
            # Create order items
            for item_data in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item_data['product'],
                    quantity=item_data['quantity'],
                    price=item_data['price']
                )
                
                # Update stock
                product = item_data['product']
                product.stock -= item_data['quantity']
                product.save()
            
            # Calculate total and clear cart
            order.calculate_total()
            
            # Create payment record
            payment = Payment.objects.create(
                order=order,
                payment_method=form.cleaned_data['payment_method'],
                amount=order.total_amount,
                status='pending'
            )
            
            # Clear cart
            del request.session['cart']
            request.session.modified = True
            
            # Redirect based on payment method
            if form.cleaned_data['payment_method'] in ['gcash']:
                # For digital wallets, show payment instructions
                messages.success(request, f'Order created! Please complete your payment via {form.cleaned_data["payment_method"].upper()}.')
                return redirect('payment_instructions', order_id=order.order_id)
            elif form.cleaned_data['payment_method'] == 'cash_on_pickup':
                # For cash on pickup, confirm order
                messages.success(request, f'Order placed successfully! Order ID: {order.order_id}. Pay with cash when you pick up.')
                return redirect('order_detail', order_id=order.order_id)
            else:
                # For other payment methods, show payment instructions
                messages.success(request, f'Order created! Please complete your payment.')
                return redirect('payment_instructions', order_id=order.order_id)
    else:
        form = CheckoutForm()
    
    context = {
        'form': form,
        'total': total,
        'cart_items': cart_items,
    }
    return render(request, 'myapp/checkout.html', context)

@login_required
def order_list(request):
    """User's order history"""
    orders = request.user.customer.orders.all()
    context = {
        'orders': orders,
    }
    return render(request, 'myapp/order_list.html', context)

@login_required
def customer_order_detail(request, order_id):
    """Authenticated customer's order detail view"""
    order = get_object_or_404(Order, order_id=order_id, customer=request.user.customer)
    context = {
        'order': order,
    }
    return render(request, 'myapp/order_detail.html', context)

@login_required
def payment_instructions(request, order_id):
    """Payment instructions page"""
    order = get_object_or_404(Order, order_id=order_id, customer=request.user.customer)
    payment = get_object_or_404(Payment, order=order)
    
    # Payment instructions for different methods
    payment_instructions = {
        'gcash': {
            'title': 'GCash Payment Instructions',
            'steps': [
                'Open your GCash app',
                'Go to "Send Money" or "Pay Bills"',
                'Enter our GCash number: 0917-123-4567',
                'Enter the amount: ₱{amount}',
                'Add reference: Order {order_id}',
                'Confirm and send payment',
                'Take a screenshot of the payment confirmation'
            ],
            'icon': 'fas fa-mobile-alt',
            'color': '#667eea'
        },
        
    }
    
    method = payment.payment_method
    instructions = payment_instructions.get(method, {})
    
    # Replace placeholders in instructions
    if instructions:
        for i, step in enumerate(instructions['steps']):
            instructions['steps'][i] = step.format(
                amount=order.total_amount,
                order_id=order.order_id
            )
    
    context = {
        'order': order,
        'payment': payment,
        'instructions': instructions,
    }
    return render(request, 'myapp/payment_instructions.html', context)

@login_required
def profile(request):
    """User profile management"""
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=request.user.customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = CustomerProfileForm(instance=request.user.customer)
    
    context = {
        'form': form,
    }
    return render(request, 'myapp/profile.html', context)

@login_required
def category_products(request, category_id):
    """Products filtered by category"""
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category, is_available=True)
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'myapp/category_products.html', context)

# -----------------------------
# Staff order management panel
# -----------------------------

@staff_member_required
def manage_orders(request):
    query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '').strip()

    orders = Order.objects.select_related('customer__user').prefetch_related('items__product')

    if query:
        orders = orders.filter(
            Q(order_code__icontains=query)
            | Q(customer__user__first_name__icontains=query)
            | Q(customer__user__last_name__icontains=query)
            | Q(customer__user__username__icontains=query)
        )

    if status_filter:
        orders = orders.filter(status=status_filter)

    paginator = Paginator(orders.order_by('-created_at'), 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'page_obj': page_obj,
        'query': query,
        'status_filter': status_filter,
        'status_choices': Order.STATUS_CHOICES,
    }
    return render(request, 'orders/manage_orders.html', context)


@staff_member_required
def order_detail(request, order_id):
    order = get_object_or_404(
        Order.objects.select_related('customer__user').prefetch_related('items__product'),
        order_id=order_id
    )
    items = order.items.all()
    computed_total = _calculate_items_total(order, items)

    context = {
        'order': order,
        'items': items,
        'computed_total': computed_total,
    }
    return render(request, 'orders/order_detail.html', context)


@staff_member_required
@transaction.atomic
def add_order(request):
    placeholder_order = Order()
    if request.method == 'POST':
        form = OrderAdminForm(request.POST)
        formset = OrderItemFormSet(request.POST, instance=placeholder_order, prefix='items')

        if form.is_valid() and formset.is_valid():
            order = form.save(commit=False)
            order.total_amount = Decimal('0.00')
            order.save()

            formset.instance = order
            formset.save()

            _recalculate_order_total(order)
            messages.success(request, 'Order created successfully.')
            return redirect('manage_order_detail', order_id=order.order_id)
    else:
        form = OrderAdminForm()
        formset = OrderItemFormSet(instance=placeholder_order, prefix='items')

    context = {
        'form': form,
        'formset': formset,
        'is_edit': False,
    }
    return render(request, 'orders/add_order.html', context)


@staff_member_required
@transaction.atomic
def edit_order(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)

    if request.method == 'POST':
        form = OrderAdminForm(request.POST, instance=order)
        formset = OrderItemFormSet(request.POST, instance=order, prefix='items')

        if form.is_valid() and formset.is_valid():
            order = form.save()
            formset.save()
            _recalculate_order_total(order)
            messages.success(request, 'Order updated successfully.')
            return redirect('manage_order_detail', order_id=order.order_id)
    else:
        form = OrderAdminForm(instance=order)
        formset = OrderItemFormSet(instance=order, prefix='items')

    context = {
        'form': form,
        'formset': formset,
        'order': order,
        'is_edit': True,
    }
    return render(request, 'orders/edit_order.html', context)


@staff_member_required
@transaction.atomic
def delete_order(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)

    if request.method == 'POST':
        order.delete()
        messages.success(request, 'Order deleted successfully.')
        return redirect('manage_orders')

    return render(request, 'orders/delete_order.html', {'order': order})


# ==============================
# Product CRUD Admin Views
# ==============================

@staff_member_required
def manage_products(request):
    """Product management admin interface"""
    products = Product.objects.all().order_by('name')
    
    # Search functionality
    query = request.GET.get('q', '')
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
    
    # Category filter
    category_filter = request.GET.get('category', '')
    if category_filter:
        products = products.filter(category_id=category_filter)
    
    # Availability filter
    available_filter = request.GET.get('available', '')
    if available_filter == 'yes':
        products = products.filter(is_available=True)
    elif available_filter == 'no':
        products = products.filter(is_available=False)
    
    # Pagination
    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get categories for filter dropdown
    categories = Category.objects.all()
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'category_filter': category_filter,
        'available_filter': available_filter,
        'categories': categories,
    }
    return render(request, 'products/manage_products.html', context)


@staff_member_required
def add_product(request):
    """Add new product"""
    if request.method == 'POST':
        form = ProductAdminForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Product "{product.name}" added successfully!')
            return redirect('manage_products')
    else:
        form = ProductAdminForm()
    
    return render(request, 'products/add_product.html', {'form': form})


@staff_member_required
def edit_product(request, product_id):
    """Edit existing product"""
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = ProductAdminForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Product "{product.name}" updated successfully!')
            return redirect('manage_products')
    else:
        form = ProductAdminForm(instance=product)
    
    return render(request, 'products/edit_product.html', {'form': form, 'product': product})


@staff_member_required
@transaction.atomic
def delete_product(request, product_id):
    """Delete product"""
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Product "{product_name}" deleted successfully!')
        return redirect('manage_products')
    
    return render(request, 'products/delete_product.html', {'product': product})

