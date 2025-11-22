from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Customer, Product, Order, Review
from .models import Order

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
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['phone', 'address', 'city', 'state', 'zip_code']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
        }

class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '1'})
    )

class CheckoutForm(forms.ModelForm):
    payment_method = forms.ChoiceField(
        choices=[
            ('gcash', 'GCash - Mobile Money'),
            ('cash_on_pickup', 'Cash on Pickup'),
        ],
        widget=forms.Select(attrs={'class': 'form-control form-select'}),
        required=True,
        help_text='Select your preferred payment method'
    )

    class Meta:
        model = Order
        fields = ['payment_method']

        widgets = {
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any special instructions?'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)], attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Share your experience...'}),
        }

class ProductSearchForm(forms.Form):
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search products...'})
    )
    category = forms.ModelChoiceField(
        queryset=None,
        required=False,
        empty_label="All Categories",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import Category
        self.fields['category'].queryset = Category.objects.all()
from django import forms
from .models import Order

class OrderProcessForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status', 'notes', 'payment_status', 'payment_method']  # match existing fields
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'payment_status': forms.Select(attrs={'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
        }
        # myapp/forms.py
from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    customer_name = forms.CharField(
        label="Customer",
        required=False,
        disabled=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Order
        fields = [
            'order_code',
            'customer_name',  # show this instead of editable 'customer'
            'status',
            'total_amount',
            'notes',
            'preparation_time',
            'pickup_time',
            'payment_method',
            'payment_status',
        ]
        widgets = {
            'order_code': forms.TextInput(attrs={'class': 'form-control', 'disabled': True}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'payment_status': forms.Select(attrs={'class': 'form-select'}),
            'total_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'preparation_time': forms.NumberInput(attrs={'class': 'form-control'}),
            'pickup_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'payment_method': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.customer:
            self.fields['customer_name'].initial = self.instance.customer.user.get_full_name()


class OrderAdminForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'customer',
            'status',
            'notes',
            'preparation_time',
            'pickup_time',
            'payment_method',
            'payment_status',
        ]
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'preparation_time': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'pickup_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'payment_method': forms.TextInput(attrs={'class': 'form-control'}),
            'payment_status': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure Bootstrap styling on any widget not covered above
        for name, field in self.fields.items():
            css_class = field.widget.attrs.get('class')
            if not css_class:
                field.widget.attrs['class'] = 'form-control'

        if self.instance and self.instance.pk:
            self.fields['customer'].disabled = True
            self.fields['customer'].help_text = 'Customer is fixed once the order is created.'
