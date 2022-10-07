from django.urls import path
from .views import (
    CheckoutView,
    ItemListView,
    post_detail,
    OrderSummaryView, 
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart,
    search,
    about,
)

app_name = 'store'

urlpatterns = [
    path('', ItemListView.as_view(), name='store'),
    path('about/', about, name='about'),
    path('product/<slug>/', post_detail, name='product'),
    path('search', search, name='search'),
    path('order-summary/', OrderSummaryView.as_view(), name='order_summary'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('add-to-cart/<slug>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove_from_cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart, name='remove_single_item_from_cart')
]
