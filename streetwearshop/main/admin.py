from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Sex)
admin.site.register(Review)
admin.site.register(CartItem)
admin.site.register(Cart)


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1


