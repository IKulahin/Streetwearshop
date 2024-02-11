from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class Sex(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.TextField()
    categories = models.ManyToManyField(Category)
    sex = models.ManyToManyField(Sex)
    material = models.CharField(max_length=255, default=0)
    type = models.CharField(max_length=255, default=0)
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.name


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username}\'s cart item for {self.product.name}'


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem, related_name='cart_items')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def update_total_price(self):
        self.total_price = sum(item.total_price for item in self.items.all())
        self.save()

    def save(self, *args, **kwargs):
        update_fields = kwargs.pop('update_fields', None)
        self.update_total_price()
        super().save(*args, **kwargs, update_fields=['total_price'])

    def __str__(self):
        return f'{self.user.username}\'s cart'


class Order(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=255, default='')
    phone_number = models.CharField(max_length=15, default='')
    payment_method = models.CharField(max_length=20, default='')

    def __str__(self):
        return f'{self.user}\'s order'


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField(default=1, choices=[(i, i) for i in range(1, 6)])
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Review by {self.user.username} for {self.product.name}'
