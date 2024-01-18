from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *


class SignUpForm(UserCreationForm):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']


class ProductSearchForm(forms.Form):
    search_query = forms.CharField(label='Search', max_length=100, required=False)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address', 'phone_number', 'payment_method']
        error_messages = {
            'address': {'required': ''},
            'phone_number': {'required': ''},
            'payment_method': {'required': ''},
        }

    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
    ]

    payment_method = forms.ChoiceField(
        choices=PAYMENT_METHOD_CHOICES,
        widget=forms.Select(attrs={'class': 'your-custom-css-class'}),
        required=True,
        label='Payment Method'
    )

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['payment_method'].empty_label = None
        self.fields['products'] = forms.CharField(widget=forms.HiddenInput())
        self.fields.pop('products', None)
