from django.urls import path

from shop.views import product_detail, products_list, new_products_list, gender_products_list, brands_list, \
    brand_products_list, search, cart_detail, remove_from_cart, add_to_cart, clear_cart, order_processed

urlpatterns = [
    path('product/<slug:slug>/', product_detail, name='product_detail'),
    path('category/', products_list, name='products_list'),
    path('category/<slug:slug>/', products_list, name='products_list_by_category'),
    path('news/', new_products_list, name='new_products_list'),
    path('gender/', gender_products_list, name='gender_products_list'),
    path('gender/<slug:slug>/', gender_products_list, name='gender_products_list'),
    path('brands/', brands_list, name='brands_list'),
    path('brands/<slug:slug>/', brand_products_list, name='brand_products_list'),
    path('search/', search, name='search'),
    path('cart/', cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:product_id>/', add_to_cart, name='cart_update'),
    path('cart/clear/', clear_cart, name='clear_cart'),
    path('cart/orderprocessed/', order_processed, name='order_processed')
]
