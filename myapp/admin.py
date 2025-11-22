from django.contrib import admin
from .models import Category, Product, Customer, Order, OrderItem, Review, Payment
from django.urls import path
from django.shortcuts import render, redirect, get_object_or_404
from django import forms

# -----------------------------
# Order process form
# -----------------------------
class OrderProcessForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status', 'preparation_time', 'pickup_time', 'notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'preparation_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'pickup_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


# -----------------------------
# Order admin
# -----------------------------
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['subtotal']




    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.calculate_total()


# -----------------------------
# Other admin registrations
# -----------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'is_available', 'created_at']
    list_filter = ['category', 'is_available', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['price', 'stock', 'is_available']
    ordering = ['name']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'city', 'state', 'created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'phone']
    list_filter = ['city', 'state', 'created_at']
    ordering = ['user__first_name']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'customer', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['product__name', 'customer__user__username']
    readonly_fields = ['created_at']
    ordering = ['-created_at']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['order', 'payment_method', 'amount', 'status', 'created_at']
    list_filter = ['payment_method', 'status', 'created_at']
    search_fields = ['order__order_id', 'reference_number', 'transaction_id']
    readonly_fields = ['order', 'amount', 'created_at', 'updated_at']
    ordering = ['-created_at']
from django.utils.html import format_html

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_code', 'customer', 'status', 'total_amount', 'created_at')
    list_display_links = ('order_code',)  # Makes order_code clickable
    search_fields = ('order_code', 'customer_name')
    list_filter = ('status', 'created_at')


    # Add a column with a clickable link
    def manage_link(self, obj):
        return format_html(
            '<a class="button" href="{}">Manage</a>',
            f'/admin/myapp/order/manage/{obj.order_id}/'
        )
    manage_link.short_description = 'Manage Order'
    manage_link.allow_tags = True

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('manage/<uuid:order_id>/', self.admin_site.admin_view(self.manage_order), name="manage_order"),
        ]
        return custom_urls + urls

    def manage_order(self, request, order_id):
        order = get_object_or_404(Order, order_id=order_id)
        if request.method == 'POST':
            form = OrderProcessForm(request.POST, instance=order)
            if form.is_valid():
                form.save()
                self.message_user(request, "Order updated successfully ✅")
                return redirect("admin:myapp_order_changelist")
        else:
            form = OrderProcessForm(instance=order)

        return render(request, "admin/manage_order.html", {"form": form, "order": order})
    from django.contrib import admin
from .models import Order


