from django.urls import path
from products.views import get_product, add_to_cart, view_cart, update_cart

urlpatterns = [
    path('product/<slug>/', get_product, name='get_product'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('update-cart/<int:item_id>/', update_cart, name='update_cart'),
]
