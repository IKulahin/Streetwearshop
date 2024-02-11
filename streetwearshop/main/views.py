from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from .forms import *
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db import transaction
from django.db.models import Sum
# Create your views here.


def main(request):
    categories = Category.objects.all()
    sexs = Sex.objects.all()

    category_filter = request.GET.get('category', None)
    sex_filter = request.GET.get('sex', None)
    search_query = request.GET.get('search', None)

    products = Product.objects.all()

    if category_filter:
        products = products.filter(categories__name=category_filter)

    if sex_filter:
        products = products.filter(sex__name=sex_filter)

    if search_query:
        products = products.filter(name__icontains=search_query)

    context = {
        'products': products,
        'categories': categories,
        'sexs': sexs,
    }
    return render(request, 'html/main.html', context)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return redirect('login')
    else:
        form = SignUpForm()

    context = {
        'form': form
    }

    return render(request, 'html/signup.html', context)


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('main')
    else:
        form = AuthenticationForm()
    return render(request, 'html/login.html', {'form': form})


def logout_user(request):
    auth_logout(request)
    return redirect('main')


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.save()
            return redirect('product_detail', pk=pk)

    reviews = Review.objects.filter(product=product)

    context = {
        'product': product,
        'form': form,
        'reviews': reviews,
    }
    return render(request, 'html/product.html', context)


@login_required
def create_review(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('detailed_product', pk=product.pk)
    else:
        form = ReviewForm()
    return render(request, 'html/product.html', {'form': form, 'product': product})


@transaction.atomic
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)

    cart_item, _ = CartItem.objects.get_or_create(user=user, product=product, defaults={'quantity': 0, 'price': product.price})
    cart_item.quantity += 1
    cart_item.save()

    if created:
        cart.save()
    cart.items.add(cart_item)

    return redirect('main')


def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            phone_number = form.cleaned_data['phone_number']
            payment_method = form.cleaned_data['payment_method']

            cart, created = Cart.objects.get_or_create(user=request.user)
            products = cart.products.all()

            order = Order.objects.create(
                user=request.user,
                address=address,
                phone_number=phone_number,
                payment_method=payment_method,
                total_price=calculate_total_price(products),
            )

            order.products.set(products)
            order.save()

            cart.products.clear()

            return render(request, 'html/confirmation.html', {
                'address': address,
                'phone_number': phone_number,
                'payment_method': payment_method,
                'products': products,
            })
    else:
        form = OrderForm()

    return render(request, 'html/order.html', {'form': form})


def calculate_total_price(selected_products):
    total_price = 0

    for product in selected_products:
        total_price += product.price

    return total_price


def cart_view(request):
    user = request.user
    try:
        cart = Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        cart = None

    if cart:
        cart_items = cart.items.all()
        total_price = cart_items.aggregate(Sum('total_price'))['total_price__sum'] or 0
    else:
        cart_items = []
        total_price = 0

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': total_price,
    }

    return render(request, 'html/cart.html', context)
