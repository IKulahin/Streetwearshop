from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('main/', main, name='main'),
    path('detailed_product/<int:pk>/', product_detail, name="detailed_product"),
    path('signup/', signup, name="signup"),
    path('accounts/login/', login_user, name="login"),
    path('logout/', logout_user, name='logout'),
    path('product/<int:pk>/review/', create_review, name='create_review'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('place_order/', place_order, name='place_order'),
    path('cart/', cart_view, name='cart'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)